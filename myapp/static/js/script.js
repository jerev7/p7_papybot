function updateQuestion(route) {
	$.getJSON(route, {
	    		note: $("#note").val(),
	    	}, function(data) { 
	    			$("#imggoogle").attr('src', data.map_url);
    				let first_part = ("Vous : " + ($("#note").val()));
    				$("#conversation").show()
    				$("#conversation").text(first_part);
    				$('#loader').show()
    				$("#loader").fadeOut(3000, function(event) {
    					$("#conversation").append("\nPapybot : " + data.papy_response + data.adress).delay(5000);
						$("#conversation").append("\nPapybot : Mais laisse moi t'en dire plus !... ");
						$("#conversation").append("\n" + data.wiki_extract);
						$("#wikilink").attr('href', data.wiki_link)
						$("#wikilink").show();
						$("#imggoogle").show();
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
