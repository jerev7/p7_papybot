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
	    			event.preventDefault();
	    			$("#imggoogle").attr('src', data.backend_result);
	    			$("#imggoogle").show();
	    	});
}
$("#imggoogle").hide();
$(document).ready(function() {
	$("#result").hide();
    $("#submit_button").on('click', function (event) {
    	if ($("#note").val() != "") {
    		event.preventDefault();
    		$("#result").text("Votre question est : " + $("#note").val());
    		$("#result").show();
	    	updateQuestion("/backend_process");
	    };
    });
});



  
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