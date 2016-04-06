# CSH Superlatives Main

from database import init_db

from flask import Flask, jsonify, request
import json
import sys

json_config = None

app = Flask(__name__)

eboard = \
    [
        'ajgajg1134',
        'com6056',
        'faokryn',
        'henry',
        'jeid',
        'maxime',
        'mbillow',
        'rosehacker',
        'victoria'
    ]

rtps = \
    [
        'com6056',
        'dgonyeo',
        'ehouse',
        'jeid',
        'loothelion',
        'mbillow',
        'rbuzzell',
        'robgssp',
        'rossdylan',
        'slackwill'
    ]

@app.route('/')
def hi():
    return jsonify({'message':"hi"})

@app.route('/people')
def list_people():
    import models
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.all()]
    return jsonify({'people': people})

@app.route('/rtps')
def list_rtps():
    import models
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.filter(
                    models.Person.uid.in_(rtps))]
    return jsonify({'people': people})

@app.route('/eboard')
def list_eboard():
    import models
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.filter(
                    models.Person.uid.in_(eboard))]
    return jsonify({'people': people})


#   Accepts a json post
#
#   answers is an array of integers
#   associating people with IDs
#
@app.route('/submit', methods=['POST'])
def submit():
    import models

    from database import db_session
    #ensure webauth user hasn't already submitted
    username = request.headers.get('x-webauth-user')
    voted = models.Person.query.filter(
                models.Person.uid == username
            ).first().voted

    if voted:
        return jsonify({'error': "already voted"})


    answers = request.get_json()['answers']

    # Only vote once
    models.Person.query.filter(
        models.Person.uid == username).\
        update({"voted": True})

    db_session.add(models.SuperlativeVote(answers))
    db_session.flush()
    db_session.commit()

    return jsonify({'status': "ok"})

with open(sys.argv[1]) as config_file:
    json_config = json.load(config_file)

    init_db(json_config['db']['url'])

    app.run(**json_config['flask'])