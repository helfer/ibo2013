from django import forms
from ibo2013.question.forms import QMLTableField
from xml.etree import ElementTree as et
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
            self.identifier = root.attrib['id']
        except KeyError:
            self.identifier = "element has no identifier"
            print "no ident: ",root.tag
        self.children = []
        self.parse(root)

    def addChild(self,child):
        self.children.append(child)

    #outputs a django form consisting of all elements
    def formalize(self):
        raise Exception("not implemented")

    #takes cleaned form data as input and updates its own values accordingly
    def update(self,cd):
        if self.identifier in cd:
            self.data = cd[self.identifier]
            print self.__class__.__name__,"has data",self.data
            self.apply_update()
        else:
            print "no data",self.__class__.__name__

        for c in self.children:
            c.update(cd)


    def apply_update(self):
        self.xml.text = self.data

    def parse(self,xml):
        pass

    def zackzack(self):
        return et.tostring(self.xml,'utf-8')

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
<text id="{{qid}}_st_1">text</text>       
<task id="{{qid}}_tsk_1">task</task>    

<answerlist randomize="false">
    <answersplit id="{{qid}}_s_1">True</answersplit>
    <answersplit id="{{qid}}_s_2">False</answersplit>
    <choice id="{{qid}}_c_1">answer option 1</choice>
    <choice id="{{qid}}_c_2">answer option 2</choice>
    <choice id="{{qid}}_c_3">answer option 3</choice>
    <choice id="{{qid}}_c_4">answer option 4</choice>
</answerlist>   
</question>"""

        xml = t.replace("{{qid}}",str(qid))

        return QMLobject(xml)



class QMLtext(QMLobject):
    def parse(self,elem):
       self.form_element = forms.CharField(label="text",initial = elem.text,widget = forms.Textarea)


class QMLtask(QMLtext):
    pass

class QMLanswerlist(QMLobject):
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
    def get_filename(self,elem):
        self.filename = self.xml.attrib["imagefile"]

    def apply_update(self):
        self.xml.attrib["imagefile"] = self.data

    def parse(self,elem):
        self.form_element = forms.CharField(label="figure", initial = elem.attrib["imagefile"])

class QMLtable(QMLobject):
    def parse(self,elem):
        rowz = []
        for child in elem:
            if child.tag == "header" or child.tag == "row":
                ro = []
                for sub in child:
                    ro.append(sub.text)
                
                rowz.append(ro)
            else:
                raise QMLException("unknown QML tag: "+child.tag)

        self.form_element = QMLTableField(rowz)

    def apply_update(self):
        

        tabledata = []
        rows = json.loads(self.data)
        print "rows",rows
        for row in rows:
            print "row",row
            row = json.loads(row)
            for col in row:
                print "col",col
                tabledata.append(col)

        print "tabledata",tabledata

        for child in self.xml:
            if child.tag == "header" or child.tag == "row":
                for sub in child:
                    newval = tabledata.pop(0)
                    print "updating child",sub.attrib["id"],"from",sub.text,"to",newval
                    sub.text = newval
            else:
                raise QMLException("unknown QML tag: "+child.tag)

class QMLanswersplit(QMLobject):
    def parse(self,elem):
        self.form_element = forms.CharField(label="answersplit",initial = elem.text)

        for child in elem:
            raise QMLException("answersplit element cannot have children")
        

class QMLchoice(QMLobject):
    def parse(self,elem):
        self.form_element = forms.CharField(label="choice",initial = elem.text,widget=forms.Textarea)

class QMLlist(QMLobject):
    def parse(self,elem):
        for child in elem:
            if child.tag == "item":
                self.addChild(QMLlistitem(child))
            else:
                raise QMLException("invalid tag in list: "+ child.tag)


class QMLlistitem(QMLobject):
    def parse(self,elem):
        self.form_element = forms.CharField(label="item"+elem.attrib["id"],initial = elem.text)

class QMLException(Exception):
    pass
