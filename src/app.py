from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from users import User
app = Flask(__name__)
app.secret_key = "1234"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Replace with the IP address of your ESP8266
DOORLOCK_IP = "http://192.168.1.12"  
LED_IP = "http://192.168.1.11"
TEMP_IP = "http://192.168.1.10"

@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(username)
        if user and User.check_password(username, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template('main.html', user=current_user)

@app.route('/sendTemp', methods=['POST'])
def sendTemp():
    temp = request.form.get('tempInput')
    if not temp:
        return "No integer value provided", 400
    try:
        temp = int(temp)
        response = requests.post(f"{TEMP_IP}/recieveTemp", data={'temp':temp})
        response.raise_for_status()
        return render_template('main.html')
    except requests.RequestException as e:
        return f"Failed to send: {e}", 500

@app.route('/sendDoorState', methods=['POST'])
def sendDoorState():
    doorState = request.form.get('doorState')
    if doorState:
        try:
            response = requests.get(f"{DOORLOCK_IP}/{doorState}")
            response.raise_for_status()
            return render_template('main.html')
        except requests.RequestException as e:
            return f"Failed to send command: {e}", 500

@app.route('/sendLightState', methods=['POST'])
def sendLightState():
    ledState = request.form.get('ledState')
    if ledState:
        try:
            response = requests.get(f"{LED_IP}/{ledState}")
            response.raise_for_status()
            return render_template('main.html')
        except requests.RequestException as e:
            return f"Failed to send command: {e}", 500

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
