from __future__ import annotations

import os
from typing import Iterator

import yaml


def make_action_docs(path: str, owner: str, version: str = "main") -> Iterator[str]:
    with open(path, encoding="utf-8") as f:
        action = yaml.safe_load(f)
    yield from _make_title(action["name"])
    yield from _make_description(action["description"])
    yield from _make_runs(action["runs"])
    if "inputs" in action:
        yield from _make_inputs(action.get("inputs", {}))
    if "outputs" in action:
        yield from _make_outputs(action.get("outputs", {}))
    yield from _make_usage(owner, path, version, action.get("inputs", {}))


def _make_title(name: str) -> Iterator[str]:
    """Create the Markdown heading for a command."""
    yield f"# {name}"
    yield ""


def _make_description(description: str) -> Iterator[str]:
    yield f"{description}"
    yield ""


def _make_runs(runs: dict) -> Iterator[str]:
    using = runs.get("using", "")
    yield f"This action is a {using} action."
    yield ""


def _make_inputs(inputs: dict) -> Iterator[str]:
    yield from _make_table_inputs(inputs)


def _make_outputs(outputs: dict) -> Iterator[str]:
    yield from _make_table_outputs(outputs)


def _make_env() -> Iterator[str]:
    yield ""


def _make_usage(owner: str, action_file: str, version: str, inputs: dict) -> Iterator[str]:
    usage_rows = [_format_usage_row(option, inputs[option]) for option in inputs]
    yield "## Usage"
    yield ""
    yield "```yaml"
    yield "name: Example usage"
    yield "on: push"
    yield "jobs:"
    yield "  example_job:"
    yield "    runs-on: ubuntu-latest"
    yield "    steps:"
    yield f"      - uses: {owner}/{os.path.splitext(os.path.basename(action_file))[0]}@{version}"
    if usage_rows:
        yield "         with:"
        yield from usage_rows
    yield "```"
    yield ""


def _format_usage_row(name: str, input: dict) -> str:
    """Format usage string for input."""
    default = input.get("default", "")
    optional_str = ""
    if not input.get("required", False):
        optional_str = " # optional"
    return f"           {name}: {default}{optional_str}"


def _make_table_inputs(input: dict) -> Iterator[str]:
    """Create the table style input options description."""

    option_rows = [_format_table_inputs_row(option, input[option]) for option in input]

    yield "## Inputs"
    yield ""
    yield "| Input | Description | Default |"
    yield "| ----- | ----------- | ------- |"
    yield from option_rows
    yield ""


def _format_table_inputs_row(name: str, input: dict) -> str:
    """Format a single row of the table."""
    required = input.get("required", False)
    required_str = "required" if required else "optional"
    description = input.get("description", "")
    default = input.get("default", "")
    return f"| {name} | [{required_str}] {description} | `{default}` |"


def _make_table_outputs(outputs: dict) -> Iterator[str]:
    """Create the table style output options description."""

    option_rows = [_format_table_outputs_row(option, outputs[option]) for option in outputs]

    yield "## Outputs"
    yield ""
    yield "| Output | Description |"
    yield "| ------ | ----------- |"
    yield from option_rows
    yield ""


def _format_table_outputs_row(name: str, output: dict) -> str:
    """Format a single row of the table."""
    description = output.get("description", "")
    output.get("value", "")

    return f"| {name} | {description} |"
