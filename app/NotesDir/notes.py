from flask import Blueprint
from flask import jsonify, request
from flask_jwt import jwt_required, current_identity

from app import db
from app.NotesDir.c_notes import Note

#mod_note = Blueprint('note', __name__, url_prefix='/api')

mod_note = Blueprint('note', __name__)

@mod_note.route('/api/notes', methods=['GET'])
@jwt_required()
def getNotes():
    notes = Note.query.filter_by(user_id=current_identity.id).all()
    return jsonify(notes=[n.serialize() for n in notes]), 200

@mod_note.route('/api/notes', methods=['POST'])
@jwt_required()
def postNote():
    data = request.get_json(True)
    if data['title'] and data['content'] and current_identity.id:
        note = Note(data['title'], data['content'], data['category_id'], current_identity.id)
        db.session.add(note)
        db.session.commit()
        return jsonify(message="The note was created"), 201
    #if not current_identity.id:
    #    return jsonify(message="Unauthorized user"), 401
    return jsonify(message="The note has empty fields"), 400

@mod_note.route('/api/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def getNote(note_id):
    note = Note.query.filter_by(id=note_id).first()
    return jsonify(note.serialize()), 200

@mod_note.route('/api/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def deleteNote(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note and not note.is_owned_by(current_identity.id):
        return jsonify(message="You are allowed to delete only your notes"), 403
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify(message="The note was deleted"), 200
    return jsonify(message="Not found"), 404

