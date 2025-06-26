from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from collections import defaultdict
from models import db, Attendee
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db BEFORE importing models
from models import db, Attendee
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "<h1>Welcome to YSA 2025 Check-in System</h1>"



@app.route("/admin")
def admin_panel():
    all_attendees = Attendee.query.order_by(Attendee.stake, Attendee.ward, Attendee.full_name).all()

    for attendee in all_attendees:
        if isinstance(attendee.attendance, str):
            try:
                attendee.attendance = json.loads(attendee.attendance)
            except json.JSONDecodeError:
                attendee.attendance = {}
        elif attendee.attendance is None:
            attendee.attendance = {}

    grouped_attendees = defaultdict(lambda: defaultdict(list))
    for attendee in all_attendees:
        grouped_attendees[attendee.stake][attendee.ward].append(attendee)

    return render_template("admin.html", grouped_attendees=grouped_attendees)

@app.route("/checkin/<registration_id>", methods=["POST"])
def check_in(registration_id):
    attendee = Attendee.query.filter_by(registration_id=registration_id).first()
    if attendee:
        today = datetime.now()
        
        # Default to an empty dict if attendance is None
        if attendee.attendance is None:
            attendee.attendance = {}
        
        # Convert string keys like "day_1" if needed
        attendee.attendance["manual_checkin"] = today.isoformat()

        # Update time_in for logging purposes
        attendee.time_in = today

        db.session.commit()
    return redirect(url_for('admin_panel'))



@app.route("/checkout/<registration_id>", methods=["POST"])
def check_out(registration_id):
    attendee = Attendee.query.filter_by(registration_id=registration_id).first()
    if attendee:
        attendee.time_out = datetime.now()
        db.session.commit()
    return redirect(url_for('admin_panel'))




@app.route("/checkin_day/<registration_id>/<int:day_number>", methods=["POST"])
def checkin_day(registration_id, day_number):
    from datetime import datetime
    import json

    attendee = Attendee.query.filter_by(registration_id=registration_id).first()
    if attendee:
        key = f"day_{day_number}"

        # Normalize attendance to a dict
        if isinstance(attendee.attendance, str):
            try:
                attendee.attendance = json.loads(attendee.attendance)
            except json.JSONDecodeError:
                attendee.attendance = {}
        elif attendee.attendance is None:
            attendee.attendance = {}

        # Toggle: remove if exists, else add
        if key in attendee.attendance:
            del attendee.attendance[key]  # Uncheck
        else:
            attendee.attendance[key] = datetime.now().isoformat()  # Check

        # Save as JSON string
        db.session.query(Attendee).filter_by(id=attendee.id).update({
            Attendee.attendance: json.dumps(attendee.attendance)
        })
        db.session.commit()

    return redirect(url_for('admin_panel'))


@app.route("/attendance_day/<int:day_number>")
def attendance_day(day_number):
    from datetime import date, timedelta

    event_start = date(2025, 6, 24)
    target_day = event_start + timedelta(days=day_number - 1)
    target_day_str = target_day.isoformat()

    key = f"day_{day_number}"

    attendees = Attendee.query.order_by(Attendee.full_name).all()
    checked_in = []
    not_checked_in = []

    for attendee in attendees:
        if attendee.attendance and key in attendee.attendance:
            checked_in.append(attendee)
        else:
            not_checked_in.append(attendee)

    return render_template("attendance_day.html",
                           day_number=day_number,
                           checked_in=checked_in,
                           not_checked_in=not_checked_in,
                           target_day=target_day_str)




@app.route("/add", methods=["GET", "POST"])
def add_attendee():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        ward = request.form["ward"]
        stake = request.form["stake"]
        registration_id = request.form["registration_id"].strip().upper()

        # Normalize for uniqueness
        existing = Attendee.query.filter_by(registration_id=registration_id).first()
        if existing:
            flash("⚠️ That Registration ID already exists.", "error")
            return redirect(url_for("add_attendee"))

        try:
            new_attendee = Attendee(
                full_name=full_name.strip(),
                email=email.strip(),
                phone=phone.strip(),
                ward=ward.strip().title(),
                stake=stake.strip().title(),
                registration_id=registration_id
            )
            db.session.add(new_attendee)
            db.session.commit()
            flash("✅ Attendee added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("🚫 Error adding attendee. Please check your input or try again.", "error")
            print(str(e))  # Optional: log error
        return redirect(url_for("add_attendee"))

    return render_template("add_attendee.html")
