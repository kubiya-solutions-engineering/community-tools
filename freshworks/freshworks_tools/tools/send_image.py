from kubiya_sdk.tools import Arg
from .base import FreshworksTool
from kubiya_sdk.tools.registry import tool_registry

get_grafana_render_url = FreshworksTool(
    name="get_grafana_render_url",
    description="Generate the render URL for a Grafana dashboard",
    content="""
        # Debug: Print all environment variables to check if grafana_dashboard_url is being set
        echo "Environment variables:"
        printenv

        # Debug: Print the passed argument to ensure it's available
        if [ -z $grafana_dashboard_url ]; then
            echo "Error: 'grafana_dashboard_url' is not set or empty"
        else
            echo "Passed grafana_dashboard_url: $grafana_dashboard_url"
        fi
        
        # Set environment variables
        export GRAFANA_URL=$grafana_dashboard_url
        export SLACK_API_TOKEN=$SLACK_API_TOKEN  # Ensure the Slack API token is available
        export SLACK_CHANNEL_ID=$SLACK_CHANNEL_ID  # Ensure the Slack Channel ID is available
        echo "GRAFANA_URL: $GRAFANA_URL"
        
        # Run the Python script to generate the Grafana render URL and send it to Slack
        python -c '
    import os
    import requests
    from urllib.parse import urlparse, parse_qs
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    def generate_grafana_render_url(grafana_dashboard_url):
        # Parse the Grafana dashboard URL
        parsed_url = urlparse(grafana_dashboard_url)
        path_parts = parsed_url.path.strip("/").split("/")

        try:
            if len(path_parts) >= 3 and path_parts[0] == "d":
                dashboard_uid = path_parts[1]
                dashboard_slug = path_parts[2]
            else:
                raise ValueError("URL path does not have the expected format '/d/{uid}/{slug}'")

            query_params = parse_qs(parsed_url.query)
            org_id = query_params.get("orgId", ["1"])[0]  # Default to '1' if not present

            render_url = f"{parsed_url.scheme}://{parsed_url.netloc}/render/d/{dashboard_uid}/{dashboard_slug}?orgId={org_id}"
            return render_url
        except (IndexError, ValueError) as e:
            print(f"Invalid Grafana dashboard URL: {str(e)}")
            exit(1)

    def download_image(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            exit(1)

    def send_image_to_slack(image_data, channel_id, token):
        client = WebClient(token=token)
        try:
            response = client.files_upload(
                channels=channel_id,
                file=image_data,
                title="Grafana Rendered Dashboard"
            )
            print(f"Image sent to Slack successfully: {response['file']['permalink']}")
        except SlackApiError as e:
            print(f"Error sending image to Slack: {e.response['error']}")

    # Access environment variables
    grafana_dashboard_url = os.environ.get("GRAFANA_URL")
    slack_token = os.environ.get("SLACK_API_TOKEN")
    slack_channel_id = os.environ.get("SLACK_CHANNEL_ID")

    # Generate the render URL
    render_url = generate_grafana_render_url(grafana_dashboard_url)
    print(f"Generated render URL: {render_url}")

    # Download the rendered image
    image_data = download_image(render_url)

    # Send the image to Slack
    send_image_to_slack(image_data, slack_channel_id, slack_token)
    ' """,
    args=[
        Arg(
            name="grafana_dashboard_url",
            type="str",
            description="URL of the Grafana dashboard",
            required=True
        )
    ],
)

# Register the updated tool
tool_registry.register("freshworks", get_grafana_render_url)
