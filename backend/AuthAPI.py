import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.cloud import datastore
from Utils import handleException

auth_api = flask.Blueprint('auth_api', __name__)

CLIENT_SECRETS_FILENAME = '/home/szheng/client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'openid', 'https://www.googleapis.com/auth/userinfo.email']


def saveToken(credential):
    datastore_client = datastore.Client()
    entity = datastore.Entity(datastore_client.key('Tokens'))
    entity.update(credential)
    datastore_client.put(entity)


def getToken(token):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='Tokens')
    query.add_filter('token', '=', token)
    data = list(query.fetch())

    if len(data) > 0:
        return data[0]
    return None


@auth_api.route('/checkLogin')
def checkLogin():
    response = {'status': 'Error'}
    try:
        if 'credentials' not in flask.session:
            response['isLogin'] = False

        else:
            complete_token = getToken(flask.session['credentials']['token'])
            if complete_token is None:
                response['isLogin'] = False
            else:
                response['isLogin'] = True
                # Load the credentials from the session.
                credentials = google.oauth2.credentials.Credentials(
                    **complete_token)

                # Get the basic user info from the Google OAuth2.0 API.
                client = googleapiclient.discovery.build(
                    'oauth2', 'v2', credentials=credentials)

                response['userInfo'] = client.userinfo().v2().me().get().execute()

        response['status'] = 'OK'

    except Exception as e:
        handleException(e)

    return flask.make_response(flask.jsonify(response))


@auth_api.route('/login')
def authorize():
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
    # steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME,
        scopes=SCOPES)
    flow.redirect_uri = flask.url_for('auth_api.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        # This parameter enables offline access which gives your application
        # an access token and a refresh token for the user's credentials.
        access_type='offline',
        # This parameter enables incremental auth.
        include_granted_scopes='true')
    print('authorize', flow.redirect_uri)
    # Store the state in the session so that the callback can verify the
    # authorization server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@auth_api.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME,
        scopes=SCOPES,
        state=state)
    # flow.redirect_uri = flask.url_for('auth_api.oauth2callback', _external=True)
    flow.redirect_uri = 'https://8080-cs-673962857811-default.us-central1.cloudshell.dev/oauth2callback'

    authorization_response = flask.request.url
    print('oauth2callback', flow.redirect_uri)
    print(authorization_response)

    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    credentials = flow.credentials
    flask.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    saveToken(flask.session['credentials'])

    return flask.redirect('/')
