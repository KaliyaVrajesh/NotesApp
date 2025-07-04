from flask import Blueprint, render_template, request, flash, jsonify  # Import flash
from flask_login import login_required, current_user
from . import db
from .models import Note  # Import the Note model
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_text = request.form.get('note')  # Rename to avoid confusion

        if not note_text or len(note_text) < 1:  # Ensure note is valid
            flash("Note is too short", category='error')
        else:
            new_note = Note(data=note_text, user_id=current_user.id)  # Use Note model
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Parse the incoming JSON data
    noteId = note['noteId']  # Access 'noteId' from the parsed data

    # Fetch the note from the database using noteId
    note = Note.query.get(noteId)

    # Check if the note exists and belongs to the current user
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({"success": True})  # Return success if deletion is successful

    # If the note does not exist or the user is unauthorized
    return jsonify({"success": False, "message": "Note not found or unauthorized"})


