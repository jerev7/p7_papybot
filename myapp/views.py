from flask import Flask, render_template, url_for, request, jsonify
import requests
from . import config

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html',
                            logo_img=url_for('static', filename="images/robot.jpg"))

@app.route('/backend_process')
def backend_process():
    user_input = request.args.get('note')
    keyword = question_to_keyword(user_input)
    my_map = Map(keyword)
    adress = my_map.adress_updated
    street = my_map.street
    map_url = my_map.map_url
    my_wiki = Wikipedia_extract(street)
    wiki_extract = my_wiki.extract
    wiki_link = "https://fr.wikipedia.org/wiki/" + street
    
    return jsonify(map_url=map_url, adress=adress, wiki_extract=wiki_extract, keyword=keyword, wiki_link=wiki_link)


def question_to_keyword(user_input):
    input_into_words = user_input.replace("'", " ' ")
    input_list = input_into_words.split(" ")
    list_updating = [i for i in input_list if i not in config.STOP_WORDS]
    if "adresse" in list_updating:
        adress_index = list_updating.index("adresse")
        list_updated = list_updating[adress_index + 1:]
    else:
        list_updated = list_updating
    keyword = " ".join(list_updated)
    return keyword



class Map():
    
    def __init__(self, keyword):
        self.keyword = keyword
        result_get_adress = self.get_adress()
        self.adress_updated = result_get_adress["formatted_address"]
        self.street = result_get_adress["address_components"][1]["long_name"]
        self.map_url = "https://www.google.com/maps/embed/v1/search?q=France+" + keyword + "&key=" + config.key

    def get_adress(self):
        keyword = self.keyword.replace(" ", "+")
        r = requests.get("https://maps.google.com/maps/api/geocode/json?address=France+" + keyword + "&sensor=false&key=" + config.key)
        return r.json()["results"][0]



class Wikipedia_extract():
    
    def __init__(self, street):
        r = requests.get("https://fr.wikipedia.org/api/rest_v1/page/summary/" + street)
        self.extract = r.json()["extract"]