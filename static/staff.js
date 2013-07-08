function make_table(nrows,ncols) {

    var textarea = document.getElementById("area51");
    var qid = document.getElementById("question_id").value;

    var xml = '<table id="">';
    var header = '\n<header>';
    for(var h=0;h<ncols;h++){
        header += '\n\t<col id="">header '+h+'</col>';
    }  
    header +=  '\n</header>';

    var rows = ""
    for(var i = 0;i<nrows;i++){
        var row = '\n<row id="'+qid+'_r'+i+'">';
        for(var j = 0;j<ncols;j++){
            row += '\n\t<col id="">col '+j+'</col>';
        }
        row += '\n</row>';
        rows += row
    }
    xml += header + rows + '\n</table>';

    return xml;
}

function add_table(){
    var nrows = document.getElementById("nrows").value;
    var ncols = document.getElementById("ncols").value;
    var table = make_table(nrows,ncols);
    insertAtCaret("area51",table);
    return false;
}

function add_figure(){
    var qid = document.getElementById("question_id").value;
    var sel = document.getElementById("id_figure")
    var fname = sel.options[sel.selectedIndex].innerHTML
    var image = '<figure id="" imagefile="'+fname+'" />';
    insertAtCaret("area51",image);
    return false;
}
 
function add_list(){
    var qid = document.getElementById("question_id").value;
    var list = '<list id="">\n';
    var items = ['\t<item id=""></item>',
                '\t<item id=""></item>',
                '\t<item id=""></item>',
                '\t<item id=""></item>'].join("\n");
    list += items;
    list += '\n</list>\n';
    
    insertAtCaret("area51",list);
    return false;
}

function insertAtCaret(areaId,text) {
    var txtarea = document.getElementById(areaId);
    var scrollPos = txtarea.scrollTop;
    var strPos = 0;
    var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? 
        "ff" : (document.selection ? "ie" : false ) );
    if (br == "ie") { 
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
    }
    else if (br == "ff") strPos = txtarea.selectionStart;

    var front = (txtarea.value).substring(0,strPos);  
    var back = (txtarea.value).substring(strPos,txtarea.value.length); 
    txtarea.value=front+text+back;
    strPos = strPos + text.length;
    if (br == "ie") { 
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        range.moveStart ('character', strPos);
        range.moveEnd ('character', 0);
        range.select();
    }
    else if (br == "ff") {
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
    }
    txtarea.scrollTop = scrollPos;
}
