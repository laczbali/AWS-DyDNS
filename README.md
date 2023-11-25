# AWS-DyDNS
Client-side DNS updater for an AWS Route 53 based Dynamic DNS solution

Currently one configuration can only handle updating one record.

## AWS Setup
Make sure that the target record exists. It should have a
- Name
- Record Type of `A`
- Alias, TTL, etc

Configure an **IAM user**. It should have access to the following, on your hosted zone:
- `route53:ChangeResourceRecordSets`
- `route53:ListResourceRecordSets`

## Docker Setup
Create a Docker Compose file, that sets the following env vars:

| Key name              | Value explanation                                                |
| --------------------- | ---------------------------------------------------------------- |
| AWS_ACCESS_KEY_ID     | AWS \ IAM \ Users \ USER \ Security credentials \ Access keys    |
| AWS_SECRET_ACCESS_KEY | AWS \ IAM \ Users \ USER \ Security credentials \ Access keys    |
| HOSTED_ZONE_ID        | AWS \ Route 53 \ Hosted zones \ Zone ID field                    |
| RECORD_NAME           | AWS \ Route 53 \ Hosted zones \ ZONE \ Record name field         |
| LOG_LOCATION          | Wheres should it create log files (errors and assigment changed) |

