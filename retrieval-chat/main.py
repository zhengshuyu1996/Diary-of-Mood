import os
from flask import Flask, request, make_response, jsonify, Blueprint
#from Utils import handleException
import json
from extract_feature import BertVector
from annoy import AnnoyIndex
import traceback

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.debug = True

f = 768
t = AnnoyIndex(f, 'angular')

q=[]
bv = BertVector()

ans = []

def handleException(e):
    print ('str(e):\t\t', str(e))
    print ('repr(e):\t', repr(e))
    print ('e.message:\t', e.message)
    print ('traceback.print_exc():', traceback.print_exc())
    print ('traceback.format_exc():\n%s' % traceback.format_exc())
    
def generateComment(comment, mode='retrieval'):
    result = ''
    if mode == 'retrieval':
        testq = bv.encode([comment]) # get sentence embedding
        res = t.get_nns_by_vector(testq[0], 5) # find 5 nearest
        candidate = [ans[res[i]] for i in range(5)]
        result = max(candidate, key=len, default='') 
    return result


@app.route('/generate', methods=['GET', 'POST'])
def postCommentAPI():
    response = {'status': 'Error'}
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data(as_text=True))
            comment = data['comment']
            mode = data['mode']
            
            ret = generateComment(comment, mode)

            response['status'] = 'OK'
            response['data'] = ret

        except Exception as e:
            handleException(e)

    return make_response(jsonify(response))



if __name__ == '__main__':

    with open('corpus/answer_2.txt', 'r',encoding='UTF-8') as DR:
        for line in DR:
            if len(line)>0:
                ans.append(line)
    DR.close()

    t.load('test.ann')
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='0.0.0.0', port=5000)