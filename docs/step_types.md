# Step Types Reference

PyTestFlow provides a set of step types that define how functions are executed, validated, and integrated into a TestSequence.

Each step type is implemented via a decorator and defines:
- input/output expectations
- validation logic
- runtime behavior

---

## Overview

| Step Type | Purpose |
|------------|--------|
| Action Step | Performs an action |
| Pass/Fail Step | Boolean validation |
| Numeric Limit Step | Validates numeric outputs against thresholds |
| DataFrame Numeric Limits Step | Multi-channel numeric validation |
| String Check Step | String comparison validation |
| Waveform Limit Step | Signal / waveform validation |
| Message Pop-up Step | User interaction / input |
| Flow Control Step | Dynamic execution branching |

---

## Action Step

Used to store values during execution for later retrieval.

### Example use case
- Logging intermediate results
- Sharing values between steps
- Reporting

---

## Pass/Fail Step

Returns a boolean value representing success or failure.

### Return type
- `True` → pass
- `False` → fail

### Example use case
- Digital signals
- Readiness checks
- Simple validation logic

---

## Numeric Limit Step

Validates a numeric output against defined limits.

### Supported comparison modes
- `ge` → greater or equal
- `le` → less or equal
- `between` → within range [min, max]
- `outside` → outside range [min, max]

### Example use case
- Scalar measurement validation

---

## DataFrame Numeric Limits Step

Extends numeric validation to multiple named values using a structured table.

### Key concept
Each row defines:
- name
- limit range
- comparison mode

### Example use case
- Multi-channel validation
- Grouped measurements

---

## String Check Step

Validates string outputs against expected values.

### Supported modes
- `exact` and `contains`

### Example use case
- Identifiers
- Firmware versions
- Serial numbers

---

## Waveform Limit Step

Validates waveform data using upper and lower masks.

### Input structure
- x/y waveform data
- upper mask
- lower mask

### Example use case
- Signal integrity checks
- Oscilloscope captures
- Pattern validation

---

## Message Pop-up Step

Pauses execution and requests user interaction.

### Features
- configurable buttons
- optional response box
- stores response in execution context

### Example use case
- operator confirmation
- manual selection of execution path

---

## Flow Control Step

Enables dynamic branching of execution flow.

### Concept
Returns an index or condition that maps to `next_steps`.

### Behavior
- routes execution to different steps
- can terminate sequences
- enables conditional pipelines

### Example use case
- UI-driven workflows
- conditional test execution
- dynamic sequencing

---

## Summary

Step types are the core building blocks of PyTestFlow.

They define:
- how data is produced
- how it is validated
- how execution flows through a sequence