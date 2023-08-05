from glob import glob
import re
import shlex
from typing import (
    Dict,
    Iterable,
    MutableMapping,
    Type,
    TYPE_CHECKING,
)
from .base import PoeTask

if TYPE_CHECKING:
    from ..config import PoeConfig
    from ..context import RunContext

_GLOBCHARS_PATTERN = re.compile(r".*[\*\?\[]")


class CmdTask(PoeTask):
    """
    A task consisting of a reference to a shell command
    """

    content: str

    __key__ = "cmd"
    __options__: Dict[str, Type] = {}

    def _handle_run(
        self,
        context: "RunContext",
        extra_args: Iterable[str],
        env: MutableMapping[str, str],
    ) -> int:
        cmd = self._resolve_args(context, extra_args, env)
        self._print_action(" ".join(cmd), context.dry)
        return context.get_executor(env).execute(cmd)

    def _resolve_args(
        self,
        context: "RunContext",
        extra_args: Iterable[str],
        env: MutableMapping[str, str],
    ):
        # Parse shell command tokens
        cmd_tokens = shlex.split(
            self._resolve_envvars(self.content, context, env),
            comments=True,
            posix=not self._is_windows,
        )
        extra_args = [
            self._resolve_envvars(token, context, env) for token in extra_args
        ]
        # Resolve any glob pattern paths
        result = []
        for cmd_token in (*cmd_tokens, *extra_args):
            if _GLOBCHARS_PATTERN.match(cmd_token):
                # looks like a glob path so resolve it
                result.extend(glob(cmd_token, recursive=True))
            else:
                result.append(cmd_token)
        # Finally add the extra_args from the invoking command and we're done
        return result
