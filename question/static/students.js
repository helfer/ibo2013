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