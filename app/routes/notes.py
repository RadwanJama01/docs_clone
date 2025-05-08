from flask import Blueprint, request,jsonify
from app.models.note import Note
from app import db
import traceback
from app.models.user import User  



note_bp = Blueprint('note',__name__)


@note_bp.route('/note/create', methods=["POST"])
def create_note():
    data = request.get_json()
    print("📥 Incoming data:", data)
    note_id = data.get('id')
    owner_id = data.get('owner')
    title = data.get('title', '')
    content = data.get('content', '')

    if not owner_id:
        return jsonify({'message': 'Missing owner'}), 400

  
    
    try:
         
        new_note = Note(
            id=note_id,
            title=title,
            content=content,
            owner_id=owner_id
        )
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'message': 'Note created successfully!', 'id': new_note.id}), 201
    except Exception as e:
        with open("error_log.txt", "w") as f:
            traceback.print_exc(file=f)
        print("🔥 ERROR CREATING NOTE:", e)
        return jsonify({'message': 'Internal server error'}), 500


@note_bp.route('/note/<int:note_id>/delete', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': f'Note {note_id} deleted successfully'}), 200
    except Exception as e:
        print(f"ERRORRR AS {e}")
        return jsonify({"message": "Server error"}), 500

@note_bp.route('/note/<int:note_id>', methods = ['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)  

    if not note:
        return jsonify({'message': 'Note_ID not found'}), 404
    
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'owner_id': note.owner_id,
        'created_at': str(note.created_at)
    }), 200
    
@note_bp.route('/note/<int:note_id>/update', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404

    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)

    try:
        db.session.commit()
        return jsonify({'message': f'Note {note_id} updated'}), 200
    except Exception as e:
        print(f"Update Error: {e}")
        return jsonify({'message': 'Update failed'}), 500
    
    
@note_bp.route('/note/<int:note_id>/collaborators', methods=['POST'])
def add_collaborator(note_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing or invalid JSON body'}), 400
    collaborator_id = data.get('user_id')
    note = Note.query.get(note_id)
    
    if not note or not collaborator_id:
        return jsonify({'message': 'Missing note or user'}), 400

    user = User.query.get(collaborator_id)
    if not user:
        return jsonify({'message': 'Collaborator not found'}), 404
    if user in note.collaborators:
        return jsonify({'message': 'User is already a collaborator'}), 409
    note.collaborators.append(user)
    db.session.commit()
    return jsonify({'message': f'Added collaborator {user.username} to note {note_id}'}), 200

@note_bp.route('/notes', methods=['GET'])
def all_notes():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'message': 'Missing user header'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    owned = Note.query.filter_by(owner_id=user_id).all()
    shared = user.collaborations  # comes from the backref

    all_notes = owned + shared

    return jsonify([{
        'id': n.id,
        'title': n.title,
        'content': n.content
    } for n in all_notes]), 200


    


    
