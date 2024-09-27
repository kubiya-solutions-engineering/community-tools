from kubiya_sdk.tools import Arg
from .base import FreshworksTool
from kubiya_sdk.tools.registry import tool_registry


get_grafana_render_url = FreshworksTool(
    name="get_grafana_render_url",
    description="Generate the render URL for a Grafana dashboard",
    content="""python -c '
import sys
from urllib.parse import urlparse

def generate_grafana_render_url(grafana_dashboard_url):
    # Parse the Grafana dashboard URL to extract UID and slug
    parsed_url = urlparse(grafana_dashboard_url)
    path_parts = parsed_url.path.strip("/").split("/")

    try:
        # Ensure that the URL contains the 'd' segment and extract necessary parts
        if "d" in path_parts:
            d_index = path_parts.index("d")
            dashboard_uid = path_parts[d_index + 1]
            dashboard_slug = path_parts[d_index + 2] if len(path_parts) > d_index + 2 else ""
        else:
            raise ValueError("Invalid Grafana dashboard URL")

        # Construct the render URL using the provided Grafana dashboard URL
        render_url = f"{parsed_url.scheme}://{parsed_url.netloc}/render/d/{dashboard_uid}/{dashboard_slug}?orgId=1"
        return render_url
    except (IndexError, ValueError) as e:
        print("Invalid Grafana dashboard URL:", str(e))
        exit(1)

# Access the first argument passed to the Python script
grafana_dashboard_url = sys.argv[1]

render_url = generate_grafana_render_url(grafana_dashboard_url)
print(render_url)
' "$grafana_dashboard_url" """,
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
