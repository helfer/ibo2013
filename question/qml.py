from django import forms
from ibo2013.question.forms import QMLTableField
from ibo2013.question.models import Figure
from xml.etree import ElementTree as et
#import lxml.etree as lxmltree
import json
class QMLobject():

    def __init__(self,xml):
        self.form_element = None
        if type(xml) == str:
            root = et.fromstring(xml)
        elif type(xml) == unicode:
            root = et.fromstring(xml.encode('utf-8'))
        else:
            root = xml
        
        self.xml = root

        try:
            self.identifier = self.xml.attrib['id']
        except KeyError:
            if not self.__class__.__name__ in ["QMLanswerlist"]:
                raise KeyError("id missing from QML element "+ self.xml.tag)
            self.identifier = "element has no identifier"
            print "no ident: ",root.tag
        self.children = []
        self.parse(root)

    def addChild(self,child):
        self.children.append(child)

    #assign initial xml id attribute where it is empty
    def assign_initial_id(self,question_id,blacklist=None):
        if blacklist is None:
            blacklist = self.list_id()

        #print blacklist
        if "id" in self.xml.attrib:
            if self.xml.attrib["id"] == "":
                i = 0
                ident = False
                while (not ident) or (ident in blacklist):
                    i += 1
                    ident = self.make_ident(question_id,i)

                self.identifier = ident
                self.xml.attrib["id"] = ident
                #print "assigned initial id " + ident
                blacklist.append(ident)

        for c in self.children:
            c.assign_initial_id(question_id,blacklist)
    
    def parse_figures(self):
        if self.xml.tag == "figure":
           if len(self.xml) == 0:
                repl = et.fromstring(Figure.objects.get(name=self.xml.attrib['imagefile']).var) 
                for c in repl:
                    c.attrib['id'] = ''
                    self.xml.append(c)
                    self.addChild(QMLfigureText(c))
        else:
            for c in self.children:
                c.parse_figures()            

    #list xml attribute id for self and all sub-elements
    def list_id(self):
        lst = []
        if "id" in self.xml.attrib:
            lst.append(self.xml.attrib["id"])
        for c in self.children:
            lst.extend(c.list_id())
        
        return lst

    def make_ident(self,question_id,i):
        return str(question_id) + "_" + self.__class__.abbr + str(i)



    #takes cleaned form data as input and updates its own values accordingly
    def update(self,cd):
        if self.identifier in cd:
            self.data = cd[self.identifier]
            ##print self.__class__.__name__,"has data",self.data
            self.apply_update()
        else:
            pass
            #print "no data",self.__class__.__name__

        for c in self.children:
            c.update(cd)


    def reassign_identifiers(self,question_id,blacklist=None):
        if blacklist is None:
            blacklist = []
       
        #print "reassign" 
        
        if "id" in self.xml.attrib and self.xml.tag != "question":
            i = 0
            ident = False
            while (not ident) or (ident in blacklist):
                i += 1
                ident = self.make_ident(question_id,i)

            #print "update id to " + ident
            self.xml.attrib['id'] = ident
            self.identifier = ident
            blacklist.append(self.xml.attrib['id'])

        for c in self.children:
            c.reassign_identifiers(question_id,blacklist)

    def apply_update(self):
        self.xml.text = self.data

    def parse(self,xml):
        pass

    def zackzack(self,pretty=False):
        txt = et.tostring(self.xml,'utf-8')
        if pretty:
            print "prettifyyyyyyyyyyyyyyyyyy"
            #return lxmltree.tostring(lxmltree.fromstring(txt),pretty_print=True)
            return txt
        else:
            return txt
    def get_form_field(self):
        return forms.CharField(label=self.__class__.__name__)

    def get_form_elements(self):
        if self.form_element is None:
            elems = []
        else:
            elems = [(self.identifier,self.form_element)]
        for c in self.children:
                elems.extend(c.get_form_elements())
        return elems

    def summary(self,prefix=""):
        return prefix + str(self.__class__.__name__) + "\n" + "".join([c.summary(prefix+">") for c in self.children])

class QMLquestion(QMLobject):
    abbr = "q"
    #takes element tree as input and parses it
    def parse(self,root):
        for child in root:
            if child.tag == "text":
                self.addChild(QMLtext(child))
            elif child.tag == "task":
                self.addChild(QMLtask(child))
            elif child.tag == "answerlist":
                self.addChild(QMLanswerlist(child))
            elif child.tag == "figure":
                self.addChild(QMLfigure(child))
            elif child.tag == "table":        
                self.addChild(QMLtable(child))
            elif child.tag == "list":
                self.addChild(QMLlist(child))
            else:
                raise KeyError("invalid xml tag: " + child.tag)

    @staticmethod
    def from_template(qid):
        t = """<question id="{{qid}}">
<text id="">text</text>       
<task id="">task</task>    

<answerlist randomize="false">
    <answersplit id="">True</answersplit>
    <answersplit id="">False</answersplit>
    <choice id="">answer option 1</choice>
    <choice id="">answer option 2</choice>
    <choice id="">answer option 3</choice>
    <choice id="">answer option 4</choice>
</answerlist>   
</question>"""

        xml = t.replace("{{qid}}",str(qid))

        return QMLobject(xml)



class QMLtext(QMLobject):
    abbr = "tx"
    def parse(self,elem):
       self.form_element = forms.CharField(label="text",initial = elem.text,widget = forms.Textarea)


class QMLtask(QMLtext):
    abbr = "ta"
    pass

class QMLanswerlist(QMLobject):
    abbr = "ans"
    def parse(self,elem):
        self.choices = []
        self.answersplit = []
        for child in elem:
            if child.tag == "answersplit":
                self.addChild(QMLanswersplit(child))
            elif child.tag == "choice":
                self.addChild(QMLchoice(child))
            else:
                raise KeyError("invalid xml tag: " + child.tag)



class QMLfigure(QMLobject):
    abbr = "fi"
    def get_filename(self,elem):
        self.filename = self.xml.attrib["imagefile"]

    def apply_update(self):
        self.xml.attrib["imagefile"] = self.data

    def parse(self,elem):
        for child in elem:
            if child.tag == "textarea":
                self.addChild(QMLfigureText(child))
            else:
                raise QMLException("invalid sub-element in figure: "+child.tag)
        #self.form_element = forms.CharField(label="figure", initial = elem.attrib["imagefile"])

class QMLfigureText(QMLobject):
    abbr = "ft"
    def parse(self,elem):
        self.form_element = forms.CharField(label=elem.attrib['ibotag'],initial=elem.text)

class QMLtable(QMLobject):
    abbr = "tb"
    def parse(self,elem):
        rowz = []
        for child in elem:
            if child.tag == "header" or child.tag == "row":
                ro = []
                for sub in child:
                    ro.append(sub.text)
                    self.addChild(QMLtableCol(sub))
                rowz.append(ro)
            else:
                raise QMLException("unknown QML tag: "+child.tag)

        self.form_element = QMLTableField(rowz)

    def apply_update(self):
        

        tabledata = []
        rows = json.loads(self.data)
        #print "rows",rows
        for row in rows:
            #print "row",row
            row = json.loads(row)
            for col in row:
                #print "col",col
                tabledata.append(col)

        #print "tabledata",tabledata

        for child in self.xml:
            if child.tag == "header" or child.tag == "row":
                for sub in child:
                    newval = tabledata.pop(0)
                    #print "updating child",sub.attrib["id"],"from",sub.text,"to",newval
                    sub.text = newval
            else:
                raise QMLException("unknown QML tag: "+child.tag)

class QMLtableCol(QMLobject):
    abbr = "cl"


class QMLanswersplit(QMLobject):
    abbr = "sp"
    def parse(self,elem):
        self.form_element = forms.CharField(label="answersplit",initial = elem.text)

        for child in elem:
            raise QMLException("answersplit element cannot have children")
        

class QMLchoice(QMLobject):
    abbr = "ch"
    def parse(self,elem):
        self.form_element = forms.CharField(label="choice",initial = elem.text,widget=forms.Textarea)

class QMLlist(QMLobject):
    abbr = "ls"
    def parse(self,elem):
        for child in elem:
            if child.tag == "item":
                self.addChild(QMLlistitem(child))
            else:
                raise QMLException("invalid tag in list: "+ child.tag)


class QMLlistitem(QMLobject):
    abbr = "li"
    def parse(self,elem):
        self.form_element = forms.CharField(label="item"+elem.attrib["id"],initial = elem.text)

class QMLException(Exception):
    pass
