import os
import jenkins
from kubiya import Tool, tool, arg

class AuthTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def whoami(self):
        """Get information about the authenticated user"""
        user = self.client.get_whoami()
        return f"Authenticated as: {user['fullName']} ({user['absoluteUrl']})"

    # Add more methods for other auth-related operations