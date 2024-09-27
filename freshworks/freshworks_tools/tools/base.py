from kubiya_sdk.tools import Tool

SLACK_ICON_URL = "https://a.slack-edge.com/80588/marketing/img/icons/icon_slack_hash_colored.png"

class FreshworksTool(Tool):
    def __init__(self, name, description, content, args, long_running=False, thread_context=False, mermaid_diagram=None):
        env = ["SLACK_API_TOKEN"]
        if thread_context:
            env.extend(["SLACK_THREAD_TS", "SLACK_CHANNEL_ID"])
        secrets = ["GRAFANA_API_KEY", "TOOLS_GH_TOKEN"]

        super().__init__(
            name=name,
            description=description,
            icon_url=SLACK_ICON_URL,
            type="docker",
            image="python:3.12-slim",
            content=content,
            args=args,
            env=env,
            secrets=secrets,
            long_running=long_running,
            requirements=["slack_sdk"],
            mermaid_diagram=mermaid_diagram
        )