from app import app, db
from models import Attendee
import csv

def import_attendees(filename):
    with app.app_context():
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if the registration ID already exists
                exists = Attendee.query.filter_by(registration_id=row['registration_id']).first()
                if exists:
                    print(f"❌ Skipping duplicate: {row['registration_id']}")
                    continue

                attendee = Attendee(
                    full_name=row['full_name'],
                    email=row['email'],
                    phone=row['phone'],
                    ward=row['ward'],
                    stake=row['stake'],
                    registration_id=row['registration_id']
                )
                db.session.add(attendee)
            db.session.commit()
            print("✅ Import completed.")

import_attendees("attendees.csv")
