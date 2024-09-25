import os
import subprocess
from kubiya_sdk.tools import Arg
from .base import GlacierRestoreTool
from kubiya_sdk.tools.registry import tool_registry

GLACIER_RESTORE_PATH = os.environ.get('GLACIER_RESTORE_PATH', '/path/to/glacier-restore')

glacier_restore_initiate = GlacierRestoreTool(
    name="glacier_restore_initiate",
    description="Initiate a restore request for a Glacier object",
    content=f"""
import subprocess

def run_glacier_restore(bucket, key, days):
    cmd = ['{GLACIER_RESTORE_PATH}', 'initiate-restore', bucket, key, str(days)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")

run_glacier_restore(bucket, key, days)
    """,
    args=[
        Arg(name="bucket", type="str", description="Name of the S3 bucket", required=True),
        Arg(name="key", type="str", description="Key of the Glacier object to restore", required=True),
        Arg(name="days", type="int", description="Number of days to keep the restored copy", required=True),
    ],
    long_running=True,
)

glacier_restore_status = GlacierRestoreTool(
    name="glacier_restore_status",
    description="Check the restore status of a Glacier object",
    content=f"""
import subprocess

def check_restore_status(bucket, key):
    cmd = ['{GLACIER_RESTORE_PATH}', 'check-status', bucket, key]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")

check_restore_status(bucket, key)
    """,
    args=[
        Arg(name="bucket", type="str", description="Name of the S3 bucket", required=True),
        Arg(name="key", type="str", description="Key of the Glacier object to check", required=True),
    ],
)

tool_registry.register("glacier-restore", glacier_restore_initiate)
tool_registry.register("glacier-restore", glacier_restore_status)