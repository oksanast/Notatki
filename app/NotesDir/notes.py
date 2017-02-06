from flask import Blueprint
from flask import jsonify, request
from flask_jwt import jwt_required, current_identity

from app import db
from app.NotesDir.c_notes import Note

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
    if 'title' in data and len(data['title']) > 0 \
            and 'content' in data and len(data['content']) > 0 \
            and 'category' in data and len(data['category']) > 0 \
            and 'tag' in data and len(data['tag']) > 0:
        note = Note(data['title'], data['content'], data['category'], data['tag'], current_identity.id)
        db.session.add(note)
        db.session.commit()
        # print(data['tag'])
        return jsonify(message="The note was created", note=note.serialize()), 201
    return jsonify(message="The note has empty fields"), 400

@mod_note.route('/api/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def getNote(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note and note.getUserId() == current_identity.id:
        return jsonify(note.serialize()), 200
    if not note:
        return jsonify(message="The note was not found"), 404
    return jsonify(message="You are allowed to view only your notes"), 403

@mod_note.route('/api/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def deleteNote(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note and not note.getUserId() == current_identity.id:
        return jsonify(message="You are allowed to delete only your notes"), 403
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify(message="The note was deleted"), 200
    return jsonify(message="The note was not found"), 404

@mod_note.route('/api/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def updateNote(note_id):
    data = request.get_json(True)
    note = Note.query.filter_by(id=note_id).first()
    if not note:
        return jsonify(status="The note was not found"), 404
    if note and not note.getUserId() == current_identity.id:
        return jsonify(message="You are allowed to update only your notes"), 403
    if 'title' in data and len(data['title']) > 0:
        note.title = data['title']
    else:
        return jsonify(message="The title of the note is empty"), 400
    if 'content' in data and len(data['content']) > 0:
        note.content = data['content']
    else:
        return jsonify(message="The content of the note is empty"), 400
    if 'category' in data and len(data['category']) > 0:
        note.category = data['category']
    else:
        return jsonify(message="The category of the note is empty"), 400
    if 'tag' in data and len(data['tag']) > 0:
        note.tag = data['tag']
    else:
        return jsonify(message="The tag of the note is empty"), 400

    db.session.commit()
    return jsonify(message="The note was updated", note=note.serialize()), 200

@mod_note.route('/api/categories/<category>', methods=['GET'])
@jwt_required()
def getNotesByCategory(category):
    notes = Note.query.filter_by(category=category, user_id=current_identity.id).all()
    return jsonify(notes=[n.serialize() for n in notes]), 200

@mod_note.route('/api/tags/<tag>', methods=['GET'])
@jwt_required()
def getNotesByTag(tag):
    notes = Note.query.filter_by(user_id=current_identity.id).all()
    allNotes = []
    for n in notes:
        if "'" + tag + "'" in n.tag:
            allNotes.append(n)
    return jsonify(notes=[n.serialize() for n in allNotes]), 200


