from kubiya_sdk.tools.models import Tool
from .common import COMMON_ENV

class IncidentResponseTool(Tool):
    def __init__(self, name, description, content, args, long_running=False, mermaid_diagram=None):
        super().__init__(
            name=name,
            description=description,
            type="docker",
            image="python:slim",
            content=content,
            args=args,
            requirements=["requests"],
            env=COMMON_ENV,
            long_running=long_running,
            mermaid=mermaid_diagram
        )