# Starter Kit for Custom Tools

Welcome to the Starter Kit for creating custom tools! This guide will help you set up and customize three essential files to fit your use cases:

1. [Tool YAML](#tool-yaml)
2. [Script File](#script-file)
3. [Terraform.tfvars](#terraformtfvars)

## Tool YAML

The Tool YAML file defines the configuration and behavior of your tool. Here is a template you need to edit:

```yaml
tools:
  - name: list_s3_buckets # 1. Change this to the name of your tool
    image: python:3.11
    description: "List all S3 buckets in your AWS account using the specified AWS CLI profile." # 2. Update the description to fit your tool's purpose
    alias: list-s3-buckets # 3. Change this alias to a short, easy-to-type name for your tool
    content: |
      # Set default values for environment variables
      REPO_URL="${REPO_URL:-https://github.com/your-repo/your-project}" # 4. Update the URL to point to your repository
      REPO_NAME="${REPO_NAME:-your-project}" # 4. Change this to the name of your repository
      SOURCE_CODE_DIR="${SOURCE_CODE_DIR:-src/tool-example}" # 4. Specify the directory where your source code is located
      REPO_BRANCH="${REPO_BRANCH:-main}" # 4. Set this to the branch you want to use (e.g., main, dev)
      REPO_DIR="${REPO_DIR:-$REPO_NAME}" # 4. Directory name for cloning the repo
      BIN_DIR="${BIN_DIR:-/usr/local/bin}"
      APT_CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"
      PIP_CACHE_DIR="${PIP_CACHE_DIR:-/var/cache/pip}"

      # Create cache directories
      mkdir -p "$APT_CACHE_DIR"
      mkdir -p "$BIN_DIR"
      mkdir -p "$PIP_CACHE_DIR"

      install_git() {
        apt-get update -qq > /dev/null && apt-get install -y -qq git > /dev/null
        # 4. Add more dependencies here if needed
      }

      install_pip_dependencies() {
        export PIP_CACHE_DIR="$PIP_CACHE_DIR"
        pip install boto3 --cache-dir "$PIP_CACHE_DIR" --quiet > /dev/null
      }

      # Install git
      install_git

      # Install pip dependencies
      install_pip_dependencies

      # Clone repository if not already cloned
      if [ ! -d "$REPO_DIR" ]; then
        if [ -n "$GH_TOKEN" ]; then
          GIT_ASKPASS_ENV=$(mktemp)
          chmod +x "$GIT_ASKPASS_ENV"
          echo -e "#!/bin/sh\nexec echo \$GH_TOKEN" > "$GIT_ASKPASS_ENV"
          GIT_ASKPASS="$GIT_ASKPASS_ENV" git clone --branch "$REPO_BRANCH" "https://$GH_TOKEN@$(echo $REPO_URL | sed 's|https://||')" "$REPO_DIR" > /dev/null
          rm "$GIT_ASKPASS_ENV"
        else
          git clone --branch "$REPO_BRANCH" "$REPO_URL" "$REPO_DIR" > /dev/null
        fi
      fi

      # cd into the cloned repo
      cd "${REPO_DIR}/${SOURCE_CODE_DIR}"

      # Run the script
      export PYTHONPATH="${PYTHONPATH}:/${REPO_DIR}/${SOURCE_CODE_DIR}"
      exec python list_s3_buckets.py --profile "{{ .profile }}" # 4. Update this to match the script's location and name within your repository
    args:
      - name: profile # 5. Define the command-line arguments for your script
        description: 'AWS CLI profile name' # 5. Update the description to explain what the argument is
        required: true
    env:
      - AWS_PROFILE # 6. List environment variables required by your tool
    with_files: # 7. Only include this section if your tool requires specific files, such as AWS credentials
      - source: $HOME/.aws/credentials
        destination: /root/.aws/credentials
```

Customization Steps:
Name: Change the name of the tool to something unique and descriptive.
Description: Update the description to explain what the tool does.
Alias: Change the alias to a short, memorable name for the tool.
Within content:
Repo URL: Set the URL of your repository.
Repo Name: Change to the name of your repository.
Source Code Directory: Specify the directory containing your source code.
Repo Branch: Set to the branch you want to use (e.g., main, dev).
Repo Directory: Directory name for cloning the repository.
Dependencies: Add any additional dependencies needed in the install_git function.
Exec Python: Update the command to run your specific script within the cloned repository.
Args: Define the command-line arguments for your script, including names and descriptions.
Env: List any environment variables your tool requires.
With Files: Only include this section if your tool needs to access specific files, like AWS credentials.

Script File
The script file contains the logic for your tool. Here's an example script for listing S3 buckets:

```python
import boto3
import argparse

def list_s3_buckets(profile_name):
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client('s3')
    response = s3_client.list_buckets()
    print("Buckets:")
    for bucket in response['Buckets']:
        print(f"  {bucket['Name']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List all S3 buckets.')
    parser.add_argument('--profile', type=str, required=True, help='AWS CLI profile name')
    args = parser.parse_args()
    list_s3_buckets(args.profile)
```

Customization Steps:
Functionality: Modify the script to implement the functionality you need.
Arguments: Add or change command-line arguments as required by your tool.
Dependencies: Ensure any additional dependencies are installed in the Tool YAML file.
Terraform.tfvars
The terraform.tfvars file contains configuration variables for your Terraform setup:

```hcl
agent_name         = "S3 Bucket Lister"
kubiya_runner      = "nats"
agent_description  = "This teammate handles the listing of all S3 buckets in your AWS account using the specified AWS CLI profile."
agent_instructions = <<EOT
You are an intelligent agent designed to help manage the lifecycle of infrastructure resources.

** You have access only to the commands you see on this prompt **
EOT
llm_model          = "azure/gpt-4o"
agent_image        = "kubiya/base-agent:tools-v6"

// Terraform settings
store_tf_state_enabled = true

// **Approval settings**
// Do we need to enable the approval workflow? If yes, set it to true
// Approval workflow - When enabled, the agent will request approval from the approving users before applying the changes
// on the specified resources (e.g., creating, updating, or deleting resources) in a dedicated Slack channel.
// the approving users are the users who can approve the changes by reply to the agent message in the Slack channel.
approval_workflow_enabled = false
// Slack channel to send the approval request
approval_slack_channel = "#approval-channel"
// Array of users who can approve the changes
approving_users = ["user1@example.com", "user2@example.com"]

// Other settings
secrets      = []
integrations = ["aws", "slack", "github"]
// ACL for the agent - Users and groups who can access the agent
// Users group is a special group that includes all users
users  = ["user@example.com"]
groups = ["Admin", "Users"]
// Fetch all tools from the directory in the folder (resource-life-cycle/tools/*)
agent_tool_sources = ["https://github.com/your-repo/your-project/resource-lifecycle/tools/*"]
links              = []

// Environment variables
log_level        = "INFO"
grace_period     = "5h"
max_ttl          = "30d"
tf_modules_urls  = [] # Keep empty to auto generate TF code based on user requests
allowed_vendors  = ["aws"]
extension_period = "1w"

// Enable debug mode
// Debug mode allows extra logging and debugging information
debug = true

// dry run
// When enabled, the agent will not apply the changes but will show the changes that will be applied
dry_run = true
```

Customization Steps:
Agent Name: Change the agent_name to reflect the purpose of your tool.
Description: Update the agent_description and agent_instructions to describe your tool and its functionality.
Approval Workflow: Configure the approval settings as needed, including the Slack channel and approving users.
Integrations: List any integrations your tool needs (e.g., AWS, Slack, GitHub).
ACL: Specify the users and groups who can access the agent.
Environment Variables: Set any required environment variables.
Debug and Dry Run: Enable or disable debug mode and dry run as needed.