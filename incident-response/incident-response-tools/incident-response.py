from kubiya_sdk.tools import Arg
from .base import IncidentResponseTool
from kubiya_sdk.tools.registry import tool_registry

incident_response_communication = IncidentResponseTool(
    name="incident_response_communication",
    description="Trigger Major Incident Response",
    content="""
#!/usr/bin/env python3

import os
import requests
import json
import argparse
from datetime import datetime, timedelta

def get_access_token():
    url = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token"
    payload = {
        'client_id': os.getenv('AZURE_CLIENT_ID'),
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': os.getenv('AZURE_CLIENT_SECRET'),
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json().get('access_token')

def get_oncall_engineer(escalation_policy_id):
    url = f"https://api.pagerduty.com/oncalls?escalation_policy_ids[]={escalation_policy_id}"
    headers = {
        "Authorization": f"Token token={os.getenv('PD_API_KEY')}",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    oncalls = response.json().get('oncalls', [])
    for oncall in oncalls:
        if oncall.get('user'):
            return oncall['user']['summary']
    return "Incident Commander"

def create_pd_incident(description):
    url = "https://api.pagerduty.com/incidents"
    headers = {
        "Authorization": f"Token token={os.getenv('PD_API_KEY')}",
        "Content-Type": "application/json",
        "From": os.getenv('KUBIYA_USER_EMAIL')
    }
    payload = {
        "incident": {
            "type": "incident",
            "title": f"Major Incident via Kubi - {description}",
            "service": {
                "id": "PUSDB5G",
                "type": "service_reference"
            },
            "escalation_policy": {
                "id": "PPBZA76",
                "type": "escalation_policy_reference"
            },
            "body": {
                "type": "incident_body",
                "details": description
            }
        }
    }
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"Headers: {headers}")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    response.raise_for_status()
    return response.json()["incident"]["id"]

def create_ticket(description, business_impact, incident_id, incident_commander):
    url = "https://aenetworks.freshservice.com/api/v2/tickets"
    user_email = os.getenv('KUBIYA_USER_EMAIL')
    payload = {
        "description": f"{description}<br><strong>Incident Commander:</strong> {incident_commander}<br><strong>Detection Method:</strong> Detection Method<br><strong>Business Impact:</strong> {business_impact}<br><strong>Ticket Link:</strong>PagerDuty Incident",
        "subject": f"MAJOR INCIDENT pagerduty-kubiya-page-oncall-service - Major Incident via Kubi",
        "email": user_email,
        "priority": 1,
        "status": 2,
        "source": 8,
        "category": "DevOps",
        "sub_category": "Pageout",
        "tags": [f"PDID_{incident_id}"]
    }
    response = requests.post(url, headers={"Content-Type": "application/json"}, auth=(os.getenv('FSAPI_PROD'), "X"), data=json.dumps(payload))
    response.raise_for_status()
    return response.json()["ticket"]["id"]

def create_meeting(access_token):
    url = "https://graph.microsoft.com/v1.0/users/d69debf1-af1f-493f-8837-35747e55ea0f/onlineMeetings"
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(hours=1)
    payload = {
        "startDateTime": start_time.isoformat() + "Z",
        "endDateTime": end_time.isoformat() + "Z"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()["joinUrl"]

def get_slack_user_id(email):
    url = "https://slack.com/api/users.lookupByEmail"
    headers = {
        "Authorization": f"Bearer {os.getenv('SLACK_API_TOKEN')}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {'email': email}
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if response_data['ok']:
        return response_data['user']['id']
    else:
        print(f"Error fetching user ID for {email}: {response_data['error']}")
        return None

def send_slack_message(channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('SLACK_API_TOKEN')}"
    }
    payload = {
        "channel": channel,
        "text": message
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

def main(description, business_impact):
    if not description or not business_impact:
        print("Usage: trigger-major-incident-communication.py --description <description> --business_impact <business_impact>")
        return
        
    reporter = os.getenv("KUBIYA_USER_EMAIL")
    access_token = get_access_token()
    escalation_policy_id = "PPBZA76"  # Replace with your actual escalation policy ID
    incident_commander = get_oncall_engineer(escalation_policy_id)
    pd_incident_id = create_pd_incident(description)
    ticket_id = create_ticket(description, business_impact, pd_incident_id, incident_commander)
    ticket_url = f"https://aenetworks.freshservice.com/a/tickets/{ticket_id}"
    meeting_link = create_meeting(access_token)
    
    # Fetch Slack user ID for the reporter
    reporter_user_id = get_slack_user_id(reporter)
    reporter_mention = f"<@{reporter_user_id}>" if reporter_user_id else reporter

    # Channel ID for #incident_response (replace with actual ID)
    channel_id = "CAZ6ZGBJ7"  # Replace with the actual channel ID for #incident_response

    message = f"""
    ************** SEV 1 ****************
    <@U04JCDSHS76> <@U04J2MTMRFD> <@U04FZPQSY3H> <@U048QRBV2NA> <@U04UKPX585S> <@U02SSCGCQQ6>
    Incident Commander: {incident_commander}
    Description: {description}
    Business Impact: {business_impact}
    Bridge Link: <{meeting_link}|Bridge Link>
    PagerDuty Incident URL: https://aetnd.pagerduty.com/incidents/{pd_incident_id}
    FS Ticket URL: {ticket_url}
    Reported by: {reporter_mention}
    We will keep everyone posted on this channel as we assess the issue further.
    """
    send_slack_message("#incident_response", message.strip())

    print(f"Please go to the <#{channel_id}|incident_response> channel to find the SEV1 announcement. The bridge line and pertinent details have been posted there. Thank you.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger Major Incident Response.")
    parser.add_argument("--description", required=True, help="The description of the incident.")
    parser.add_argument("--business_impact", required=True, help="The business impact of the incident.")
    args = parser.parse_args()
    main(args.description, args.business_impact)
    """,
    args=[
        Arg(name="description", type="str", description="The description of the incident.", required=True),
        Arg(name="business_impact", type="str", description="The business impact of the incident.", required=True),
    ],
)

tool_registry.register("incident_response", incident_response_communication)