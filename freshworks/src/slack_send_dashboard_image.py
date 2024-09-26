from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import os
from urllib.parse import urlparse
import argparse

def send_dashboard_image_to_slack(grafana_dashboard_url):
    # Initialize Slack client
    client = WebClient(token=os.environ['SLACK_API_KEY'])

    # Parse the Grafana dashboard URL to extract UID and slug
    parsed_url = urlparse(grafana_dashboard_url)
    path_parts = parsed_url.path.strip('/').split('/')

    if 'd' in path_parts:
        d_index = path_parts.index('d')
        dashboard_uid = path_parts[d_index + 1]
        dashboard_slug = path_parts[d_index + 2] if len(path_parts) > d_index + 2 else ''
    else:
        print("Invalid Grafana dashboard URL")
        exit(1)

    # Construct the render URL using the provided Grafana dashboard URL
    render_url = f"{parsed_url.scheme}://{parsed_url.netloc}/render/d/{dashboard_uid}/{dashboard_slug}"

    # Set up headers for authentication (if needed)
    headers = {}
    GRAFANA_API_KEY = os.environ.get('GRAFANA_API_KEY')
    if GRAFANA_API_KEY:
        headers['Authorization'] = f"Bearer {GRAFANA_API_KEY}"

    # Get the image from Grafana
    response = requests.get(render_url, headers=headers)
    if response.status_code == 200:
        image_data = response.content
    else:
        print(f"Error fetching image from Grafana: {response.status_code} - {response.text}")
        exit(1)

    # Upload the image to Slack using files.upload
    try:
        response = client.files_upload(
            channels=os.environ['SLACK_CHANNEL_ID'],
            file=image_data,
            filename="dashboard.png",
            filetype="png",
            initial_comment="*Hey team!*\n\nHere’s an important update:",
            title="Important update image"
        )
        print(f"File uploaded successfully: {response['file']['id']}")

    except SlackApiError as e:
        print(f"Error uploading file to Slack: {e.response['error']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a Grafana dashboard image to Slack")
    parser.add_argument("grafana_dashboard_url", type=str, help="URL of the Grafana dashboard to capture and send")
    args = parser.parse_args()
    send_dashboard_image_to_slack(args.grafana_dashboard_url)