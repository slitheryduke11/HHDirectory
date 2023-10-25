from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from hhdirectory.db import get_db

bp = Blueprint("contact", __name__)


@bp.route("/")
def index():
    """Show all the contacts, ordered by name."""
    db = get_db()
    contacts = db.execute(
        "SELECT id, name, lastname, phone, favorite"
        " FROM contact"
        " ORDER BY name ASC"
    ).fetchall()
    return render_template("contact/index.html", contacts=contacts)


@bp.route("/create/", methods=("GET", "POST"))
def create():
    """Create a new contact."""
    # Create contact
    if request.method == "POST":
        # Get data from form
        name = request.form["name"]
        lastname = request.form["lastname"]
        phone = request.form["phone"]
        email_username = request.form["email_username"]
        email_domain = request.form["email_domain"]
        email = None
        # Check if necessary data is present
        if not name or not lastname or not phone:
            return render_template("contact/create.html", previous_data=request.form, error=True)
        if email_username and email_domain:
            email = email_username + "@" + email_domain # Format email
        address = request.form["address"]
        if 'favorite' in request.form:
            favorite = 1 if request.form["favorite"] else 0
        # Add contact to database
        db = get_db()
        db.execute(
            "INSERT INTO contact (name, lastname, phone, email, address, favorite)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (name, lastname, phone, email, address, favorite),
        )
        db.commit()
        return redirect(url_for("contact.index"))
    # Show form to create contact
    return render_template("contact/create.html")


@bp.route("/favorites/")
def show_favorites():
    """Show only favorite contacts, ordered by name."""
    db = get_db()
    contacts = db.execute(
        "SELECT id, name, lastname, phone, favorite"
        " FROM contact"
        " WHERE  favorite = 1"
        " ORDER BY name ASC"
    ).fetchall()
    return render_template("contact/favorites.html", contacts=contacts)


@bp.route("/contact/<contact_id>/")
def detail(contact_id):
    """Show detail of a contact."""
    # Get contact from database
    db = get_db()
    contact = db.execute(
        "SELECT id, name, lastname, phone, email, address, favorite"
        " FROM contact"
        " WHERE id = ?",
        (contact_id,),
    ).fetchone()
    # Check if contact exists
    if not contact:
        return redirect(url_for("contact.index"))
    return render_template("contact/detail.html", contact=contact)
