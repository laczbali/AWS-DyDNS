import requests
import re
import json
import subprocess

print(
"""
      __          _______   _____  _____  _   _  _____ 
     /\ \        / / ____| |  __ \|  __ \| \ | |/ ____|
    /  \ \  /\  / / (___   | |  | | |  | |  \| | (___  
   / /\ \ \/  \/ / \___ \  | |  | | |  | | . ` |\___ \ 
  / ____ \  /\  /  ____) | | |__| | |__| | |\  |____) |
 /_/    \_\/  \/  |_____/  |_____/|_____/|_| \_|_____/ 
 by blaczko                                            
                                                       
"""
)

config_file = open("config.json", "r")
config = json.loads(config_file.read())

# get current IP address
http_result = requests.get('http://checkip.amazonaws.com/')
if not http_result.ok:
    # TODO error handling
    exit()

actual_ip = http_result.text.strip()
ip_is_valid = re.search("\d+\.\d+\.\d+\.\d+", actual_ip)
if not ip_is_valid:
    # TODO error handling
    exit()

print(f"The actual public IP address is {actual_ip}")

# get the IP address set in Route 53
current_config = subprocess.getoutput(
    f"aws route53 list-resource-record-sets" \
    f" --hosted-zone-id {config['hosted_zone_id']}" \
    f" --profile {config['cli_profile']}" \
    f" --no-cli-pager --output json"
)
current_config = json.loads(current_config)
recordsets = current_config['ResourceRecordSets']

current_record = [
    r for r in recordsets
    if r['Name'] == f"{config['record_name']}."
    and r['Type'] == 'A'
][0]
currently_set_ip = current_record['ResourceRecords'][0]['Value']
# TODO error handling

print(f"The currently set IP address is {currently_set_ip}")

# update IP, if needed
if actual_ip == currently_set_ip:
    print("No change necessary\n")
    exit()

print("\nChanging")
print(f"from - {current_record}")

updated_record = current_record
updated_record['ResourceRecords'] = [
    {'Value': actual_ip}
]
print(f"to   - {updated_record}")

change_object = {
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": updated_record
        }
    ]
}

temp_json = open("temp.json", "w")
temp_json.write(json.dumps(change_object))
temp_json.close()

action_result = subprocess.getoutput(
    f"aws route53 change-resource-record-sets" \
    f" --hosted-zone-id {config['hosted_zone_id']}" \
    f" --change-batch file://temp.json" \
    f" --profile {config['cli_profile']}" \
    f" --no-cli-pager"
)
# TODO error handling

print(action_result + "\n")
