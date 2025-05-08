from flask import Blueprint, request,jsonify
from app.models.note import Note
from app import db
import traceback



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

        
    
        
    


    
