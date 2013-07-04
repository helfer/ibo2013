function gid(element) { return document.getElementById(element); }

function enlarge(obj) {
	if (obj.className != '')
		obj.className = '';
	else
		obj.className = 'large';
}

function SelectAllToggle() {
	var l = document.getElementsByName('pdfselect');
	if (l[0].checked == true) {
		for (var i=0;i<l.length;i++) {
			l[i].checked = false;
		}
	} else {
		for(var i=0;i<l.length;i++) {
			l[i].checked = true;
		}
	}
}

function DownloadPDF() {
	var l = document.getElementsByName('pdfselect');
	var s = 'Make PDF of questions: ';
	var c = 0;
	for (var i=0;i<l.length;i++) {
		if (l[i].checked) {
			s = s + l[i].value + ' ';
			c++;
		}
	}
	if (c != 0)
		confirm(s);
	else
		alert('No questions selected!');
}