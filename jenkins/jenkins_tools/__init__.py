from kubiya import Tool, tool

from .job import JobTool
from .build import BuildTool
from .node import NodeTool
from .plugin import PluginTool
from .queue import QueueTool
from .user import UserTool
from .auth import AuthTool
from .config import ConfigTool

class JenkinsTools(Tool):
    job = JobTool()
    build = BuildTool()
    node = NodeTool()
    plugin = PluginTool()
    queue = QueueTool()
    user = UserTool()
    auth = AuthTool()
    config = ConfigTool()

jenkins = tool(JenkinsTools())