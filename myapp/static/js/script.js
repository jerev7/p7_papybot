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
$(document).ready(function() {
    $("#submit_button").on('click', function (event) {
    	event.preventDefault();
    	$.getJSON("/backend_process", {
    		note: $("#note").val(),
    	}, function(data) {
    		if (data.backend_result != "") {
    			event.preventDefault();
    			alert(data.backend_result)
    		};
    	});
    });
});
