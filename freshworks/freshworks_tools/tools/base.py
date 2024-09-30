from kubiya_sdk.tools.models import Tool, Arg, FileSpec
import json

SLACK_ICON_URL = "https://a.slack-edge.com/80588/marketing/img/icons/icon_slack_hash_colored.png"

class SlackTool(Tool):
    def __init__(self, name, description, action, args, long_running=False, mermaid_diagram=None):
        env = ["SLACK_API_TOKEN", "GRAFANA_API_KEY", "TOOLS_GH_TOKEN"]
        
        arg_names_json = json.dumps([arg.name for arg in args])
        
        script_content = f"""
import subprocess
import sys
import os
import json
import requests

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install slack_sdk
install('slack_sdk')

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def serialize_slack_response(obj, max_depth=10):
    def _serialize(o, depth):
        if depth > max_depth:
            return str(o)
        if isinstance(o, (str, int, float, bool, type(None))):
            return o
        if isinstance(o, (list, tuple)):
            return [_serialize(i, depth + 1) for i in o]
        if isinstance(o, dict):
            return {{k: _serialize(v, depth + 1) for k, v in o.items()}}
        return str(o)
    
    return _serialize(obj, 0)

def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image. Status code: {{response.status_code}}")
        exit(1)

def execute_slack_action(token, action, **kwargs):
    client = WebClient(token=token)
    try:
        if action == "{action}":
            response = getattr(client, action)(**kwargs)
            return serialize_slack_response(response.data)
        else:
            raise ValueError(f"Unsupported action: {{action}}")
    except SlackApiError as e:
        print(f"Error executing Slack action: {{e}}")
        raise

if __name__ == "__main__":
    token = os.environ["SLACK_API_TOKEN"]
    
    arg_names = {arg_names_json}
    args = {{}}
    for arg in arg_names:
        if arg in os.environ:
            args[arg] = os.environ[arg]

    # Generate the Grafana render URL
    grafana_dashboard_url = args.get("grafana_dashboard_url")
    render_url = None
    if grafana_dashboard_url:
        from urllib.parse import urlparse, parse_qs
        
        parsed_url = urlparse(grafana_dashboard_url)
        path_parts = parsed_url.path.strip("/").split("/")
        org_id = parse_qs(parsed_url.query).get("orgId", ["1"])[0]

        if len(path_parts) >= 3 and path_parts[0] == "d":
            dashboard_uid = path_parts[1]
            dashboard_slug = path_parts[2]
            render_url = f"{{parsed_url.scheme}}://{{parsed_url.netloc}}/render/d/{{dashboard_uid}}/{{dashboard_slug}}?orgId={{org_id}}"

    # Download the rendered image
    image_file_path = "/tmp/rendered_image.png"
    download_image(render_url, image_file_path)

    # Send the image to Slack
    slack_channel_id = args.get("channel")
    if slack_channel_id:
        args["channels"] = slack_channel_id  # Slack API expects 'channels' for file uploads
        args["file"] = image_file_path
        args["title"] = "Grafana Rendered Dashboard"

        result = execute_slack_action(token, "{action}", **args)
        print(json.dumps(result, indent=2))
"""
        super().__init__(
            name=name,
            description=description,
            icon_url=SLACK_ICON_URL,
            type="docker",
            image="python:3.11",
            content="python /tmp/script.py",
            args=args,
            secrets=env,
            long_running=long_running,
            mermaid=mermaid_diagram,
            with_files=[
                FileSpec(
                    destination="/tmp/script.py",
                    content=script_content,
                )
            ],
        )