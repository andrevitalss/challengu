"""Dashboard web application.

To run for development::

    uvicorn app:app --reload
"""

from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from pathlib import Path

from strava_api import get_activites, get_refresh_token, get_access_token, read_refresh_token, save_new_refresh_token
from utils.parameters import get_parameters

app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/")
def root():
    return RedirectResponse('/security')

@app.get("/security")
def security(request: Request):
    username = 'andre'
    password = 'senha'
    athlete_id = '31500954'
    athlete_id = '5158194'
    athlete_id = '123'
    refresh_token = read_refresh_token(athlete_id)
    if refresh_token is None:
        return RedirectResponse('/calltoauth')
    else:
        access_token = get_access_token(refresh_token)
        if access_token is None:
            raise HTTPException(status_code=400, detail="Não foi possível obter o access_token")

        activities = get_activites(access_token)
        return templates.TemplateResponse(
            "activities.html",
            {
                "activities": activities,
                "request": request,
            }
        )

@app.get("/calltoauth")
def call_to_auth():
    parameters = get_parameters()
    return RedirectResponse('https://www.strava.com/oauth/authorize?'
                            'client_id=' + parameters['client_id'] + '&'
                            'redirect_uri=http://3.83.154.205/auth&response_type=code&scope=activity:read_all')


@app.get("/auth")
def get_code(request: Request, code: str = None):
    if code is None:
        raise HTTPException(status_code=400, detail="Código de autorização ausente")

    refresh_token, athlete_id = get_refresh_token(code)
    print('refresh token from code: ' + refresh_token)
    if refresh_token is None:
        raise HTTPException(status_code=400, detail="Não foi possível obter o refresh_token")

    save_new_refresh_token(refresh_token, athlete_id)

    access_token = get_access_token(refresh_token)
    if access_token is None:
        raise HTTPException(status_code=400, detail="Não foi possível obter o access_token")

    activities = get_activites(access_token)
    if activities is None:
        raise HTTPException(status_code=400, detail="Não foi possível acessar a API do Strava")

    return templates.TemplateResponse(
        "activities.html",
        {
            "activities": activities,
            "request": request,
        }
    )

