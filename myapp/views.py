from flask import Flask, render_template, url_for, request, jsonify
from . import config

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html',
							logo_img=url_for('static', filename="images/robot.jpg"))

# route to get data and work on them backend
@app.route('/backend_process')
def backend_process():
	# removing stop words from question :
	my_note = request.args.get('note')
	new_note1 = my_note.replace("'", " ' ")
	print(new_note1)
	note_list = new_note1.split(" ")
	for element in note_list:
		if element in config.STOP_WORDS:
			note_list.remove(element)
	# keeping only what's come after the word 'adresse' :
	print(note_list)
	if "adresse" in note_list:
		adress_index = note_list.index("adresse")
		new_list = note_list[adress_index + 1:]
	else:
		new_list = note_list
	# setting up the google map url
	note_str = " ".join(new_list)
	new_note2 = (note_str.replace(" ", "+"))
	google_map_url = "https://www.google.com/maps/embed/v1/search?q=France+" + new_note2 + "&key=" + config.key
	print(google_map_url)
	geocode_json = "https://maps.google.com/maps/api/geocode/json?address=France+" + new_note2 + "&sensor=false&key=" + config.key
	print("adresse geocode : " + geocode_json)
	return jsonify(backend_result_embedmap = google_map_url, backend_result_geocodejson = geocode_json, key_word = new_note2.replace("+", " "))


#"https://www.google.com/maps/embed/v1/search?q=7+rue+du+chêne+vert&key=
#https://maps.google.com/maps/api/geocode/json?address=Openclassrooms&sensor=false&key=
