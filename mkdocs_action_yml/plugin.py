from __future__ import annotations

from typing import Any, Callable, Iterable, Iterator

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from ._docs import make_action_docs
from ._exceptions import MkDocsActionYmlException
from ._processing import replace_blocks


class ActionYmlExtension(Extension):
    """
    Replace blocks like the following:

    ::: mkdocs-action-yml
        :path: action.yml
        :owner: athackst
        :version: v0.1.1

    by Markdown documentation generated from the specified action.yml.
    """

    def extendMarkdown(self, md: Any) -> None:
        md.registerExtension(self)
        md.preprocessors.register(
            ActionYmlPreprocessor(md, replace_func=replace_command_docs), "actionyml", 142
        )


class ActionYmlPreprocessor(Preprocessor):
    def __init__(self, md: Any, replace_func: Callable[..., Iterable[str]]) -> None:
        super().__init__(md)
        self.replace_func = replace_func

    def run(self, lines: list[str]) -> list[str]:
        return list(
            replace_blocks(
                lines,
                title="mkdocs-action-yml",
                replace=self.replace_func,
            )
        )


def replace_command_docs(**options: Any) -> Iterator[str]:
    for option in ("path", "owner"):
        if option not in options:
            raise MkDocsActionYmlException(f"Option {option!r} is required")

    path = options["path"]
    owner = options["owner"]
    version = options.get("version", "main")

    return make_action_docs(path=path, owner=owner, version=version)


def makeExtension() -> Extension:
    return ActionYmlExtension()
