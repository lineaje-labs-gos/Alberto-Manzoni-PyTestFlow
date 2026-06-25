# PyTestFlow

PyTestFlow is a Python test executive built on top of Prefect.
It turns decorated Python functions into traceable test steps and runs them in
ordered flows.

> Requires `prefect>=3.4` and Python 3.10+.

## Repositories

- Engine: https://github.com/Alberto-Manzoni/PyTestFlow
- Frontend: https://github.com/Alberto-Manzoni/PyTestFlow-FrontEnd

## Installation

```bash
python -m pip install pytestflow
```

### Init the workspace

```bash
pytestflow init
```

Set the environment variable as suggested from the CLI


## Usage

```bash
pytestflow start
```
Open the web gui at the url indicated by the CLI.



## Core concepts

- Steps are Prefect tasks defined using `@step` or specialized step decorators.
- A `TestSequence` is a Prefect flow that aggregates and executes multiple steps, tracking their states.
- `ptf_context` is a shared runtime context that provides access to `globals`, `locals`, `results`, and `current_step`.
- `SequentialProcessModel` orchestrates execution callbacks in a fixed lifecycle:
  `pre_uut -> main_sequence -> post_uut -> report -> database_logging`.
- The main output of the process model is stored in both `main_results` and `main_result` for backward compatibility.
