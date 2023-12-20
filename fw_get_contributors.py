import requests

API_URL = 'https://indiscale.preview.fair-wizard.com/wizard-api'
API_KEY = '...'

CONTRIBUTORS_PATH = '1e85da40-bbfc-4180-903e-6c569ed2da38.73d686bd-7939-412e-8631-502ee6d9ea7b'
Q_NAME_UUID = '6155ad47-3d1e-4488-9f2a-742de1e56580'
Q_EMAIL_UUID = '3a2ffc13-6a0e-4976-bb34-14ab6d938348'
Q_ORCID_UUID = '6295a55d-48d7-4f3c-961a-45b38eeea41f'


def get_contributors(project_uuid: str) -> list:
    """Get contributors of a project.

    Args:
        project_uuid (str): Project UUID.

    Returns:
        list: List of contributors.
    """
    url = f'{API_URL}/questionnaires/{project_uuid}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()

    replies = data['replies']
    
    contributors_reply = replies.get(CONTRIBUTORS_PATH, None)
    if contributors_reply is None:
        return []
    
    contributor_items = contributors_reply['value']['value']
    contributors = []
    for item_uuid in contributor_items:
        contributor = {}
        contributor['uuid'] = item_uuid

        reply = replies.get(f'{CONTRIBUTORS_PATH}.{item_uuid}.{Q_NAME_UUID}', None)
        if reply is not None:
            contributor['name'] = reply['value']['value']

        reply = replies.get(f'{CONTRIBUTORS_PATH}.{item_uuid}.{Q_EMAIL_UUID}', None)
        if reply is not None:
            contributor['email'] = reply['value']['value']

        reply = replies.get(f'{CONTRIBUTORS_PATH}.{item_uuid}.{Q_ORCID_UUID}', None)
        if reply is not None:
            contributor['orcid'] = reply['value']['value']

        contributors.append(contributor)
    return contributors


if __name__ == '__main__':
    contributors = get_contributors(project_uuid='ae8496de-b75d-4226-a04a-cee6f0869878')
    print(contributors)
