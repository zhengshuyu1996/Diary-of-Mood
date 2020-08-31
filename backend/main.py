import os
from flask import Flask
from AuthAPI import auth_api
from DiaryAPI import diary_api
from CommentAPI import comment_api

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__, static_url_path='', static_folder='dist')
app.debug = True
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
app.register_blueprint(auth_api)
app.register_blueprint(diary_api)
app.register_blueprint(comment_api)
app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080)
