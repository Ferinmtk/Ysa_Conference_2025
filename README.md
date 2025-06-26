# YSA 2025 Attendee Management System

A Flask-based web application for managing and tracking attendee information, check-ins, and attendance during the YSA 2025 Conference. Includes admin functionality for viewing attendees by stake and ward, manual attendee entry and CSV export.

---

##  Features

- View attendees grouped by Stake and Ward
- Toggle display by stake for easier navigation
- Real-time search and filtering
- Check-in and check-out buttons for each attendee
- Individual day attendance tracking (Day 1, Day 2, Day 3)
- Add new attendees via form
- Dynamic stake-to-ward dropdowns
- Flash messages for success/error
- CSV export functionality
- Flashy modern UI with responsive design

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL (via SQLAlchemy ORM)
- **Styling:** Custom CSS + Google Fonts (`Poppins`)
- **Export:** CSV generation in-browser
- **Flash Messaging:** Flask's built-in `flash()`

---

##  Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone https://github.com/ferinmtk/ysa2025-attendance.git
   cd ysa2025-attendance
