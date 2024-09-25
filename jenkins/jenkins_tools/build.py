import os
import jenkins
from kubiya import Tool, tool, arg

class BuildTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def list(self, job_name: arg(str, "Name of the job to list builds for")):
        """List builds for a specific job"""
        builds = self.client.get_job_info(job_name)['builds']
        return [{'number': b['number'], 'url': b['url']} for b in builds]

    @tool
    def stop(self, job_name: arg(str, "Name of the job"), build_number: arg(int, "Build number to stop")):
        """Stop a specific build"""
        self.client.stop_build(job_name, build_number)
        return f"Build {build_number} of job {job_name} has been stopped"

    # Add more methods for other build-related operations