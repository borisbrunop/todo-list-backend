"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Usuario, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=["GET", "POST"])
def cr_user():
    body = request.json
    users = Usuario.query.all()
    if request.method == "GET":
        users_serialize = list(map(lambda user: user.serialize(), users))
        print(users_serialize)
        return jsonify(users_serialize), 200
    else:
        if body is None:
            return jsonify({
            "result": "nothing in body"
            }), 400
        if ("name" not in body):
            return jsonify({
            "result": "nothing in body"
            }), 400
        if (body["name"] == ""):
            return jsonify({
            "result": "nothing in body"
            }), 400
        
        new_user = Usuario.register(body["name"])
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify(new_user.serialize()), 201
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "result": f"{error.args}"
            }),500


@app.route('/task', methods=["POST"])
def cr_task():
    body = request.json
    if body is None:
        return jsonify({
        "result": "nothing in body"
        }), 400
    if (
        "label" not in body or
        "done" not in body or
        "usuario_id" not in body
        ):
        return jsonify({
        "result": "nothing in body"
        }), 400
    if (
        body["label"] == "" or
        body["done"] == "" or
        body["usuario_id"] == ""
        ):
        return jsonify({
        "result": "nothing in body"
        }), 400
    
    new_task = Task.register(
        body["label"],
        body["done"],
        body["usuario_id"]
        )
    db.session.add(new_task)
    try:
        db.session.commit()
        return jsonify(new_task.serialize()), 201
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        return jsonify({
            "result": f"{error.args}"
        }),500

@app.route('/task/<task_id>', methods=["DELETE"])
def d_task(task_id):
    task = Task.query.get(task_id)
    if isinstance(task, Task):
        db.session.delete(task)
        try:
            db.session.commit()
            return jsonify({}), 204
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "result": f"{error.args}"
            }), 500
    else:
        return jsonify({
            "result": "contact not here"
        }), 404

    #tasks_filter = filter(lambda task: user ,tasks)

@app.route('/user/<user_id>', methods=["GET","DELETE"])
def d_user(user_id):
    user = Usuario.query.get(user_id)
    if isinstance(user, Usuario):
        if request.method == "GET":
            return jsonify(user.serialize()), 200
        else:
            db.session.delete(user)
            try:
                db.session.commit()
                return jsonify({}), 204
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "result": f"{error.args}"
                }), 500
    else:
        return jsonify({
            "result": "contact not here"
        }), 404
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
