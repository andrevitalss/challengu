from pathlib import Path
import os


def get_paths():
    pathsparent = Path(__file__).parent.resolve()
    paths = {'refresh_tokens': 'bases\\refresh_tokens.txt'}
    return paths


def get_parameters():
    parameters = {'client_id': '104942',
                  'client_secret': '8c416b2a7446e04c7c97b9f689849d3e0a1c8086',
                  'token_url': "https://www.strava.com/oauth/token"}
    return parameters