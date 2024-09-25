import os
import jenkins
from kubiya import Tool, tool, arg

class UserTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def list(self):
        """List all Jenkins users"""
        users = self.client.get_users()
        return [user['fullName'] for user in users]

    # Note: Creating and deleting users via API is not directly supported by python-jenkins
    # You might need to implement these using custom HTTP requests or Jenkins CLI

    # Add more methods for other user-related operations