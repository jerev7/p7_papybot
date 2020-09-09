from flask import Flask, render_template, url_for, request, jsonify
import requests
import os
import csv

# Getting environment variables :
if os.environ.get('KEY') is None:
    from . import config
    KEY = config.KEY
else:
    KEY = os.environ.get('KEY')

#Create the app
app = Flask(__name__)

stop_words = []
with open('myapp/stop_words.csv') as f:
    reader = csv.reader(f)
    # data = f.readlines()
    for row in reader:
        stop_words.append(row[0])
    stop_words.pop(0)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html',
                            logo_img=url_for('static', filename="images/robot.jpg"))

@app.route('/backend_process')
def backend_process():
    """
    We get user's input and send all data updated to our javscript script
    """
    user_input = request.args.get('note')
    keyword_with_article = question_to_keyword_with_article(user_input)
    papy_response = create_papy_response(keyword_with_article)
    keyword_only = remove_article_from_keyword(keyword_with_article)
    my_map = Map(keyword_only)
    adress = my_map.adress_updated
    street = my_map.street
    map_url = my_map.map_url
    my_wiki = Wikipedia_extract(street)
    wiki_extract = my_wiki.extract
    wiki_link = "https://fr.wikipedia.org/wiki/" + street
    
    return jsonify(papy_response=papy_response, map_url=map_url, adress=adress, wiki_extract=wiki_extract, wiki_link=wiki_link)


def question_to_keyword_with_article(user_input):
    """
    Function used to keep only keyword with its article from user's question
    """
    input_into_words = user_input.replace("'", " ' ").replace("Où", "où").replace(" ?", "")
    input_list = input_into_words.split(" ")
    if "adresse" in input_list:
        adress_index = input_list.index("adresse")
        list_updating = input_list[adress_index + 1:]
    elif "où" in input_list:
        first_index = input_list.index("où")
        list_updating_first = input_list[first_index + 1:]
        words_to_remove = ["est", "situé", "se", "situe", "trouve"]
        list_updating = [i for i in list_updating_first if i not in words_to_remove]
    else:
        list_updating = input_list
    keyword_with_article_updating = " ".join(list_updating)
    keyword_with_article = keyword_with_article_updating.replace(" ' ", "'")
    return keyword_with_article

def remove_article_from_keyword(keyword):
    """
    Function used to remove the articles before the keyword
    """
    keyword_updating = keyword.replace("'", " ' ")
    keyword_list = keyword_updating.split(" ")
    key_word_updating2 = [i for i in keyword_list if i not in stop_words]
    key_word_updated = " ".join(key_word_updating2)
    return key_word_updated

def create_papy_response(keyword_with_article):
    """
    Function used to create the first sentence that Papybot will say
    """
    if keyword_with_article[0] == "d":
        return "Tout de suite mon petit. C'est simple, l'adresse {} est ".format(keyword_with_article)
    else:
        return "Tout de suite mon petit. C'est simple, {} se trouve ".format(keyword_with_article)




class Map():
    """
    This class will make requests to Google API to update all data we need
    """
    def __init__(self, keyword):
        self.keyword = keyword
        result_get_adress = self.get_adress()
        self.adress_updated = result_get_adress["formatted_address"]
        self.street = keyword # if there is no street we gonna keep the keyword to do wikipdedia search
        for i in range(0, 5):
            if result_get_adress["address_components"][i]["types"][0] == "route":
                street_key = i
                self.street = result_get_adress["address_components"][street_key]["long_name"] # We get the street name
        self.map_url = "https://www.google.com/maps/embed/v1/search?q=France+" + keyword + "&key=" + KEY # this is the map which will be showed below the discussion with Papybot

    def get_adress(self):
        """
        Function which make the request to google API and give a first result to constructor
        """
        keyword = self.keyword.replace(" ", "+")
        r = requests.get("https://maps.google.com/maps/api/geocode/json?address=France+" + keyword + "&sensor=false&key=" + KEY)
        return r.json()["results"][0]


class Wikipedia_extract():
    """
    This class will make requests to Wikipedia API
    """
    def __init__(self, street):
        r = requests.get("https://fr.wikipedia.org/api/rest_v1/page/summary/" + street)
        if r.json()["title"] ==  "Not found.": # If wikipedia doesn't find anything about the street, we provide a response
            self.extract = "Hmmmmm.... {} ... Cette rue me dis quelque chose mais ma mémoire me joue des tours on dirait... Pose moi une autre question s'il te plait...".format(street)
        else:
            self.extract = r.json()["extract"]