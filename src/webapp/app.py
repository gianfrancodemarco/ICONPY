# set FLASK_ENV=development
# set FLASK_APP=app.py
# flask run

import os
import sys

module_path = os.path.abspath(os.path.join('../..'))
sys.path.append(module_path)

# standard
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

# custom
from src.lib.logger.mylogger import *
from src.webapp.models.ResponseDTO import ResponseDTO
from src.lib.knowledgebase.knowledgebase import KnowledgeBase
from datetime import datetime

# dd/mm/YY H:M:S
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
knowledge_base = KnowledgeBase()
print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
app = Flask(__name__)
CORS(app)

logging.info(f'Started flask app: {__name__}')

knowledge_base.prove_goal('acted(\"Harry Potter and the Goblet of Fire\",\"Daniel Radcliffe\")')

@app.route('/prove_1_goal', methods=['POST'])
def prove_1_goal() -> Response:
    query = request.json['query']
    response: ResponseDTO = knowledge_base.prove_1_goal(query)
    return jsonify(response.to_dict())


@app.route('/prove_goal', methods=['POST'])
def prove_goal() -> Response:
    query = request.json['query']
    response: ResponseDTO = knowledge_base.prove_goal(query)
    return jsonify(response.to_dict())

# @app.route('/prove_custom_goal', methods=['POST'])
# def prove_custom_goal():
#     query = request.json['query']
#     response = knowledge_base.prove_goal(query, True)
#     return jsonify(ResponseDTO(200, response).to_dict())
