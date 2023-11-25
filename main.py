import os
import requests
import re
import json
import subprocess
from datetime import datetime

print(
fr"""
      __          _______   _____  _____  _   _  _____ 
     /\ \        / / ____| |  __ \|  __ \| \ | |/ ____|
    /  \ \  /\  / / (___   | |  | | |  | |  \| | (___  
   / /\ \ \/  \/ / \___ \  | |  | | |  | | . ` |\___ \ 
  / ____ \  /\  /  ____) | | |__| | |__| | |\  |____) |
 /_/    \_\/  \/  |_____/  |_____/|_____/|_| \_|_____/ 
 by blaczko                                            

 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

"""
)

# setup
config = {
    "hosted_zone_id": os.environ['HOSTED_ZONE_ID'],
    "record_name": os.environ['RECORD_NAME'],
    "log_location": os.environ['LOG_LOCATION']
}

def create_log(filePrefix, message, details):
    filedir = config['log_location']
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    filename = f"{filePrefix}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")}"
    logpath = os.path.join(filedir, filename)

    content = f"{message}\n\n{details}"

    log = open(logpath, "w")
    log.write(content)
    log.close()

def log_error(message, details):
    create_log("error", message, details)
    print(f"ERROR: {message}")

def log_info(message, details):
    create_log("info", message, details)
    print(f"INFO: {message}")

# get current IP address
try:
    http_result = requests.get('http://checkip.amazonaws.com/')
    if not http_result.ok:
        log_error("Failed to query actual IP", http_result.text)
        exit()
except Exception as e:
    log_error("Failed to query actual IP", e)
    exit()

actual_ip = http_result.text.strip()
ip_is_valid = re.search(r"\d+\.\d+\.\d+\.\d+", actual_ip)
if not ip_is_valid:
    log_error("Received invalid actual IP", actual_ip)
    exit()

print(f"The actual public IP address is {actual_ip}")

# get the IP address set in Route 53
try:
    current_config = subprocess.getoutput(
        f"aws route53 list-resource-record-sets" \
        f" --hosted-zone-id {config['hosted_zone_id']}" \
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
except Exception as e:
    log_error("Failed to get currently set IP", e)
    exit()

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

try:
    action_result = subprocess.getoutput(
        f"aws route53 change-resource-record-sets" \
        f" --hosted-zone-id {config['hosted_zone_id']}" \
        f" --change-batch file://temp.json" \
        f" --no-cli-pager"
    )
except Exception as e:
    log_error("Failed to update IP", e)
    exit()

print(action_result + "\n")
log_info(f"Successfully updated IP from {currently_set_ip} to {actual_ip}", "")
