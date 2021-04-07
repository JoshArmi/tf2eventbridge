import json
import sys

import boto3


def build_event(change, is_apply):
  account_name = change["name"]

  type = "AccountCreated" if is_apply else "AccountRequested"
  return {
      "Source": f"josharmi.{type.lower()}",
      "Detail": f'{{"Name":"{account_name}"}}',
      "DetailType": type,
  }

def run(is_apply):
  with open("plan.out.json", "r") as file:
    plan = json.loads(file.read())
    changes = plan["resource_changes"]
    events = [build_event(change, is_apply) for change in changes if change["type"] == "aws_organizations_account"]
    eventbridge = boto3.client("events")
    print(events)
    response = eventbridge.put_events(Entries=events)
    print(response)

if __name__ == "__main__":
  if len(sys.argv) == 2:
    run(sys.argv[1] == "apply")
  else:
    run(False)
