from flask import Flask, render_template, url_for, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html',
							logo_img=url_for('static', filename="images/robot.jpg"))

# route to get data and work on them backend
@app.route('/backend_process')
def backend_process():
	my_note = request.args.get('note', 0, type=str)
	if my_note != "":
		return jsonify(backend_result = 'votre question est : ' + my_note)
	else:
		return jsonify(backend_result="vous n'avez rien écrit dans la case imbécile")
