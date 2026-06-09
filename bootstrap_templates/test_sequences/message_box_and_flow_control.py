from pytestflow.core.sequence import TestSequence
from pytestflow.core import ptf_context

from pytestflow.steps.message_pop_up import message_pop_up_step
from pytestflow.steps.numeric_limit import numeric_limit_step
from pytestflow.steps.pass_fail import pass_fail_step
from pytestflow.steps.flow_control import flow_control_step


# ------------------------------------------------------------
# USER INPUT STEP (message box)
# ------------------------------------------------------------
# This step displays a message box to the user and stores the response.
#
# The response is saved into ptf_context.locals using `store_as`.
#
# Typical use case:
# - operator confirmation
# - manual selection of test path
@message_pop_up_step(
    name="operator_confirmation",
    title="Operator Check",
    msg="Confirm that the setup is ready, then continue.",
    buttons=["Continue", "Cancel"],
    show_response_box=False,
    store_as="operator_confirmation_response",
)
def operator_confirmation():
    return "Message box displayed"


# ------------------------------------------------------------
# FLOW CONTROL STEP (based on user response)
# ------------------------------------------------------------
# This step decides the next execution path based on a condition.
#
# It returns an index that maps to `next_steps`:
#   0 → "end"
#   1 → "next"
#
# The decision is based on the stored user response.
@flow_control_step(
    name="check_operator_confirmation",
    next_steps={0: "end", 1: "next"},
)
def check_operator_confirmation():
    value = ptf_context.locals.get("operator_confirmation_response")
    return value["button"] == "Continue"


# ------------------------------------------------------------
# PASS / FAIL STEP
# ------------------------------------------------------------
@pass_fail_step(name="power_good_check")
def power_good_check():
    return True


# ------------------------------------------------------------
# NUMERIC LIMIT STEP
# ------------------------------------------------------------
@numeric_limit_step(name="vcore_voltage_check", limit=(1.0, 1.3), mode="between")
def vcore_voltage_check():
    return 1.15


# ------------------------------------------------------------
# USER SELECTION STEP (message box)
# ------------------------------------------------------------
# This step allows the operator to select a product/version.
# The selected value is stored for later flow routing.
@message_pop_up_step(
    name="operator_product_selection",
    title="Operator Product Selection",
    msg="Select Product Version",
    buttons=["Ver 1", "Ver 2", "Ver 3"],
    show_response_box=False,
    store_as="operator_product_selection_response",
)
def operator_product_selection():
    return "Selection step executed"


# ------------------------------------------------------------
# FLOW CONTROL BASED ON SELECTION
# ------------------------------------------------------------
# Converts the selected button into an execution index.
# This index is used to dynamically route the sequence.
@flow_control_step(
    name="check_operator_product_selection",
    next_steps={
        0: "ver1_test",
        1: "ver2_test",
        2: "ver3_test",
    },
)
def check_operator_product_selection():
    versions = ["Ver 1", "Ver 2", "Ver 3"]

    value = ptf_context.locals.get("operator_product_selection_response")
    idx = versions.index(value["button"])

    return idx


# ------------------------------------------------------------
# VERSION-SPECIFIC TESTS
# ------------------------------------------------------------
@numeric_limit_step(name="ver1_test", limit=(4.9, 5.1), mode="between")
def ver1_test():
    return 5.0


@numeric_limit_step(name="ver2_test", limit=(11.9, 12.1), mode="between")
def ver2_test():
    return 12.0


@numeric_limit_step(name="ver3_test", limit=(23.9, 24.1), mode="between")
def ver3_test():
    return 24.0


# ------------------------------------------------------------
# SIMPLE FLOW TERMINATION STEPS
# ------------------------------------------------------------
# These steps demonstrate explicit flow termination routing.
@flow_control_step(name="go_to_end_after_ver1", next_steps={0: "end"})
def go_to_end_after_ver1():
    return 0


@flow_control_step(name="go_to_end_after_ver2", next_steps={0: "end"})
def go_to_end_after_ver2():
    return 0


# ------------------------------------------------------------
# SEQUENCE DEFINITION
# ------------------------------------------------------------
# Demonstrates conditional execution and branching logic
# driven by user input and flow control steps.
def main_sequence() -> TestSequence:
    return TestSequence(
        name="MessageBoxAndFlowControl",
        setup_steps=[],
        main_steps=[
            operator_confirmation,
            check_operator_confirmation,
            power_good_check,
            vcore_voltage_check,
            operator_product_selection,
            check_operator_product_selection,
            ver1_test,
            go_to_end_after_ver1,
            ver2_test,
            go_to_end_after_ver2,
            ver3_test,
        ],
        cleanup_steps=[],
    )


# ------------------------------------------------------------
# PROCESS HOOK REGISTRATION
# ------------------------------------------------------------
PROCESS_HOOKS = {
    "main_sequence": main_sequence,
}