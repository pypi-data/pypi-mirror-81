"""Scenario"""

from __future__ import annotations

from abc import ABC, abstractmethod
from concurrent.futures import Executor
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, List, Optional

from preacher.core.datetime import now
from preacher.core.extraction import analyze_data_obj
from preacher.core.status import Status, Statused, StatusedList, merge_statuses
from preacher.core.value import ValueContext
from preacher.core.verification import Description, Verification
from .case import Case, CaseListener, CaseResult
from .util.concurrency import CasesTask, OrderedCasesTask, UnorderedCasesTask


class ScenarioListener(CaseListener):
    """
    Interface to listen to scenario running.
    """
    pass


@dataclass(frozen=True)
class ScenarioResult(Statused):
    label: Optional[str] = None
    status: Status = Status.SKIPPED
    message: Optional[str] = None
    conditions: Verification = field(default_factory=Verification)
    cases: StatusedList[CaseResult] = field(default_factory=StatusedList)
    subscenarios: StatusedList[ScenarioResult] = field(
        default_factory=StatusedList,
    )


class ScenarioTask(ABC):

    @abstractmethod
    def result(self) -> ScenarioResult:
        raise NotImplementedError()


class RunningScenarioTask(ScenarioTask):

    def __init__(
        self,
        label: Optional[str],
        conditions: Verification,
        cases: CasesTask,
        subscenarios: List[ScenarioTask],
    ):
        self._label = label
        self._conditions = conditions
        self._cases = cases
        self._subscenarios = subscenarios

    def result(self) -> ScenarioResult:
        cases = self._cases.result()
        subscenarios = StatusedList.collect(
            s.result() for s in self._subscenarios
        )
        return ScenarioResult(
            label=self._label,
            status=merge_statuses([cases.status, subscenarios.status]),
            conditions=self._conditions,
            cases=cases,
            subscenarios=subscenarios,
        )


class StaticScenarioTask(ScenarioTask):

    def __init__(self, result: ScenarioResult):
        self._result = result

    def result(self) -> ScenarioResult:
        return self._result


@dataclass(frozen=True)
class ScenarioContext:
    starts: datetime = field(default_factory=now)
    base_url: str = ''
    retry: int = 0
    delay: float = 0.1
    timeout: Optional[float] = None


class Scenario:

    def __init__(
        self,
        label: Optional[str] = None,
        ordered: bool = True,
        conditions: Optional[List[Description]] = None,
        cases: Optional[List[Case]] = None,
        subscenarios: Optional[List[Scenario]] = None,
    ):
        self._label = label
        self._ordered = ordered
        self._conditions = conditions or []
        self._cases = cases or []
        self._subscenarios = subscenarios or []

    @property
    def label(self) -> Optional[str]:
        return self._label

    def submit(
        self,
        executor: Executor,
        base_url: str = '',
        retry: int = 0,
        delay: float = 0.1,
        timeout: Optional[float] = None,
        listener: Optional[ScenarioListener] = None,
    ) -> ScenarioTask:
        context = ScenarioContext(
            base_url=base_url,
            retry=retry,
            delay=delay,
            timeout=timeout,
        )
        context_analyzer = analyze_data_obj(context)
        value_context = ValueContext(origin_datetime=context.starts)
        conditions = Verification.collect(
            condition.verify(context_analyzer, value_context)
            for condition in self._conditions
        )
        if not conditions.status.is_succeeded:
            status = Status.SKIPPED
            if conditions.status is Status.FAILURE:
                status = Status.FAILURE

            result = ScenarioResult(
                label=self._label,
                status=status,
                conditions=conditions,
            )
            return StaticScenarioTask(result)

        listener = listener or ScenarioListener()

        if self._ordered:
            submit_cases: Callable = OrderedCasesTask
        else:
            submit_cases = UnorderedCasesTask
        cases = submit_cases(
            executor,
            self._cases,
            base_url=base_url,
            retry=retry,
            delay=delay,
            timeout=timeout,
            listener=listener,
        )

        subscenarios = [
            subscenario.submit(
                executor,
                base_url=base_url,
                retry=retry,
                delay=delay,
                timeout=timeout,
                listener=listener,
            )
            for subscenario in self._subscenarios
        ]
        return RunningScenarioTask(
            label=self._label,
            conditions=conditions,
            cases=cases,
            subscenarios=subscenarios,
        )
