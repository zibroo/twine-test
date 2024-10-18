import json
import os
import requests


class OpsgenieClient(object):
    """ Opsgenie Client Object. """

    def __init__(self, api_key: str, og_url: str = "https://api.opsgenie.com"):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"GenieKey {api_key}",
            "Accept": "*/*",
            "Content-Type": "application/json"
        }
        self.og_url = og_url
        self.base_url = f"{self.og_url}/v2/alerts"

    def create_alert(self, message: str, description: str, responders: list[dict[str, str]], priority: str, alias: str,
                     tags: list[str], attachment: str = None) -> str:

        body = {"message": message, "alias": alias, "description": description, "responders": responders,
                "visibleTo": responders, "tags": tags, "priority": priority}

        api_response = requests.post(url=self.base_url, data=json.dumps(body), headers=self.headers)
        response_text = json.loads(api_response.text)

        if api_response.status_code != 202:
            print(f"Error creating alert: {response_text.get('result')}")
            return False
        else:
            request_id = response_text.get("requestId")
            return self.get_request_status(request_id=response_text.get("requestId"))

    def get_request_status(self, request_id: str):
        alert_status_url = f"{self.base_url}/requests/{request_id}"
        api_response = requests.get(url=alert_status_url, headers=self.headers)
        response_text = json.loads(api_response.text)
        if api_response.status_code != 200:
            print(f"Error getting alert status: {response_text.get('result')}")
            return False
        else:
            if response_text.get('data').get('success'):
                return True
            else:
                return False

    def close_alert_by_alias(self, alias: str, note: str):

        close_alert_url = f"{self.base_url}/{alias}/close?identifierType=alias"

        body = {
            "note": note
        }
        api_response = requests.post(url=close_alert_url, data=json.dumps(body), headers=self.headers)

        if api_response.status_code not in (200, 202):
            return False
        else:
            return True

    def get_alert_by_alias(self, alias: str):
        get_alert_url = f"{self.base_url}/{alias}?identifierType=alias"
        api_response = requests.get(url=get_alert_url, headers=self.headers)

        if api_response.status_code in (200, 202):
            api_response_text = json.loads(api_response.text)
            data = api_response_text.get("data")
            status = data.get("status")

            return status
        else:
            return api_response.text

    def close_alert_if_open(self, alias: str, note: str = None):
        alert_status = self.get_alert_by_alias(alias=alias)

        if alert_status == 'open':
            og_close_status = self.close_alert_by_alias(alias=alias, note=note)
            if og_close_status:
                print(f"Alert closed in Opsgenie: {note}")
        else:
            print(f"Alert status was not open so close alert was skipped")


def main():
    """Use for local testing"""
    og_api_key = os.getenv("OPSGENIE_KEY")
    og_client = OpsgenieClient(api_key=og_api_key)
    alias = "TomTestAlert"

    create_alert_status = og_client.create_alert(
        message="Test Alert form opsgenie client package",
        description="Just a test",
        responders=[{'name': 'CRE Platform', 'type': 'team'}],
        alias='TomTestAlert',
        tags=["TEAM:CRE Platform"],
        priority="P3"
    )

    if create_alert_status:
        print("Create Alert was successful")

    og_client.close_alert_if_open(alias=alias, note=f"Current check is passing. Closing previous alert for alias = "
                                                    f"{alias}")
    alert_status = og_client.get_alert_by_alias(alias=alias)



if __name__ == "__main__":
    main()
