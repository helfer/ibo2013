from django import forms
from django.utils.safestring import mark_safe 

class QMLTableWidget(forms.widgets.MultiWidget):
    def __init__(self,rows,attrs=None):
        self.rows = rows
        _widgets = [QMLRowWidget(row) for row in rows]
        super(QMLTableWidget,self).__init__(_widgets,attrs)


    def decompress(self,value):
        print "table decompress"
        print value
        if value:
            return json.loads(value)
        return ["" for r in self.rows]

class QMLRowWidget(forms.widgets.MultiWidget):
    def __init__(self,row,attrs=None):
        self.row = row
        _widgets = [forms.TextInput(attrs={"value":col}) for col in row]

        super(QMLRowWidget,self).__init__(_widgets,attrs)


    def decompress(self,value):
        print "row decompress"
        print value
        if value:
            return json.loads(value)
        return ["" for c in self.row]

    #XXX: zoooomg, this is the worst hack ever!
    def render(self,*args,**kwargs):
        html = super(QMLRowWidget,self).render(*args,**kwargs)
        return mark_safe(html + "<br />")




    #
