import os
import jenkins
from kubiya import Tool, tool, arg

class NodeTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def list(self):
        """List all Jenkins nodes"""
        nodes = self.client.get_nodes()
        return [node['name'] for node in nodes]

    @tool
    def enable(self, node_name: arg(str, "Name of the node to enable")):
        """Enable a specific node"""
        self.client.enable_node(node_name)
        return f"Node {node_name} has been enabled"

    @tool
    def disable(self, node_name: arg(str, "Name of the node to disable")):
        """Disable a specific node"""
        self.client.disable_node(node_name)
        return f"Node {node_name} has been disabled"

    # Add more methods for other node-related operations