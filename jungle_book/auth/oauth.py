from authlib.flask.client import OAuth

# TODO put sensitive data into env variable
oauth = OAuth()
oauth.register(
    name="google",
    client_id="810979674149-i58pjaopuunstb60n6j645nhb9mvk66e.apps.googleusercontent.com",
    client_secret="DVVkppPgpEFDX5S7naVvLGjA",
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com',
    client_kwargs={'scope': 'email profile openid'},
    redirect_uri="http://localhost:5000/"
 )
