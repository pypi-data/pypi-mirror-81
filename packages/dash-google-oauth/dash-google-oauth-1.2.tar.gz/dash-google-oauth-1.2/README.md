# Dash Google OAuth

This is a simple library using Google OAuth to authenticate and view a Dash app
written based on [dash-auth](https://github.com/plotly/dash-auth).
Upon authentication, a cookie is created and kept for 2 weeks.

### Setup
Navigate to [Google API Console](https://console.cloud.google.com/apis/credentials), and setup an OAuth credentials
with `http://localhost:5000/login/callback` as authorized redirect URL.

Install the package:
```
$ pip install dash-google-oauth
```
Define following environment variables:
```
FLASK_SECRET_KEY

GOOGLE_AUTH_URL
GOOGLE_AUTH_SCOPE
GOOGLE_AUTH_TOKEN_URI
GOOGLE_AUTH_REDIRECT_URI
GOOGLE_AUTH_USER_INFO_URL
GOOGLE_AUTH_CLIENT_ID
GOOGLE_AUTH_CLIENT_SECRET
```
for example using [python-dotenv](https://pypi.org/project/python-dotenv/):
```
FLASK_SECRET_KEY="..."

GOOGLE_AUTH_URL=https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent
GOOGLE_AUTH_SCOPE="openid email profile"
GOOGLE_AUTH_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_AUTH_REDIRECT_URI=http://localhost:5000/login/callback
GOOGLE_AUTH_USER_INFO_URL=https://www.googleapis.com/userinfo/v2/me
GOOGLE_AUTH_CLIENT_ID="..."
GOOGLE_AUTH_CLIENT_SECRET="..."
```
Add it to the application:
```
app = Dash(__name__)

from dash_google_oauth.google_auth import GoogleAuth
auth = GoogleAuth(app)
```
To logout, you may make a `GET` request to `/logout`
