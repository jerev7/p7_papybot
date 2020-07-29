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
    # removing stop words from question :
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
    print(input_into_words)
    input_list = input_into_words.split(" ")
    list_updating = [i for i in input_list if i not in config.STOP_WORDS]
    print(list_updating)
    if "adresse" in list_updating:
        adress_index = list_updating.index("adresse")
        list_updated = list_updating[adress_index + 1:]
    else:
        list_updated = list_updating
    keyword = " ".join(list_updated)
    print(keyword)
    return keyword



class Map():
    
    def __init__(self, keyword):
        self.keyword = keyword.replace(" ", "+")
        r = requests.get("https://maps.google.com/maps/api/geocode/json?address=France+" + self.keyword + "&sensor=false&key=" + config.key)
        self.adress_updated = r.json()["results"][0]["formatted_address"]
        self.street = r.json()["results"][0]["address_components"][1]["long_name"]
        self.map_url = "https://www.google.com/maps/embed/v1/search?q=France+" + keyword + "&key=" + config.key


class Wikipedia_extract():
    
    def __init__(self, street):
        r = requests.get("https://fr.wikipedia.org/api/rest_v1/page/summary/" + street)
        self.extract = r.json()["extract"]

#"https://www.google.com/maps/embed/v1/search?q=7+rue+du+chêne+vert&key=
#https://maps.google.com/maps/api/geocode/json?address=Openclassrooms&sensor=false&key=

# @app.route('/backend_process')
# def backend_process():
#     # removing stop words from question :
#     my_note = request.args.get('note')
#     new_note1 = my_note.replace("'", " ' ")
#     print(new_note1)
#     note_list = new_note1.split(" ")
#     for element in note_list:
#         if element in config.STOP_WORDS:
#             note_list.remove(element)
#     # keeping only what's come after the word 'adresse' :
#     print(note_list)
#     if "adresse" in note_list:
#         adress_index = note_list.index("adresse")
#         new_list = note_list[adress_index + 1:]
#     else:
#         new_list = note_list
#     # setting up the google map url
#     note_str = " ".join(new_list)
#     new_note2 = (note_str.replace(" ", "+"))
#     google_map_url = "https://www.google.com/maps/embed/v1/search?q=France+" + new_note2 + "&key=" + config.key
#     print(google_map_url)
#     geocode_json = "https://maps.google.com/maps/api/geocode/json?address=France+" + new_note2 + "&sensor=false&key=" + config.key
#     print("adresse geocode : " + geocode_json)
#     return jsonify(backend_result_embedmap = google_map_url, backend_result_geocodejson = geocode_json, key_word = new_note2.replace("+", " "))
