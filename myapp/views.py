from flask import Flask, render_template, url_for, request, jsonify
import requests
import os

# Getting environment variables :
if os.environ.get('KEY') is None:
    from . import config
    KEY = config.KEY
else:
    KEY = os.environ.get('KEY')

#Create the app
app = Flask(__name__)

STOP_WORDS = ["a","abord","absolument","afin","ah","ai","aie","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aujourd","aujourd'hui","aupres","auquel","aura","auraient","aurait","auront","aussi","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avoir","avons","ayant","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","boum","bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","douze","douzième","dring","du","duquel","durant","dès","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","est","et","etant","etc","etre","eu","euh","eux","eux-mêmes","exactement","excepté","extenso","exterieur","f","fais","faisaient","faisant","fait","façon","feront","fi","flac","floc","font","g","gens","h","ha","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","minimale","moi","moi-meme","moi-même","moindres","moins","mon","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","plein","plouf","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","seraient","serait","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soit","soixante","son","sont","sous","souvent","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","superpose","sur","surtout","t","ta","tac","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","été","être","ô", "?", "'", "trouve", "situe", "situé"]

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


# def question_to_keyword(user_input):
#     """
#     Function used to keep only the key word from user's question
#     """
#     input_into_words = user_input.replace("'", " ' ").replace("Où", "où")
#     input_list = input_into_words.split(" ")
#     if "adresse" in input_list:
#         adress_index = input_list.index("adresse")
#         list_updating = input_list[adress_index + 1:]
#     elif "où" in input_list:
#         adress_index = input_list.index("où")
#         list_updating = input_list[adress_index + 1:]
#     else:
#         list_updating = input_list

#     list_updated = [i for i in list_updating if i not in STOP_WORDS] # We create a new list with all words in STOP_WORDS removed

#     keyword = " ".join(list_updated)
#     return keyword

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

    keyword_updating = keyword.replace("'", " ' ")
    keyword_list = keyword_updating.split(" ")
    key_word_updating2 = [i for i in keyword_list if i not in STOP_WORDS]
    key_word_updated = key_word_updating2[0]
    return key_word_updated

def create_papy_response(keyword_with_article):
    if keyword_with_article[0] == "l":
        return "Tout de suite mon petit. C'est simple, {} se trouve ".format(keyword_with_article)
    elif keyword_with_article[0] == "d":
        return "Tout de suite mon petit. C'est simple, l'adresse {} est ".format(keyword_with_article)





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