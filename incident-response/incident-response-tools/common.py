from kubiya_sdk.tools.models import FileSpec


# This is the profile that will be used to authenticate with AWS by default
# In a Kubiya managed teammate, this environment variable will be set automatically
# If you're using this in a local environment, make sure to set it on your shell
COMMON_ENV = [
    "FSAPI_PROD",
    "SLACK_API_TOKEN",
    "SLACK_CHANNEL_ID",
    "SLACK_THREAD_TS",
    "AZURE_TENANT_ID",
    "AZURE_CLIENT_ID",
    "AZURE_CLIENT_SECRET",
    "PD_API_KEY",
    "KUBIYA_USER_EMAIL",
    "TOOLS_GH_TOKEN"
]