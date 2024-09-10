from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Time
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///booking.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Booking model/table class
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    table_type = db.Column(db.String(20), nullable=False)
    guest_number = db.Column(db.Integer, nullable=False)
    placement = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    note = db.Column(db.Text)

    def __repr__(self):
        return f"<Booking {self.first_name} {self.last_name} on {self.date}>"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        table_type = request.form['table_type']
        guest_number = int(request.form['guest_number'])
        placement = request.form['placement']
        date_str = request.form['date']  # Get date as string from form

        # Validate date format
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        time_str = request.form['time']  # Get time as string from form

        # Validate time format
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return "Invalid time format. Please use HH:MM (24-hour format)."

        note = request.form['note']

        # Create a new booking
        new_booking = Booking(
            first_name=first_name,
            last_name=last_name,
            email=email,
            table_type=table_type,
            guest_number=guest_number,
            placement=placement,
            date=date,
            time=time_obj,
            note=note
        )

        db.session.add(new_booking)
        db.session.commit()

        all_bookings = Booking.query.all()  # Get all bookings for the display
        return render_template('booking.html', all_booking=all_bookings)

    return render_template('booking.html')  # Render booking form on GET request

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

if __name__ == "__main__":
    app.run(debug=True)
