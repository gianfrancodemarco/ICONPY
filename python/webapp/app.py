# set FLASK_ENV=development
# set FLASK_APP=app.py
# flask run

# standard
import datetime
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# custom
import python.lib.logger.mylogger
from .models.ResponseDTO import ResponseDTO
from python.lib.knowledgebase.knowledgebase import KnowledgeBase
import datetime
# create_kb()


from datetime import datetime


# dd/mm/YY H:M:S
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
knowledge_base = KnowledgeBase()
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
app = Flask(__name__)
CORS(app)

logging.info(f'Started flask app: {__name__}')


@app.route('/prove_1_goal', methods=['POST'])
def prove_1_goal():
    query = request.json['query']
    response = knowledge_base.prove_1_goal(query)
    return jsonify(ResponseDTO(200, response).to_dict())


@app.route('/prove_goal', methods=['POST'])
def prove_goal():
    query = request.json['query']
    response = knowledge_base.prove_goal(query)
    return jsonify(ResponseDTO(200, response).to_dict())

@app.route('/prove_custom_goal', methods=['POST'])
def prove_custom_goal():
    query = request.json['query']
    response = knowledge_base.prove_goal(query, True)
    return jsonify(ResponseDTO(200, response).to_dict())
