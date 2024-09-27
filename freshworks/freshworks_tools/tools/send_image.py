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

# Set environment variable
export GRAFANA_URL=$grafana_dashboard_url
echo "GRAFANA_URL: $GRAFANA_URL"

# Run the Python script to generate the Grafana render URL
python -c '
import os
from urllib.parse import urlparse, parse_qs

def generate_grafana_render_url(grafana_dashboard_url):
    print(f"Received Grafana URL: {grafana_dashboard_url}")  # Print the input URL for debugging
    # Parse the Grafana dashboard URL
    parsed_url = urlparse(grafana_dashboard_url)
    path_parts = parsed_url.path.strip("/").split("/")

    try:
        # Check if the path contains the expected segments
        if len(path_parts) >= 3 and path_parts[0] == "d":
            dashboard_uid = path_parts[1]
            dashboard_slug = path_parts[2]
        else:
            raise ValueError("URL path does not have the expected format '/d/{uid}/{slug}'")

        # Extract query parameters, if any
        query_params = parse_qs(parsed_url.query)
        org_id = query_params.get("orgId", ["1"])[0]  # Default to '1' if not present

        # Construct the render URL
        render_url = f"{parsed_url.scheme}://{parsed_url.netloc}/render/d/{dashboard_uid}/{dashboard_slug}?orgId={org_id}"
        return render_url
    except (IndexError, ValueError) as e:
        print(f"Invalid Grafana dashboard URL: {str(e)}")
        exit(1)

# Access the environment variable
grafana_dashboard_url = os.environ.get("GRAFANA_URL")

# Print the received URL for debugging
print(f"Debug: Received URL -> {grafana_dashboard_url}")

render_url = generate_grafana_render_url(grafana_dashboard_url)
print(render_url)
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
