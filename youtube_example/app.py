import sqlalchemy as db

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from core.config import CommonSettings

app = Flask(__name__)

url_db = CommonSettings().DB.DSN

engine = create_engine(url_db)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine),
)

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

tutorials = [
    {
        'id': 1,
        'title': 'title1',
        'description': 'descriprion1'
    },
    {
        'id': 2,
        'title': 'title2',
        'description': 'descriprion2'
    },
]


@app.route('/tutorials', methods=['GET'])
def get_list():
    videos = Video.query.all()
    serialised = []
    for video in videos:
        serialised.append({
            'id': video.id,
            'name': video.name,
            'description': video.description,
        })
    return jsonify(serialised)


@app.route('/tutorials', methods=['POST'])
def update_list():
    new_one = Video(**request.json)
    session.add(new_one)
    session.commit()
    return {
        'id': new_one.id,
        'name': new_one.name,
        'description': new_one.description,
    }


@app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
def update_tutorial(tutorial_id):
    item = Video.query.get(tutorial_id)
    params = request.json
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
    }


@app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
def drop_tutorial(tutorial_id):
    item = Video.query.get(tutorial_id)
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)
