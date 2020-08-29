from flask import request, make_response, jsonify, Blueprint
from google.cloud import datastore
from Utils import handleException
from seq2seq import reply
import time
import json


comment_api = Blueprint('comment_api', __name__)


def getDiary(date, uid):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='Diary')
    query.add_filter('date', '=', date)
    query.add_filter('uid', '=', uid)
    diary = list(query.fetch())
    if len(diary) > 0:
        return diary[0]
    return None


def getComments(date, uid):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='DiaryComment')
    query.add_filter('date', '=', date)
    query.add_filter('uid', '=', uid)
    query.order = ['timestamp']
    return list(query.fetch())


def saveComment(date, uid, comment, isowner):
    datastore_client = datastore.Client()
    comment_entity = datastore.Entity(datastore_client.key('DiaryComment'))
    comment_entity.update({
        'date': date,
        'comment': comment,
        'isowner': isowner,
        'timestamp': time.time(),
        'uid': uid
    })
    datastore_client.put(comment_entity)


def generateComment(comment, mode='retrieval'):
    if mode == 'retrieval':
        ans = reply(comment)
    else:
        ans = reply(comment)
    return ans


@comment_api.route('/comment', methods=['GET'])
def getCommentAPI():
    response = {'status': 'Error'}
    try:
        date = request.args.get('date')
        uid = request.args.get('id')

        diary = getDiary(date, uid)
        if diary is not None:
            if diary['score'] < -0.8 or diary['emotion_class'] == 'depressed':
                comments = getComments(date, uid)
                if len(comments) == 0 or comments[-1]['isOwner']:
                    newComment = generateComment(diary['content'])
                    saveComment(date, uid, newComment, isowner = False)
                    comments = getComments(date, uid)
                response['data'] = comments
            else:
                response['data'] = []
            response['status'] = 'OK'

    except Exception as e:
        handleException(e)

    return make_response(jsonify(response))


@comment_api.route('/post-comment', methods=['POST'])
def postCommentAPI():
    response = {'status': 'Error'}
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data(as_text=True))
            date = data['date']
            uid = data['id']
            comment = data['comment']

            saveComment(date, uid, comment, isowner = True)

            response['status'] = 'OK'

        except Exception as e:
            handleException(e)

    return make_response(jsonify(response))
