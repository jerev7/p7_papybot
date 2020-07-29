from . import views
from . import config

def test_question_to_keyword():
	assert views.question_to_keyword("Je voudrais savoir l'adresse d'Openclassrooms ?") == "Openclassrooms"

def test_map_attributes():
	mymap = views.Map("Openclassrooms")
	assert mymap.map_url == "https://www.google.com/maps/embed/v1/search?q=France+Openclassrooms" + "&key=" + config.key

def test_wiki_attributes():
	mywiki = views.Wikipedia_extract("Cité Paradis")