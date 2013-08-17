function gid(element) { return document.getElementById(element); }

function login() {
	var p = gid("studentcode");
	var q = gid("D");
	var r = gid("M");
	var s = gid("Y");
	
	if (p.value == '' || q.value == '' ||
		r.value == '' || s.value == '')
	{
		alert("You have not filled in all required field.");
		// there is a difficulty here to do this multilingually
	}
	else
	{
		// check login with database to see if it is valid
		window.location.href = 'examhome.html';
	}
}

function fullsize() {
	
	var p = gid("header");
	var q = gid("footer");
	var r = gid("main");
	var s = gid("clock");
	var t = gid("answerbar");
	var u = gid("answers");
	
	if (p.className == 'hide')
	{
		p.className = '';
		q.className = '';
		r.className = '';
		s.className = '';
		t.className = '';
		u.className = '';
	}
	else
	{
		p.className = 'hide';
		q.className = 'hide';
		r.className = 'hide';
		s.className = 'hide';
		t.className = 'hide';
		u.className = 'hide';
	}
}


function enlarge(obj) {
	if (obj.className != '')
		obj.className = '';
	else
		obj.className = 'large';
}

function zoomfont() {
	
	if (document.body.className == 'zoom')
	{
		document.body.className = '';
	}
	else
	{
		document.body.className = 'zoom';
	}
}

function flag() {
	var p = gid("flag");
	
	if (p.className == 'select')
	{
		p.className = '';
	}
	else
	{
		p.className = 'select';
	}
}



//AJAX functions

// using jQuery
function getCookie(name) {
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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function submit_flag(qid,uid) {
    ck = $('#id_flag').is(':checked');

    url = "/ajax/flag/";
    ajax_req = $.ajax({
        url: url,
        type: "POST",
        data: {
            qid:qid,
            uid:uid,
            flag:ck
        },
        success: function(data, textStatus, jqXHR) {
            console.log(data);
        },
        error: function(data, textStatus, jqXHR) {
                    console.log(data.responseText)
                    console.log("ERROR: " + $.parseJSON(data.responseText));
            }
    });
}

function save_answer(qid,ans,ename) {
    ck = $('input[name="'+ename+'"]:checked')
    console.log("ckid",ck.id);
    ckv = ck.val();
 
    url = "/ajax/answer/";
    ajax_req = $.ajax({
        url: url,
        type: "POST",
        data: {
            qid:qid,
            ans:ans,
            choice:ckv,
            ename:ename
        },
        success: function(data, textStatus, jqXHR) {
            console.log("success");
            console.log(data);
            //ck = document.getElementByName(data);
            ck.prop("checked",true);
            return true;
        },
        error: function(data, textStatus, jqXHR) {
                    console.log("fail");
                    //console.log(data.responseText)
                    response = $.parseJSON(data.responseText);
                    console.log("ERROR: " + response); 
                    if(response == "exam is over"){
                        //alert("Your answer was not recorded because the exam is over. Please follow the instructions of the exam staff.");
                        alert("the exam is over, you can no longer change your responses");
                    }
                    ck.checked = false;
                    return false;
            }
    });
    return false;
   //alert(qid + " " + ans + "  " + ename + " " + ck);
}

//$(document).ready(function() {
//    setTimeout(function(){$('input[type=radio]').each(function(){
//        console.log(this.name);
//        if (this.name.indexOf("checked") > 0){
//            this.checked = true;
//        }
//    });},100);
//});


// fix for images now showing up immediately
window.onload = function() {
	var v = document.getElementsByTagName('img');
for (var i = 0; i < v.length; i++) {
	v[i].style.display = 'none';
	v[i].style.display = 'block';
}
}
