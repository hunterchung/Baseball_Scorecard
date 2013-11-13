function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name){
	var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(c_name, value, exdays) {
	var exdate = new Date();
	exdate.setDate(exdate.getDate() + exdays);
	var c_value = escape(value)
			+ ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
	document.cookie = c_name + "=" + c_value;
}

function is_logged_in(){
	var result = false;
	
	$.ajax({
		url: "/is_logged_in/",
		async: false
	})
	.done(function(data){
		if(data=="true"){
			result = true;
		}	
	});
	return result;
}

$(document).ready(function() {
	// setup csrf for ajax
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
	    crossDomain: false, // obviates need for sameOrigin test
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type)) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});	
	
	// $("#search_by_tag").typeahead({
	// 	source: function(query, process){
	// 		return $.post("/tools/search_by_tag/", {query: query}, function(data){
	// 			return process(data);
	// 		});
	// 	}
	// });
});