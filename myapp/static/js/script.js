// $(document).ready(function() {
//     $("#submit_button").on( 'click', function (event) {
//     	// event.preventDefault();
//     	var $mynote = $("#note").val();
//     	if ($mynote != "") {
//     		event.preventDefault();
//     		alert("Voilà votre question très intéressante :\n" + $mynote)
//     	};
//     });
// });

function updateQuestion(route) {
	$.getJSON(route, {
	    		note: $("#note").val(),
	    	}, function(data) { 
	    			$("#imggoogle").attr('src', data.backend_result_embedmap);
	    			var key_word = data.key_word;
	    			$.getJSON(data.backend_result_geocodejson, function(data) {
	    				let first_part = ("Votre question : " + ($("#note").val()));
	    				$("#conversation").show()
	    				$("#conversation").text(first_part);
	    				$('#loader').show()
	    				$("#loader").fadeOut(3000, function(event) {
	    					$("#conversation").append("\nPapybot : Tout de suite mon petit. L'adresse de " + key_word + " est " + data["results"][0]["formatted_address"]).delay(5000);
	    					let street = data["results"][0]["address_components"][1]["long_name"];
	    					$.getJSON("https://fr.wikipedia.org/api/rest_v1/page/summary/" + street, function(data) {
	    						$("#conversation").append("\nMais laisse moi t'en dire plus !... ");
	    						$("#conversation").append(data["extract"] + "\n");
	    						$("#wikilink").attr('href', "https://fr.wikipedia.org/wiki/" + street)
	    						$("#wikilink").show();
	    						$("#imggoogle").show();
	    					});
	    				})
	    			});
	    	});
}
$("#conversation").hide()
$("#imggoogle").hide();
$("#loader").hide();
$("#wikilink").hide();
$(document).ready(function() {
    $("#submit_button").on('click', function (event) {
    	if ($("#note").val() != "") {
    		event.preventDefault();
	    	updateQuestion("/backend_process");
	    };
    });
});
// $("#imggoogle").on('change', function() {
//   $('#mdb-preloader').delay(1000).fadeOut(300);

// LA BONNE ADRESSE PR L'EXTRAIT DE WIKIPEDIA EST ////////////////////////////////////////////////////////////////////////////////////////////////////////
// https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=OpenClassrooms&exintro=&exsentences=2&explaintext=&redirects=&formatversion=2/////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



//https://en.wikipedia.org/w/api.php?format=json&action=query&titles=OpenClassrooms&prop=revisions&rvprop=content&callback=?
  
// function dowiki(place) {
//     var URL = 'https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=';

//     URL += "&titles=" + place;
//     URL += "&rvprop=content";
//     URL += "&callback=?";
//     $.getJSON(URL, function (data) {
//         var obj = data.query.pages;
//         var ob = Object.keys(obj)[0];
//         try{
//             document.getElementById('result').textContent = obj[ob]["extract"];
//         }
//         catch (err) {
//             document.getElementById('result').textContent = err.message;
//         }

//     });
// }
// dowiki("Openclassrooms")