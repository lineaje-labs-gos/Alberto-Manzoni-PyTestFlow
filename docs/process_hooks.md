# Process Hooks (SequentialProcessModel)

Process hooks define the execution lifecycle callbacks used by the default `SequentialProcessModel`.

⚠️ Important:
These hooks are NOT a core requirement of PyTestFlow.

They are an implementation detail of the `SequentialProcessModel`.
Custom process models may define their own lifecycle, callbacks, or ignore hooks entirely.

---

## Lifecycle overview

The default execution model supports the following lifecycle stages:

- `pre_uut`
- `main_sequence`
- `post_uut`
- `report`
- `database_logging`

Each stage is mapped to a callback function.

---

## Default callback mapping

```python
DEFAULT_CALLBACKS = {
    "pre_uut": pre_uut_callback,
    "main_sequence": None,  # mandatory
    "post_uut": post_uut_callback,
    "report": report_callback_jinja,
    "database_logging": database_logging_callback,
}