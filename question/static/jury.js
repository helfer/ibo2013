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

function debugCK() {
	var l = gid("tq");
	alert(l.innerHTML);
}

function CopyContent(id_source,id_dest) {
	var m = gid(id_source);
	var n = gid(id_dest);
	n.innerHTML = '<p>'+m.innerHTML+'</p';
}

function CopyContentAll() {
	CopyContent('oq','tq');
	CopyContent('op','tp');
	
	// this should become a for-loop over all available fields
	// -- not sure how make that into a dynamically sized loop though...
	CopyContent('oi1','ti1');
	CopyContent('oi2','ti2');
	CopyContent('oi3','ti3');
	
	CopyContent('oa1','ta1');
	CopyContent('oa2','ta2');
	CopyContent('oa3','ta3');
	CopyContent('oa4','ta4');
}

function ClearContent(id_dest) {
	var m = gid(id_dest);
	m.innerHTML = '';
}

function ClearContentAll() {
	ClearContent('tq');
	ClearContent('tp');
	
	// this should become a for-loop over all available fields
	// -- not sure how make that into a dynamically sized loop though...
	ClearContent('ti1');
	ClearContent('ti2');
	ClearContent('ti3');
	
	ClearContent('ta1');
	ClearContent('ta2');
	ClearContent('ta3');
	ClearContent('ta4');
}