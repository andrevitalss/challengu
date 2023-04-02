# https://github.com/franchyze923/Code_From_Tutorials/blob/master/Strava_Api/strava_api.py
# https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde

import requests
import urllib3
from pathlib import Path
from utils.parameters import get_parameters, get_paths

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from pandas import json_normalize


def read_refresh_token(athlete_id):
    pathsparent = Path(__file__).parent.resolve()
    paths = get_paths()
    rtpath = pathsparent / paths['refresh_tokens']
    df = pd.read_csv(rtpath, sep=',').set_index('athlete_id')
    try:
        refresh_token = df.loc[int(athlete_id), 'refresh_token']
        return refresh_token
    except KeyError:
        return None


def get_refresh_token(code):

    print('code: ' + code)

    parameters = get_parameters()
    client_id = parameters['client_id']
    client_secret = parameters['client_secret']
    token_url = parameters['token_url']

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        return None

    refresh_token = response.json().get("refresh_token")
    athlete_id = response.json().get("athlete").get('id')

    return refresh_token, athlete_id

def get_access_token(refresh_token):
    print('refresh_token: ' + refresh_token)

    parameters = get_parameters()
    client_id = parameters['client_id']
    client_secret = parameters['client_secret']
    token_url = parameters['token_url']

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    response = requests.post(token_url, data=payload, verify=False)

    if response.status_code != 200:
        return None

    access_token = response.json()['access_token']

    return access_token

def get_activites(access_token):

    print('access_token: ' + access_token)

    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}

    response = requests.get(activites_url, headers=header, params=param)
    print(response)
    if response.status_code != 200:
        return None

    my_dataset = response.json()

    activities = json_normalize(my_dataset)
    return my_dataset



if __name__ == '__main__':
    refresh_token = '87cc32167d7fd043f5d73a93a2df44a52bab2d7c'
    activities = get_activites(refresh_token)
    print(activities)