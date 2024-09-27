from kubiya_sdk.tools import Tool

SLACK_ICON_URL = "https://a.slack-edge.com/80588/marketing/img/icons/icon_slack_hash_colored.png"

class FreshworksTool(Tool):
    def __init__(self, name, description, content, args, long_running=False, thread_context=False, mermaid_diagram=None):
        secrets = ["GRAFANA_API_KEY", "TOOLS_GH_TOKEN"]

        super().__init__(
            name=name,
            description=description,
            icon_url=SLACK_ICON_URL,
            type="python",
            content=content,
            args=args,
            secrets=secrets,
            long_running=long_running,
            mermaid_diagram=mermaid_diagram
        )