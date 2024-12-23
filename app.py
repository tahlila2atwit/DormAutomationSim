from flask import Flask, render_template, request

app = Flask(__name__)

# Initial states
light_state = "Off"
door_state = "Unlocked"
temperature = "70"

@app.route("/", methods=["GET", "POST"])
def index():
    global light_state, door_state, temperature
    if request.method == "POST":
        if "toggle_light" in request.form:
            # Toggle light state
            light_state = "On" if light_state == "Off" else "Off"
        elif "toggle_door" in request.form:
            # Toggle door state
            door_state = "Locked" if door_state == "Unlocked" else "Unlocked"
        
        # Get the temperature input
        temperature = request.form.get("temperature_field", "")
        print(f"light state: {light_state}\nDoor State: {door_state}\nTemperature: {temperature}")
    return render_template("index.html", light_state=light_state, door_state=door_state, temperature=temperature)

if __name__ == "__main__":
    app.run(debug=True)
