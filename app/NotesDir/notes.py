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
            and 'category_id' in data and len(data['category_id']) > 0 \
            and 'tag_id' in data and len(data['tag_id']) > 0:
        note = Note(data['title'], data['content'], data['category_id'], data['tag_id'], current_identity.id)
        db.session.add(note)
        db.session.commit()
        return jsonify(message="The note was created"), 201
    return jsonify(message="The note has empty fields"), 400

@mod_note.route('/api/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def getNote(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if note:
        return jsonify(note.serialize()), 200
    return jsonify(message="The note was not found"), 404

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
        return jsonify(status="Title is empty", note=note.serialize()), 400
    if 'content' in data and len(data['content']) > 0:
        note.content = data['content']
    else:
        return jsonify(status="Content is empty", note=note.serialize()), 400
    if 'category_id' in data and len(data['category_id']) > 0:
        note.category_id = data['category_id']
    else:
        return jsonify(status="Category_id is empty", note=note.serialize()), 400
    if 'tag_id' in data and len(data['tag_id']) > 0:
        note.tag_id = data['tag_id']
    else:
        return jsonify(status="Tag_id is empty", note=note.serialize()), 400

    db.session.commit()
    return jsonify(status="The note was updated", note=note.serialize()), 200

@mod_note.route('/api/categories/<int:category_id>', methods=['GET'])
@jwt_required()
def getNotesByCategory(category_id):
    notes = Note.query.filter_by(category_id=category_id).all()
    return jsonify(notes=[n.serialize() for n in notes]), 200

@mod_note.route('/api/tags/<int:tag_id>', methods=['GET'])
@jwt_required()
def getNotesByTag(tag_id):
    notes = Note.query.filter_by(tag_id=tag_id).all()
    return jsonify(notes=[n.serialize() for n in notes]), 200

