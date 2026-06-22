# numeric_limit_step.py
from pytestflow.core.core import StepWrapper
from pytestflow.core.pytestflow_states import PyTestflowPassed, PyTestflowFailed
from pytestflow.core.utils import get_data_for_gui
from pytestflow.steps.common import get_metadata_from_prefect_context, get_runtime_value
from typing import Callable
import re
from prefect.artifacts import create_markdown_artifact


class NumericLimitStep(StepWrapper):
    def __init__(self, fn, *, limit, mode, name=None, store_as=None, autowire=True, **task_kwargs):
        super().__init__(fn, name=name, autowire=autowire, **task_kwargs)
        self.limit = limit
        self.mode = mode
        self.store_as = store_as
        self.step_type = "numeric_limit"


    def _run(self, *args, **kwargs):
        from pytestflow.core.context import ptf_context

        value = super()._run(*args, **kwargs)

        limit = get_runtime_value(self.limit)
        mode = get_runtime_value(self.mode)
        store_as = get_runtime_value(self.store_as)

        if not isinstance(value, (int, float)):
            raise TypeError("Return value must be numeric")

        if mode == "ge":
            passed = value >= limit

        elif mode == "le":
            passed = value <= limit

        elif mode == "between":
            assert isinstance(limit, (list, tuple)) and len(limit) == 2
            passed = limit[0] <= value <= limit[1]

        elif mode == "outside":
            assert isinstance(limit, (list, tuple)) and len(limit) == 2
            passed = value < limit[0] or value > limit[1]

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        if store_as:
            ptf_context.locals[store_as] = value

        result_data = {
            "measurement": value,
            "limit": limit,
            "mode": mode,
            "store_as": store_as,
            "step_status": "passed" if passed else "failed",
            "output": value,
            "step_type": self.step_type,
        }

        result_data.update(self.get_meta_info())
        result_data.update(get_metadata_from_prefect_context())

        # Send End data to GUI
        get_data_for_gui(self, result_data.get("end_time"), result_data)

        try:
            safe_step_name = re.sub(r"[^a-z0-9\-]", "-", self.name.lower())

            artifact_md = (
                f"### Step: `{self.name}`\n"
                f"- **Measurement:** `{value}`\n"
                f"- **Limit ({mode}):** `{limit}`\n"
                f"- **Status:** {'✅ PASSED' if passed else '❌ FAILED'}"
            )

            create_markdown_artifact(
                key=f"result-{safe_step_name}",
                markdown=artifact_md,
                description=f"Numeric limit check for `{self.name}`",
            )

        except RuntimeError:
            pass

        return (
            PyTestflowPassed(ptf_result=result_data)
            if passed
            else PyTestflowFailed(
                ptf_result=result_data,
                message=f"{self.name} failed"
            )
        )


def numeric_limit_step(*, limit, mode="ge", name=None, store_as=None, autowire=True, **task_kwargs):
    def decorator(fn: Callable):
        # IMPORTANT: return the step instance (already task-wrapped by StepWrapper)
        return NumericLimitStep(
            fn,
            limit=limit,
            mode=mode,
            name=name,
            store_as=store_as,
            autowire=autowire,
            **task_kwargs,
        )
    return decorator
