import os
import jenkins
from kubiya import Tool, tool, arg

class PluginTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def list(self):
        """List all installed Jenkins plugins"""
        plugins = self.client.get_plugins_info()
        return [{'name': p['shortName'], 'version': p['version']} for p in plugins]

    # Note: Installing and uninstalling plugins via API is not directly supported by python-jenkins
    # You might need to implement these using custom HTTP requests or Jenkins CLI

    # Add more methods for other plugin-related operations