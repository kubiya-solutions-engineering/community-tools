import jenkins
from kubiya import Tool, tool, arg

class JobTool(Tool):
    def __init__(self):
        self.client = jenkins.Jenkins(
            os.environ['JENKINS_URL'],
            username=os.environ['JENKINS_USER'],
            password=os.environ['JENKINS_TOKEN']
        )

    @tool
    def list(self):
        """List all Jenkins jobs"""
        jobs = self.client.get_jobs()
        return [job['name'] for job in jobs]

    @tool
    def build(self, job_name: arg(str, "Name of the job to build")):
        """Trigger a build for a specific job"""
        self.client.build_job(job_name)
        return f"Build triggered for job: {job_name}"

    # Add more methods for other job-related operations