from flask import request, make_response, jsonify, Blueprint
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import datastore
from Utils import handleException
from multi_label_semantic import get_label
from sos_classify import sos_model


diary_api = Blueprint('diary_api', __name__)


def deleteDiary(date, uid):
    datastore_client = datastore.Client()

    # Delete from Diary
    query = datastore_client.query(kind='Diary')
    query.add_filter('date', '=', date)
    query.add_filter('uid', '=', uid)
    query.keys_only()
    keys = list([entity.key for entity in query.fetch()])
    datastore_client.delete_multi(keys)

    # Delete from Calendar
    query = datastore_client.query(kind='Calendar')
    query.add_filter('date', '=', date)
    query.add_filter('uid', '=', uid)
    query.keys_only()
    keys = list([entity.key for entity in query.fetch()])
    datastore_client.delete_multi(keys)


def deleteDiaryComment(date, uid):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='DiaryComment')
    query.add_filter('date', '=', date)
    query.add_filter('uid', '=', uid)
    query.keys_only()
    keys = list([entity.key for entity in query.fetch()])
    datastore_client.delete_multi(keys)

def addDiary(date, title, content, uid):
    # Detects the sentiment of the text
    nlp_client = language.LanguageServiceClient()
    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = nlp_client.analyze_sentiment(
        document=document
        ).document_sentiment
    score = sentiment.score

    # Detect multilabel class
    emotion_class, emotion_score = get_label(content)
    emotion_score = float(emotion_score)
    if 'depressed' in emotion_class:
        emotion_class = 'depressed'
    else:
        emotion_class = emotion_class[0]
    print('multi_label_analysis', emotion_class, emotion_score)

    # Detect sos class
    sos = int(sos_model.predict(content))

    # Store Calendar entity
    datastore_client = datastore.Client()
    calendar_entity = datastore.Entity(datastore_client.key('Calendar'))
    calendar_entity.update({
        'date': date,
        'point': score,
        'emotion_class': emotion_class,
        'emotion_score': emotion_score,
        'sos': sos,
        'words': len(content),
        'responseNum': 0,
        'hasNew': False,
        'uid': uid
    })
    datastore_client.put(calendar_entity)

    # Store Calendar entity
    diary_entity = datastore.Entity(datastore_client.key('Diary'))
    diary_entity.update({
        'title': title,
        'date': date,
        'content': content,
        'point': score,
        'emotion_class': emotion_class,
        'emotion_score': emotion_score,
        'sos': sos,
        'uid': uid
    })
    datastore_client.put(diary_entity)


@diary_api.route('/calendar/', methods=['GET'])
def getCalendarAPI():
    response = {'status': 'Error'}
    if request.method == 'GET':
        try:
            uid = request.args.get('id')
            datastore_client = datastore.Client()
            query = datastore_client.query(kind='Calendar')
            query.add_filter('uid', '=', uid)
            response['data'] = list(query.fetch())
            response['status'] = 'OK'

        except Exception as e:
            handleException(e)

    return make_response(jsonify(response))


@diary_api.route('/diary', methods=['GET'])
def getDiaryAPI():
    response = {'status': 'Error'}
    try:
        date = request.args.get('date')
        uid = request.args.get('id')

        datastore_client = datastore.Client()
        query = datastore_client.query(kind='Diary')
        query.add_filter('date', '=', date)
        query.add_filter('uid', '=', uid)
        diary = list(query.fetch())

        if len(diary) > 0:
            response['status'] = 'OK'
            response['data'] = diary[0]

    except Exception as e:
        handleException(e)

    return make_response(jsonify(response))


@diary_api.route('/delete', methods=['GET'])
def deleteDiaryAPI():
    response = {'status': 'Error'}
    try:
        date = request.args.get('date')
        uid = request.args.get('id')
        deleteDiary(date, uid)
        deleteDiaryComment(date, uid)
        response['status'] = 'OK'

    except Exception as e:
        handleException(e)

    return make_response(jsonify(response))


@diary_api.route('/add', methods=['POST'])
def addDiaryAPI():
    response = {'status': 'Error'}
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data(as_text=True))
            title = data['title']
            date = data['date']
            diary_text = data['content']
            uid = data['id']

            addDiary(date, title, diary_text, uid)

            response['status'] = 'OK'

        except Exception as e:
            handleException(e)

    return make_response(jsonify(response))


@diary_api.route('/edit', methods=['POST'])
def editDiaryAPI():
    response = {'status': 'Error'}
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data(as_text=True))
            title = data['title']
            date = data['date']
            diary_text = data['content']
            uid = data['id']

            deleteDiary(date, uid)
            addDiary(date, title, diary_text, uid)

            response['status'] = 'OK'

        except Exception as e:
            handleException(e)

    return make_response(jsonify(response))
