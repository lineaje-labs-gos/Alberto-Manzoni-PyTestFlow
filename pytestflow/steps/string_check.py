from prefect.artifacts import create_markdown_artifact
from pytestflow.core.core import StepWrapper
from pytestflow.core.pytestflow_states import PyTestflowPassed, PyTestflowFailed
from pytestflow.core.utils import get_data_for_gui
from pytestflow.steps.common import get_metadata_from_prefect_context
from typing import Callable
from pytestflow.steps.common import get_runtime_value
import re


class StringCheckStep(StepWrapper):
    def __init__(self, fn, *, expected, match="exact", case_sensitive=True,
                 name=None, autowire=True, **task_kwargs):
        super().__init__(fn, name=name, autowire=autowire, **task_kwargs)
        self.expected = expected
        self.match = match
        self.case_sensitive = case_sensitive
        self.step_type = "string_check"

    def _run(self, *args, **kwargs):
        actual = super()._run(*args, **kwargs)

        expected_value = get_runtime_value(self.expected)
        match_mode = get_runtime_value(self.match)
        is_case_sensitive = get_runtime_value(self.case_sensitive)

        if not isinstance(actual, str):
            raise TypeError(f"Expected string output, got {type(actual)}")

        compare_actual = actual if is_case_sensitive else actual.lower()
        compare_expected = expected_value if is_case_sensitive else expected_value.lower()

        if match_mode == "exact":
            passed = compare_actual == compare_expected
        elif match_mode == "contains":
            passed = compare_expected in compare_actual
        else:
            raise ValueError(f"Unsupported match mode: {match_mode}")

        result_data = {
            "step_status": "passed" if passed else "failed",
            "output": actual,
            "expected": expected_value,
            "match": match_mode,
            "case_sensitive": is_case_sensitive,
            "step_type": self.step_type,
        }

        result_data.update(self.get_meta_info())
        result_data.update(get_metadata_from_prefect_context())

        # Send End data to GUI
        get_data_for_gui(self, result_data.get("end_time"), result_data)

        # Prefect UI artifact (best-effort)
        try:
            safe_step_name = re.sub(r"[^a-z0-9\-]", "-", self.name.lower())

            artifact_md = (
                f"### Step: `{self.name}`\n"
                f"- **Actual:** `{actual}`\n"
                f"- **Expected:** `{expected_value}`\n"
                f"- **Match mode:** `{match_mode}`\n"
                f"- **Case sensitive:** `{is_case_sensitive}`\n"
                f"- **Status:** {'✅ PASSED' if passed else '❌ FAILED'}"
            )

            create_markdown_artifact(
                key=f"result-{safe_step_name}",
                markdown=artifact_md,
                description=f"String check for `{self.name}`",
            )

        except Exception:
            # Runtime might not support artifacts or not be in task context
            pass

        return (
            PyTestflowPassed(ptf_result=result_data)
            if passed
            else PyTestflowFailed(
                ptf_result=result_data,
                message=f"{self.name} failed"
            )
        )


def string_check_step(*, expected, match="exact", case_sensitive=True,
                      name=None, autowire=True, **task_kwargs):
    """
    Decorator factory for string check steps.
    """
    def decorator(fn: Callable):
        # IMPORTANT: already task-wrapped by StepWrapper
        return StringCheckStep(
            fn,
            expected=expected,
            match=match,
            case_sensitive=case_sensitive,
            name=name,
            autowire=autowire,
            **task_kwargs,
        )
    return decorator
