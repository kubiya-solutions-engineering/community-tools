# Jenkins Tools Module for Kubiya SDK

This module provides a comprehensive set of tools for interacting with Jenkins using the Jenkins API via the Kubiya SDK. These tools are designed to be stateless and easily discoverable by the Kubiya engine, allowing for dynamic execution in various environments with different Jenkins configurations.

## Tools Overview

1. **Job**: Manages Jenkins jobs (create, list, view, build, delete)
2. **Build**: Manages Jenkins builds (list, view, stop)
3. **Node**: Manages Jenkins nodes (list, view, enable, disable)
4. **Plugin**: Manages Jenkins plugins (list, install, uninstall)
5. **Queue**: Manages Jenkins build queue (list, cancel)
6. **User**: Manages Jenkins users (create, list, delete)
7. **Auth**: Handles Jenkins authentication
8. **Config**: Manages Jenkins configuration

## Configuration

This module uses environment variables for configuration:

- `JENKINS_URL`: The URL of your Jenkins instance
- `JENKINS_USER`: The username for Jenkins authentication
- `JENKINS_TOKEN`: The API token for Jenkins authentication

Ensure these environment variables are set before using the module.

## Usage

To use these tools in your Kubiya SDK workflows, first add this module as a source in your Teammate Environment. Then, you can use the tools in your workflows like this: