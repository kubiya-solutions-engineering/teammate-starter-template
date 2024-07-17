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

// Other settings
secrets      = []
integrations = ["aws", "slack"]
// ACL for the agent - Users and groups who can access the agent
// Users group is a special group that includes all users
users  = ["user@example.com"]
groups = ["Admin", "Users"]
// Fetch all tools from the directory in the folder (resource-life-cycle/tools/*)
agent_tool_sources = ["https://github.com/your-repo/src/tool-example/*"]
links              = []

// Environment variables
log_level        = "INFO"

// Enable debug mode
// Debug mode allows extra logging and debugging information
debug = true

// dry run
// When enabled, the agent will not apply the changes but will show the changes that will be applied
dry_run = true
```

### Customization Steps

1. **Agent Name**
   - **Action:** Change the `agent_name` to reflect the purpose of your tool.

2. **Runner**
   - **Action:** Update the `kubiya_runner` to the name of the runner you create within Kubiya.

3. **Description**
   - **Action:** Update the `agent_description` to describe your tool and its functionality.
   - **Action:** Update the `agent_instructions` to give the agent an identity, like the example shown: "You are an intelligent agent designed to help manage the lifecycle of infrastructure resources. **You have access only to the commands you see on this prompt**."

4. **Integrations**
   - **Action:** List any integrations your tool needs (e.g., AWS, Slack, GitHub).

5. **ACL**
   - **Action:** Specify the users and groups who can access the agent.

6. **Environment Variables**
   - **Action:** Set any required environment variables.

7. **Debug and Dry Run**
   - **Action:** Enable or disable debug mode and dry run as needed.


