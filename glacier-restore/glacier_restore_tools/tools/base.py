from kubiya_sdk.tools import Tool, Arg

class GlacierRestoreTool(Tool):
    def __init__(self, name, description, content, args=None, long_running=False):
        super().__init__(name, description, content, args, long_running)