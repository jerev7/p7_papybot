from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html',
							logo_img=url_for('static', filename="images/robot.jpg",
							script_js=url_for('static', filename="js/script.js")))