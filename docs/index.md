# PyTestFlow Documentation

PyTestFlow is a lightweight framework for building structured, step-based execution pipelines with support for validation, user interaction, and dynamic flow control.

---

## Core concepts

### Steps
Steps are the fundamental building blocks of PyTestFlow.

Each step is a Python function wrapped by a decorator that defines its behavior and validation logic.

Examples include:
- numeric validation steps
- pass/fail checks
- string comparisons
- waveform validation
- user interaction steps

---

### TestSequence
A TestSequence defines an ordered execution pipeline composed of:

- `setup_steps`: initialization phase
- `main_steps`: core execution logic
- `cleanup_steps`: teardown phase

Sequences are executed sequentially unless modified by flow control steps.

---

### Context (`ptf_context`)
PyTestFlow provides a shared runtime context:

- `globals`: global execution state
- `locals`: step-level stored values
- `results`: step outputs
- `current_step`: reference to the running step

This enables state sharing between steps without explicit parameter passing.

---

### Flow Control
Flow control steps allow dynamic branching of execution.

They can:
- redirect execution to different steps
- terminate sequences
- implement conditional pipelines


## Included example sequences

After installation, PyTestFlow provides a set of ready-to-run example sequences located in the `test_sequences/` directory.

These examples demonstrate the main framework capabilities and are designed to be:
- easy to run
- easy to modify
- representative of real usage patterns

---

### Default execution scope

By default, PyTestFlow only discovers and executes sequences located inside the `test_sequences/` directory.

This design choice ensures:
- clear separation between framework code and executable workflows
- predictable discovery of test sequences
- controlled execution scope in project environments

Custom execution sources can be configured if needed, but `test_sequences/` is the default entry point.

---

### Available example categories

- **Basic sequence usage**
  → Simple linear execution of steps without branching

- **Step type quickstart**
  → Overview of all available step types in a single sequence

- **Message box and flow control**
  → User interaction combined with dynamic execution branching

- **Flow control patterns**
  → Conditional execution paths driven by runtime state

---

### How to use examples

Each sequence can be executed directly after installation.

They are intentionally minimal and self-contained to serve as:
- learning material
- reference templates
- starting points for custom workflows