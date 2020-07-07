from authlib.flask.client import OAuth
import os

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    GOOGLE_CLIENT_SECRET=os.environ["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com',
    client_kwargs={'scope': 'email profile openid'},
    redirect_ur=os.environ['REDIRECT_URI']
)
