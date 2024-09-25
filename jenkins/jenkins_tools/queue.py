import os
import jenkins
from kubiya import Tool, tool, arg

class QueueTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def list(self):
        """List all items in the Jenkins build queue"""
        queue = self.client.get_queue_info()
        return [{'id': item['id'], 'name': item['task']['name']} for item in queue]

    @tool
    def cancel(self, item_id: arg(int, "ID of the queue item to cancel")):
        """Cancel a specific item in the build queue"""
        self.client.cancel_queue(item_id)
        return f"Queue item {item_id} has been cancelled"

    # Add more methods for other queue-related operations