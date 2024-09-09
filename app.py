from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/booking')
def booking_page():
    return render_template('booking.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

if __name__ == "__main__":
    app.run(debug=True)
