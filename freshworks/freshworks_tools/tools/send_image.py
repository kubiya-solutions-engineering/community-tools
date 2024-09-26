from kubiya_sdk.tools import Arg
from .base import FreshworksTool
from kubiya_sdk.tools.registry import tool_registry

slack_send_dashboard_image = FreshworksTool(
    name="slack_send_dashboard_image",
    description="Render a Grafana dashboard and send it as an image to a Slack channel",
    content="""
#!/bin/bash

# Function to install git
install_git() {
    apt-get update -qq > /dev/null && apt-get install -y -qq git > /dev/null
}

# Function to install pip dependencies
install_dependencies() {
    pip install -r requirements.txt
}

# Install git
install_git

# Set variables
REPO_DIR="community-tools"
REPO_BRANCH="slackimage"  # Change this to the desired branch
GIT_ORG="kubiya-solutions-engineering"
REPO_NAME="community-tools"
TOOLS_GH_TOKEN="${TOOLS_GH_TOKEN}"  # Ensure this environment variable is set

# Clone repository if not already cloned
if [ ! -d "$REPO_DIR" ]; then
    git clone -b "$REPO_BRANCH" https://"$TOOLS_GH_TOKEN"@github.com/"$GIT_ORG"/"$REPO_NAME".git "$REPO_DIR"
else
    git clone --branch "$REPO_BRANCH" "https://$TOOLS_GH_TOKEN@github.com/$GIT_ORG/$REPO_NAME.git" "$REPO_DIR" > /dev/null
fi

# Change to the repository directory
cd "$REPO_DIR"
cd freshworks
cd src

# Install pip dependencies
install_dependencies

# Run the Python script
exec python slack_send_dashboard_image.py --grafana_dashboard_url "{{ .grafana_dashboard_url }}"
""",
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
tool_registry.register("freshworks", slack_send_dashboard_image)
