var OriginalValues = [];

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
		$('#submitbtn').click();
	else
		alert('No questions selected!');
}

function CopyContent(id_source,id_dest) {
	var m = gid(id_source);
	var n = gid(id_dest);
	var o = m.innerHTML.replace(/<del>[^>]*<\/del>/g, '').replace(/<ins>/g, '').replace(/<\/ins>/g,'');
	if (n.tagName == 'TEXTAREA')
	{
		CKEDITOR.instances[id_dest].setData('<p>'+o+'</p>');
	}
	else
	{
		n.value = o;
	}
}

function CopyContentAll() {
	var allElements = document.getElementsByTagName('*');
	for (var i = 0; i < allElements.length; i++) {
		var m = allElements[i].getAttributeNode('onclick');
		if (m) {
			if (m.value.search("CopyContent\\(") !== -1)
				eval(m.value);
		}
	}
}

function ClearContent(id_dest) {
	var m = gid(id_dest);
	
	if (m.tagName == 'TEXTAREA')
	{
		CKEDITOR.instances[id_dest].setData('');
	}
	else
	{
		m.value = '';
	}
}

function ClearContentAll() {
	var allElements = document.getElementsByTagName('*');
	for (var i = 0; i < allElements.length; i++) {
		var m = allElements[i].getAttributeNode('onclick');
		if (m) {
			if (m.value.search("ClearContent\\(") !== -1)
				eval(m.value);
		}
	}
}

function CheckChanges_StoreCurrent() // on page load
{

	// need to add check for rating
	
	var p = document.getElementsByTagName("textarea");
	var q = document.getElementsByTagName("input");
	OriginalValues.push(gid("id_flag").checked);
	OriginalValues.push(gid("id_checkout").checked);
	
	for (i=0;i<p.length;i++)
	{
		OriginalValues.push(p[i].innerHTML);
	}
	for (i=0;i<q.length;i++)
	{
		OriginalValues.push(q[i].value);
	}
} 

function CheckChanges_Check() // on page exit
{
	var changes = false;
	
	if (OriginalValues[0] != gid("id_flag").checked)
		changes = true;
	if (OriginalValues[1] != gid("id_checkout").checked)
		changes = true;
	
	var p = document.getElementsByTagName("textarea");
	var q = document.getElementsByTagName("input");
	
	for (i=0;i<p.length;i++)
	{
		if (OriginalValues[i+2] != p[i].innerHTML)
		{
			changes = true;
		}
	}
	
	for (i=0;i<q.length;i++)
	{
		if (OriginalValues[i+2+p.length] != q[i].value)
		{
			changes = true;
		}
	}
	
	if (changes)
		confirm('You have unsaved changes on the page. Do you really want to leave?');
	
}

// temporarily not used!
//window.onbeforeunload = CheckChanges_Check;
