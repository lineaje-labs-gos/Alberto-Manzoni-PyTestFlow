from pytestflow.core.sequence import TestSequence
from pytestflow.steps.numeric_limit import numeric_limit_step
from pytestflow.steps.pass_fail import pass_fail_step

# ------------------------------------------------------------
# STEP 1: Numeric limit validation example
# ------------------------------------------------------------
# This step demonstrates how a numeric_limit_step works.
#
# The wrapped function MUST return a numeric value (int or float).
#
# The framework will validate the output using the selected comparator:
# - "ge"      → greater or equal
# - "le"      → less or equal
# - "between" → value must be within [min, max]
# - "outside" → value must be outside [min, max]
#
# This is a generic example and does not represent any specific domain.
@numeric_limit_step(name="measure_vcore", limit=(1.0, 1.3), mode="between")
def measure_vcore():
    return 1.15

# ------------------------------------------------------------
# STEP 2: Pass / Fail validation example
# ------------------------------------------------------------
# This step demonstrates a simple boolean-based check.
# The function must return True (pass) or False (fail).
@pass_fail_step(name="functional_check")
def functional_check():
    return True

# ------------------------------------------------------------
# TEST SEQUENCE DEFINITION
# ------------------------------------------------------------
# A TestSequence represents an executable workflow in PyTestFlow.
#
# Structure:
# - setup_steps   → executed before main execution (initialization phase)
# - main_steps    → primary execution steps
# - cleanup_steps → executed after execution (teardown phase)
#
# In this example:
# - no setup or cleanup steps are defined
# - two demonstration steps are executed sequentially
def main_sequence() -> TestSequence:
    return TestSequence(
        name="BasicSequence",
        setup_steps=[],
        main_steps=[measure_vcore, functional_check],
        cleanup_steps=[],
    )

# ------------------------------------------------------------
# PROCESS HOOK REGISTRATION
# ------------------------------------------------------------
# PROCESS_HOOKS maps a sequence name to its factory function.
# This enables dynamic discovery and execution of test sequences
# by the PyTestFlow runtime.
PROCESS_HOOKS = {
    "main_sequence": main_sequence,
}

