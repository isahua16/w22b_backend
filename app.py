from dbhelpers import run_statement
from dbcreds import production_mode
from apihelpers import check_data
from flask import Flask, request, make_response, jsonify
import uuid

app = Flask(__name__)

@app.post('/api/client')
def next_client():
    error = check_data(request.json, ['username', 'email', 'password', 'image_url', 'bio'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call new_client(?,?,?,?,?)', [request.json.get('username'), request.json.get('email'), request.json.get('password'), request.json.get('image_url'), request.json.get('bio')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

@app.post('/api/login')
def new_login():
    error = check_data(request.json, ['username', 'password'])
    if(error != None):
        return make_response(jsonify(error), 400)
    token = uuid.uuid4().hex
    results = run_statement('call new_login(?,?,?)', [request.json.get('username'), request.json.get('password'), token])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)
    
@app.get('/api/client')
def get_client():
    error = check_data(request.args, ['token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_client(?)', [request.args.get('token')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

@app.delete('/api/login')
def delete_login():
    error = check_data(request.json, ['token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call delete_login(?)', [request.json.get('token')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

if(production_mode == True):
    print('Running in production mode')
    import bjoern # type: ignore
    bjoern.run(app, '0.0.0.0', 5000)
else:
    print('Running in development mode')
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
    CORS(app)
