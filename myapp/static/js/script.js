$(document).ready(function() {
    $("#submit_button").on( 'click', function (event) {
    	// event.preventDefault();
    	var $mynote = $("#note").val();
    	if ($mynote != "") {
    		event.preventDefault();
    		alert("Voilà votre question très intéressante :\n" + $mynote)
    	};
    });
});
