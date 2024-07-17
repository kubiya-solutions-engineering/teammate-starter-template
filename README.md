# Introduction

Welcome to the teammate-starter-template! This guide will walk you through the steps to customize and deploy your own tool using this template.

## Steps to Get Started:

**Step 1: Clone the teammate-starter-template repo.**
   - Use the following command to clone the repository:
     ```sh
     git clone https://github.com/kubiya-solutions-engineering/teammate-starter-template.git
     ```

**Step 2: Replace the script in the `src` directory with your script.**
   - Ensure your script is placed in the `src` directory and remove the existing placeholder script.

**Step 3: Update the YAML in the `tool` directory to call your script.**
   - Open the `tool/content.sh` file and update it to call your script.
   - Update all necessary fields, such as `name`, `alias`, `description`, `arguments`, and `env`. If your script requires secrets that exist in Kubiya, bring them in here.

**Step 4: Update the `terraform.tfvars` file with agent info.**
   - Include details like description, instructions, and any necessary secrets or environment variables.

**Step 5: Run Terraform commands to initialize and apply your configuration.**
   - Initialize Terraform:
     ```sh
     terraform init
     ```
   - Apply the Terraform configuration:
     ```sh
     terraform apply
     ```
   - Test your setup to ensure everything is working correctly.
   - Once tested, share the updated repository with your team. They can clone the repo, run `terraform init` and `terraform apply` to set up the tool in their environment.

**Step 6: (If applicable) Add Python package dependencies.**
   - If your script is written in Python and requires additional packages, list them in the `requirements.txt` file in the root directory.
   - Install the packages using:
     ```sh
     pip install -r requirements.txt
     ```

Follow these steps to get your tool up and running using the teammate-starter-template. If you encounter any issues, refer to the documentation or reach out for support.





# Starter Kit for Custom Tools

The Starter Kit for creating custom tools! This guide will help you set up and customize three essential files to fit your use cases:

1. [Tool YAML](#tool-yaml)
2. [Script File](#script-file)
3. [Terraform.tfvars](#terraformtfvars)

## Tool YAML

The Tool YAML file defines the configuration and behavior of your tool. Here is a template you need to edit:

```yaml
tools:
  # 1. Change this to the name of your tool   
  - name: list_s3_buckets
    image: python:3.11
    # 2. Update the description to fit your tool's purpose
    description: "List all S3 buckets in your AWS account using the specified AWS CLI profile."
    # 3. Change this alias to a short, easy-to-type name for your tool
    alias: list-s3-buckets
    content: |
      # 4. Update the URL to point to your repository
      REPO_URL="${REPO_URL:-https://github.com/your-repo/your-project}"

      # 5. Change this to the name of your repository
      REPO_NAME="${REPO_NAME:-your-project}"

      # 6. Specify the directory where your source code is located
      SOURCE_CODE_DIR="${SOURCE_CODE_DIR:-src/tool-example}"

      # 7. Set this to the branch you want to use (e.g., main, dev)
      REPO_BRANCH="${REPO_BRANCH:-main}"

      # 8. Directory name for cloning the repo
      REPO_DIR="${REPO_DIR:-$REPO_NAME}"

      BIN_DIR="${BIN_DIR:-/usr/local/bin}"
      APT_CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"
      PIP_CACHE_DIR="${PIP_CACHE_DIR:-/var/cache/pip}"

      # Create cache directories (DO NOT REMOVE THE CREATION OF CACHE DIRECTORIES)
      mkdir -p "$APT_CACHE_DIR"
      mkdir -p "$BIN_DIR"
      mkdir -p "$PIP_CACHE_DIR"

      # 9. Add more dependencies here if needed
      install_git() {
        apt-get update -qq > /dev/null && apt-get install -y -qq git > /dev/null
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

      # 10. Update this to match the script's location and name within your repository
      exec python list_s3_buckets.py --profile "{{ .profile }}"
    args:
      # 11. Define the command-line arguments for your script
      - name: profile
        # 12. Update the description to explain what the argument is
        description: 'AWS CLI profile name'
        required: true
    env:
      # 13. List environment variables required by your tool
      - AWS_PROFILE
    # 14. Only include this section if your tool requires specific files, such as AWS credentials
    with_files:
      - source: $HOME/.aws/credentials
        destination: /root/.aws/credentials
```

### Customization Steps

#### 1. **Name**
   - **Action:** Change the name of the tool to something unique and descriptive.

#### 2. **Description**
   - **Action:** Update the description to explain what the tool does.

#### 3. **Alias**
   - **Action:** Change the alias to a short, memorable name for the tool.

---

### Within Content

#### 4. **Repo URL**
   - **Action:** Set the URL of your repository.

#### 5. **Repo Name**
   - **Action:** Change to the name of your repository.

#### 6. **Source Code Directory**
   - **Action:** Specify the directory containing your source code.

#### 7. **Repo Branch**
   - **Action:** Set to the branch you want to use (e.g., main, dev).

#### 8. **Repo Directory**
   - **Action:** Directory name for cloning the repository.

#### 9. **Dependencies**
   - **Action:** Add any additional dependencies needed in the `install_git` function.

#### 10. **Exec Python**
   - **Action:** Update the command to run your specific script within the cloned repository.

#### 11. **Args**
   - **Action:** Define the command-line arguments for your script, including names and descriptions.

#### 12. **Env**
   - **Action:** List any environment variables your tool requires.

---

### With Files

> **Note:** Only include this section if your tool needs to access specific files, like AWS credentials.



### Script File
The `tool-example.py` contains the logic for your tool. Here's an example script for listing S3 buckets:

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

### Customization Steps

#### 1. **Functionality**
   - **Action:** Modify the script to implement the functionality you need.

#### 2. **Arguments**
   - **Action:** Add or change command-line arguments as required by your tool.

#### 3. **Dependencies**
   - **Action:** Ensure any additional dependencies are installed in the Tool YAML file.

---

### Terraform.tfvars

The `terraform.tfvars` file contains configuration variables for your Terraform setup:


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

### Customization Steps

#### 1. **Agent Name**
   - **Action:** Change the `agent_name` to reflect the purpose of your tool.

#### 2. **Description**
   - **Action:** Update the `agent_description` and `agent_instructions` to describe your tool and its functionality.

#### 3. **Approval Workflow**
   - **Action:** Configure the approval settings as needed, including the Slack channel and approving users.

#### 4. **Integrations**
   - **Action:** List any integrations your tool needs (e.g., AWS, Slack, GitHub).

#### 5. **ACL**
   - **Action:** Specify the users and groups who can access the agent.

#### 6. **Environment Variables**
   - **Action:** Set any required environment variables.

#### 7. **Debug and Dry Run**
   - **Action:** Enable or disable debug mode and dry run as needed.
