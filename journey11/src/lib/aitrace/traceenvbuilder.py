from typing import Dict
from journey11.src.interface.envbuilder import EnvBuilder
from journey11.src.lib.aitrace.trace import Trace


class TraceEnvBuilder(EnvBuilder):
    _context: Dict
    _trace: Trace

    def __init__(self,
                 context: Dict):
        self._context = context
        self._trace = None
        return

    def execute(self,
                purge: bool) -> None:
        """
        Execute actions to build the element of the environment owned by this builder
        :return: None: Implementation should throw and exception to indicate failure
        """
        self._trace = Trace(session_uuid=self._context[EnvBuilder.EnvSessionUUID])
        self._context[EnvBuilder.TraceContext] = self._trace
        self._trace.log().info("Invoked : {}".format(str(self)))
        return

    def uuid(self) -> str:
        """
        The immutable UUID of this build phase. This should be fixed at the time of coding as it is
        used in the environment factory settings to sequence build stages
        :return: immutable UUID
        """
        return "f13b6ca716bc481aa7d90979681e29cd"

    def __str__(self) -> str:
        return "Trace Logging Builder - Id: {}".format(self.uuid())

    def __repr__(self):
        return self.__str__()
