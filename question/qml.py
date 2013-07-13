from django import forms
from ibo2013.question import utils
from ibo2013.question.forms import QMLTableField
from ibo2013.question.models import Figure
from xml.etree import ElementTree as et
from ibo2013.question import simplediff
#import lxml.etree as lxmltree
import json
class QMLobject():

    def __init__(self,xml):
        if type(xml) == str:
            root = et.fromstring(xml)
        elif type(xml) == unicode:
            root = et.fromstring(xml.encode('utf-8'))
        else:
            root = xml
        
        self.xml = root
        self.data = None
        self.meta = None

        try:
            self.identifier = self.xml.attrib['id']
        except KeyError:
            if not self.__class__.__name__ in ["QMLanswerlist"]:
                raise KeyError("id missing from QML element "+ self.xml.tag)
            self.identifier = "element has no identifier"
        self.children = []
        self.parse(root)

    def form_element(self):
        return None

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

    #compare_to is another qml object
    def get_texts_nested(self,prep=False,compare_to=None):
        if self.data is None:
            sub = []
            for c in self.children:
                sub.extend(c.get_texts_nested(prep,compare_to))
            rt = [{"id":self.identifier,"tag":self.xml.tag,"data":sub,"meta":self.meta}]
        else:
            if compare_to is None:
                data = self.data
            else:
                original = self.__class__(compare_to.xml.find(".//{0}[@id='{1}']".format(self.xml.tag,self.identifier)))
                print "diffing"
                data = simplediff.html_diff(original.data,self.data)

            if prep:
                data = utils.prep_for_display(data)
            rt = [{"id":self.identifier,"tag":self.xml.tag,"data":data,"meta":self.meta}]
        
        return rt

    def get_data(self):
        rt = {}
        if self.data is not None:
            rt = {self.identifier:self.data}
        for c in self.children:
            rt.update(c.get_data())

        return rt

    def get_forms_nested(self):
        if self.form_element() is None:
            sub = []
            for c in self.children:
                sub.extend(c.get_forms_nested())
            rt = [{"id":self.identifier,"tag":self.xml.tag,"data":sub,"meta":self.meta}]
        else:
            rt = [{"id":self.identifier,"tag":self.xml.tag,"data":self.form_element(),"meta":self.meta}]

        return rt

    #takes cleaned form data as input and updates its own values accordingly
    def update(self,cd):
        #print self.xml.tag,self.identifier
        if self.identifier in cd:
            self.data = cd[self.identifier]
            #print self.__class__.__name__,"has data",self.data
        else:
            if self.data is not None:
                self.data = '' #set fields to empty if not required and no data given
            #print "no data",self.__class__.__name__

        self.apply_update()
        
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

    # makes the figures appear inline
    def inline_image(self):
        for c in self.children:
            c.inline_image()

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
        if self.form_element() is None:
            elems = []
        else:
            elems = [(self.identifier,self.form_element())]
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
                raise QMLException("tables are not supported, use svg figure instead")
                #self.addChild(QMLtable(child))
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


    def update(self,cd):
        for c in self.children:
            c.update(cd)


class QMLtext(QMLobject):
    abbr = "tx"
    def parse(self,elem):
       self.data = elem.text
    def form_element(self):
       return  forms.CharField(label="text",initial = self.data,widget = forms.Textarea) 

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
        return self.filename
    #def apply_update(self):
    #    self.xml.attrib["imagefile"] = self.data

    def inline_image(self):
        try:
            fig = Figure.objects.get(name=self.filename).svg
        except:
            raise QMLException("figure {0} not found".format(self.filename))
        search = "textarea"
        replace = self.xml.findall(search)
        for r in replace:
            fig = fig.replace(hex(hash(r.attrib['ibotag'])),r.text)
        e1 = et.Element("svginline")
        e = et.fromstring(fig)
        e1.append(e)
        self.xml.append(e1)
        

    def parse(self,elem):
        self.filename = self.xml.attrib["imagefile"]
        self.meta = elem.attrib["imagefile"]
        for child in elem:
            if child.tag == "textarea":
                self.addChild(QMLfigureText(child))
            else:
                raise QMLException("invalid sub-element in figure: "+child.tag)
        #self.form_element = forms.CharField(label="figure", initial = elem.attrib["imagefile"])

class QMLfigureText(QMLobject):
    abbr = "ft"
    def parse(self,elem):
        self.data = elem.text
        self.meta = elem.attrib['ibotag']

    def form_element(self):
        return forms.CharField(label=self.meta,initial=self.data)

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
        self.rowz = rowz

    def form_element(self):
       return QMLTableField(self.rowz)

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
        self.data = elem.text
        for child in elem:
            raise QMLException("answersplit element cannot have children")
       
    def form_element(self): 
        return forms.CharField(label="answersplit",initial = self.data)

class QMLchoice(QMLobject):
    abbr = "ch"
    def parse(self,elem):
        self.data = elem.text

    def form_element(self):
        return forms.CharField(label="choice",initial = self.data,widget=forms.Textarea)

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
        self.data = elem.text
        self.meta = elem.attrib['id']

    def form_element(self):
        return forms.CharField(label="item_"+self.meta,initial = self.data)

class QMLException(Exception):
    pass
