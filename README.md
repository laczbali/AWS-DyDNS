# AWS-DyDNS
Client-side DNS updater for an AWS Route 53 based Dynamic DNS solution

Currently one configuration can only handle updating one record.

## Setup
Make sure that the target record exists. It should have a
- Name
- Record Type of `A`
- Alias, TTL, etc

Configure an **IAM user**. It should have access to the following, on your hosted zone:
- `route53:ChangeResourceRecordSets`
- `route53:ListResourceRecordSets`

Download the **AWS CLI**, and create a named profile with the IAM user
```
aws configure --profile CLI_PROFILE_NAME
```

Create a file, called `config.json` in the repo folder.
```json
{
    "$schema": ".\\config.schema.json",

    "cli_profile": "CLI_PROFILE_NAME",
    "hosted_zone_id": "YOUR_HOSTED_ZONE_ID",
    "record_name": "RECORD_NAME"
}
```

**Run `install.bat`**. It will create a file called `startup.bat`, which you can use to run the script.
It will also register a Scheduled Task, which will call `startup.bat` every 5 minutes.
