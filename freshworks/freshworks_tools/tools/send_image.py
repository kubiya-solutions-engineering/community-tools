from kubiya_sdk.tools import Arg
from .base import FreshworksTool
from kubiya_sdk.tools.registry import tool_registry


get_grafana_render_url = FreshworksTool(
    name="get_grafana_render_url",
    description="Generate the render URL for a Grafana dashboard",
    content="""python -c '
import os
from urllib.parse import urlparse
import argparse

def generate_grafana_render_url(grafana_dashboard_url):
    # Parse the Grafana dashboard URL to extract UID and slug
    parsed_url = urlparse(grafana_dashboard_url)
    path_parts = parsed_url.path.strip("/").split("/")

    if "d" in path_parts:
        d_index = path_parts.index("d")
        dashboard_uid = path_parts[d_index + 1]
        dashboard_slug = path_parts[d_index + 2] if len(path_parts) > d_index + 2 else ""
    else:
        print("Invalid Grafana dashboard URL")
        exit(1)

    # Construct the render URL using the provided Grafana dashboard URL
    render_url = f"{parsed_url.scheme}://{parsed_url.netloc}/render/d/{dashboard_uid}/{dashboard_slug}"
    return render_url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the render URL for a Grafana dashboard")
    parser.add_argument("grafana_dashboard_url", type=str, help="URL of the Grafana dashboard to generate the render URL for")
    args = parser.parse_args()
    render_url = generate_grafana_render_url(os.environ["grafana_dashboard_url"])
    print(render_url)
'""",
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