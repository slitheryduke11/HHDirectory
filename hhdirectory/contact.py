import requests
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
        email_sign_error = {"username": "@" in email_username, "domain": "@" in email_domain}
        # Check if necessary data is present
        if (not name or not lastname or not phone) or\
                (email_username and not email_domain or not email_username and email_domain) or\
                (email_sign_error["username"] or email_sign_error["domain"]):
            return render_template("contact/create.html", previous_data=request.form, email_sign_error=email_sign_error, error=True)
        if email_username or email_domain:
            email = email_username + "@" + email_domain # Format email
        address = request.form["address"] if request.form["address"] else None
        favorite = 1 if 'favorite' in request.form else 0
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


@bp.route("/contact/<contact_id>/delete/", methods=("POST",))
def delete(contact_id):
    """Delete a contact."""
    # Remove contact from database
    db = get_db()
    db.execute(
        "DELETE FROM contact"
        " WHERE id = ?",
        (contact_id,),
    )
    db.commit()
    return redirect(url_for("contact.index"))


@bp.route("/contact/<contact_id>/edit/", methods=("GET", "POST"))
def edit(contact_id):
    """Edit a new contact."""
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
    # Edit contact
    if request.method == "POST":
        # Get data from form
        name = request.form["name"]
        lastname = request.form["lastname"]
        phone = request.form["phone"]
        email_username = request.form["email_username"]
        email_domain = request.form["email_domain"]
        email = None
        email_sign_error = {"username": "@" in email_username, "domain": "@" in email_domain}
        # Check if necessary data is present
        if (not name or not lastname or not phone) or\
                (email_username and not email_domain or not email_username and email_domain) or\
                (email_sign_error["username"] or email_sign_error["domain"]):
            return render_template("contact/create.html", previous_data=request.form, email_sign_error=email_sign_error, error=True)
        if email_username or email_domain:
            email = email_username + "@" + email_domain # Format email
        address = request.form["address"] if request.form["address"] else None
        favorite = 1 if 'favorite' in request.form else 0
        # Add contact to database
        db = get_db()
        db.execute(
            "UPDATE contact "
            " SET name = ?, lastname= ?, phone= ?, email= ?, address= ?, favorite= ?"
            " WHERE id = ?",
            (name, lastname, phone, email, address, favorite, contact_id),
        )
        db.commit()
        return redirect(url_for("contact.detail", contact_id=contact_id))
    # Show form to edit contact
    return render_template("contact/edit.html", contact=contact)


@bp.route("/public-data/")
def get_public_data():
    """Show public data from randomuser.me API."""
    url = "https://randomuser.me/api/"
    # Parameters for API request
    params = {
        "nat": "US",  
        "results": 10,
    }
    # Get data from API
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            persons = data["results"]
            contacts = []
            for person in persons:
                contact = {
                    "name": person["name"]["first"],
                    "lastname": person["name"]["last"],
                    "email": person["email"],
                    "address": person["location"]["street"]["number"]
                }
                contacts.append(contact)
        error = False
    # Handle errors
    except requests.exceptions.RequestException as e:
        error = "Service temporarily unavailable."
    return render_template("contact/public_data.html", contacts=contacts, error=error)
