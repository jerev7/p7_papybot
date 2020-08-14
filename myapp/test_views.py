import myapp.views
import myapp.config
import json

def test_question_to_keyword_with article():
    assert myapp.views.question_to_keyword_with_article("Je voudrais savoir l'adresse d'Openclassrooms ?") == "d'Openclassrooms"

def test_remove_article_from_keyword():
   assert myapp.views.remove_article_from_keyword("d'Openclassrooms") == "Openclassrooms"

def substitute_func(self):
    myjson = '''{
               "results" : [
                  {
                     "address_components" : [
                        {
                           "long_name" : "7",
                           "short_name" : "7",
                           "types" : [ "street_number" ]
                        },
                        {
                           "long_name" : "Cité Paradis",
                           "short_name" : "Cité Paradis",
                           "types" : [ "route" ]
                        },
                        {
                           "long_name" : "Paris",
                           "short_name" : "Paris",
                           "types" : [ "locality", "political" ]
                        },
                        {
                           "long_name" : "Arrondissement de Paris",
                           "short_name" : "Arrondissement de Paris",
                           "types" : [ "administrative_area_level_2", "political" ]
                        },
                        {
                           "long_name" : "Île-de-France",
                           "short_name" : "IDF",
                           "types" : [ "administrative_area_level_1", "political" ]
                        },
                        {
                           "long_name" : "France",
                           "short_name" : "FR",
                           "types" : [ "country", "political" ]
                        },
                        {
                           "long_name" : "75010",
                           "short_name" : "75010",
                           "types" : [ "postal_code" ]
                        }
                     ],
                     "formatted_address" : "7 Cité Paradis, 75010 Paris, France",
                     "geometry" : {
                        "location" : {
                           "lat" : 48.8748465,
                           "lng" : 2.3504873
                        },
                        "location_type" : "ROOFTOP",
                        "viewport" : {
                           "northeast" : {
                              "lat" : 48.8761954802915,
                              "lng" : 2.351836280291502
                           },
                           "southwest" : {
                              "lat" : 48.8734975197085,
                              "lng" : 2.349138319708498
                           }
                        }
                     },
                     "place_id" : "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8",
                     "plus_code" : {
                        "compound_code" : "V9F2+W5 Paris, France",
                        "global_code" : "8FW4V9F2+W5"
                     },
                     "types" : [ "establishment", "point_of_interest" ]
                  }
               ],
               "status" : "OK"
            }'''
    return json.loads(myjson)["results"][0]

def test_get_adress(monkeypatch):
    monkeypatch.setattr(myapp.views.Map, 'get_adress', substitute_func)
    newmap = myapp.views.Map("Openclassrooms")
    assert newmap.adress_updated == "7 Cité Paradis, 75010 Paris, France"
    assert newmap.street == "Cité Paradis"

