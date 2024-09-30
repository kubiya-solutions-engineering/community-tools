from kubiya_sdk.tools import Arg
from .base import FreshworksTool
from kubiya_sdk.tools.registry import tool_registry

get_grafana_image_and_send_slack = FreshworksTool(
    name="get_grafana_image_and_send_slack",
    description="Generate the render URL for a Grafana dashboard, download the image, and send it to a Slack channel",
    content="""
    # Debug: Print all environment variables
    echo "Environment variables:"
    printenv

    # Debug: Print the passed arguments
    if [ -z $grafana_dashboard_url ]; then
        echo "Error: 'grafana_dashboard_url' is not set or empty"
    else
        echo "Passed grafana_dashboard_url: $grafana_dashboard_url"
    fi

    if [ -z $slack_channel ]; then
        echo "Error: 'slack_channel' is not set or empty"
    else
        echo "Passed slack_channel: $slack_channel"
    fi
    
    # Set environment variables
    export GRAFANA_URL=$grafana_dashboard_url
    export SLACK_CHANNEL=$slack_channel
    echo "GRAFANA_URL: $GRAFANA_URL"
    echo "SLACK_CHANNEL: $SLACK_CHANNEL"
    
    # Install required Python packages
    pip install requests slack_sdk

    # Run the Python script to generate the Grafana render URL, download the image, and send it to Slack
    python -c '
import os
import requests
from urllib.parse import urlparse, parse_qs
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json

def generate_grafana_render_url(grafana_dashboard_url):
    print(f"Received Grafana URL: {grafana_dashboard_url}")
    parsed_url = urlparse(grafana_dashboard_url)
    path_parts = parsed_url.path.strip("/").split("/")

    try:
        if len(path_parts) >= 3 and path_parts[0] == "d":
            dashboard_uid = path_parts[1]
            dashboard_slug = path_parts[2]
        else:
            raise ValueError("URL path does not have the expected format '/d/{uid}/{slug}'")

        query_params = parse_qs(parsed_url.query)
        org_id = query_params.get("orgId", ["1"])[0]

        render_url = f"{parsed_url.scheme}://{parsed_url.netloc}/render/d-solo/{dashboard_uid}/{dashboard_slug}?orgId={org_id}&from=now-1h&to=now&panelId=1&width=1000&height=500"
        return render_url
    except (IndexError, ValueError) as e:
        print(f"Invalid Grafana dashboard URL: {str(e)}")
        raise

def download_grafana_image(render_url, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(render_url, headers=headers)
    if response.status_code == 200:
        with open("grafana_dashboard.png", "wb") as f:
            f.write(response.content)
        print("Grafana dashboard image downloaded successfully")
        return "grafana_dashboard.png"
    else:
        print(f"Failed to download Grafana image. Status code: {response.status_code}")
        raise Exception("Failed to download Grafana image")

def send_slack_file(token, channel, file_path, initial_comment):
    client = WebClient(token=token)
    try:
        response = client.files_upload(
            channels=channel,
            file=file_path,
            initial_comment=initial_comment
        )
        return response
    except SlackApiError as e:
        print(f"Error sending file to Slack: {e}")
        raise

# Access environment variables
grafana_dashboard_url = os.environ.get("GRAFANA_URL")
slack_channel = os.environ.get("SLACK_CHANNEL")
slack_token = os.environ.get("SLACK_API_TOKEN")
grafana_api_key = os.environ.get("GRAFANA_API_KEY")

# Generate Grafana render URL
render_url = generate_grafana_render_url(grafana_dashboard_url)
print(f"Generated Grafana render URL: {render_url}")

# Download Grafana image
image_path = download_grafana_image(render_url, grafana_api_key)

# Send image to Slack
initial_comment = f"Grafana dashboard image from: {grafana_dashboard_url}"
slack_response = send_slack_file(slack_token, slack_channel, image_path, initial_comment)
print("Slack response:")
print(json.dumps(slack_response, indent=2))

# Clean up the downloaded image
os.remove(image_path)
print("Temporary image file removed")
' """,
    args=[
        Arg(
            name="grafana_dashboard_url",
            type="str",
            description="URL of the Grafana dashboard",
            required=True
        ),
        Arg(
            name="slack_channel",
            type="str",
            description="The Slack channel to send the message to",
            required=True
        )
    ],
)

# Register the updated tool
tool_registry.register("freshworks", get_grafana_image_and_send_slack)