from kubiya_sdk.tools import Arg
from .base import FreshworksTool
from kubiya_sdk.tools.registry import tool_registry

# Slack Upload File Tool
slack_upload_file = FreshworksTool(
    name="slack_upload_file",
    description="Upload a rendered Grafana image to a Slack channel",
    action="files_upload_v2",
    args=[
        Arg(name="grafana_dashboard_url", type="str", description="The URL of the Grafana dashboard", required=True),
        Arg(name="channel", type="str", description="The channel to send the image to", required=True),
    ],
)

# Register the updated tool
tool_registry.register("freshworks", slack_upload_file)
