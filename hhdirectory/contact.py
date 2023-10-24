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
