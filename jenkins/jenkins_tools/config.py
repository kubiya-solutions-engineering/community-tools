import os
import jenkins
from kubiya import Tool, tool, arg

class ConfigTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def get_version(self):
        """Get the version of Jenkins"""
        version = self.client.get_version()
        return f"Jenkins version: {version}"

    @tool
    def get_info(self):
        """Get general information about the Jenkins instance"""
        info = self.client.get_info()
        return {
            'mode': info['mode'],
            'node_description': info['nodeDescription'],
            'num_executors': info['numExecutors'],
            'quieting_down': info['quietingDown']
        }

    # Add more methods for other config-related operations