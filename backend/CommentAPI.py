from flask import request, make_response, jsonify, Blueprint
from google.cloud import datastore
from Utils import handleException
# from seq2seq import reply
import time
import json
import requests


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
    # print(date, uid)
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='DiaryComment')
    query.add_filter('date', '=', date)
    query.add_filter('uid', '=', uid)
    ans = list(query.fetch())
    ans = sorted(ans, key = lambda x: x['timestamp'])
    return ans


def saveComment(date, uid, comment, isowner):
    datastore_client = datastore.Client()

    # save comment
    comment_entity = datastore.Entity(datastore_client.key('DiaryComment'))
    comment_entity.update({
        'date': date,
        'comment': comment,
        'isOwner': isowner,
        'timestamp': time.time(),
        'uid': uid
    })
    datastore_client.put(comment_entity)

    # update calendar
    query = datastore_client.query(kind='Calendar')
    query.add_filter('uid', '=', uid)
    query.add_filter('date', '=', date)
    calendar_entity = list(query.fetch())[0]
    calendar_entity['responseNum'] = calendar_entity['responseNum'] + 1
    datastore_client.put(calendar_entity)


def generateComment(comment, mode='retrieval'):
    data = {'comment': comment, 'mode': mode}
    ans = requests.post('http://luckylucy060.nat300.top/generate', json.dumps(data))
    ans.encoding = 'utf-8'
    data = json.loads(ans.text)
    if data['status'] == 'OK':
        # print(data['data'])
        return data['data']
    return ''


@comment_api.route('/comments', methods=['GET'])
def getCommentAPI():
    response = {'status': 'Error'}
    try:
        date = request.args.get('date')
        uid = request.args.get('id')

        diary = getDiary(date, uid)
        if diary is not None:
            if diary['point'] < -0.5 or diary['emotion_class'] == 'depressed':
                comments = getComments(date, uid)
                # print(comments)
                if len(comments) == 0 or comments[-1]['isOwner']:
                    if len(comments) == 0:
                        newComment = generateComment(diary['content'])
                    else:
                        newComment = generateComment(comments[-1]['comment'])
                    if len(newComment) > 0:
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
