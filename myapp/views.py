from flask import Flask, render_template, url_for, request, jsonify

#key=API_KEY
#apikey = AIzaSyB5XuF2yL6oKsm_EEWVjM_CGMEMIVogVVw
#https://www.google.com/maps/embed/v1/MODE?key=YOUR_API_KEY&parameters

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html',
							logo_img=url_for('static', filename="images/robot.jpg"))

# route to get data and work on them backend
@app.route('/backend_process')
def backend_process():
	my_note = request.args.get('note')
	new_note = (my_note.replace(" ", "+"))
	google_map_url = "https://www.google.com/maps/embed/v1/search?q=" + new_note + "&key=AIzaSyB5XuF2yL6oKsm_EEWVjM_CGMEMIVogVVw"
	return jsonify(backend_result = google_map_url)


#"https://www.google.com/maps/embed/v1/search?q=7+rue+du+chêne+vert&key=AIzaSyB5XuF2yL6oKsm_EEWVjM_CGMEMIVogVVw
