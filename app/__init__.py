from flask import Flask, jsonify
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from app import config

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# import blueprints
from app.UserDir.user import mod_auth, authenticate, identity
app.register_blueprint(mod_auth)
from app.NotesDir import note_module
app.register_blueprint(note_module)

app.debug = True
db.create_all()

jwt = JWT(app, authenticate, identity)

@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Not found"), 404

if __name__ == '__main__':
    app.run()

