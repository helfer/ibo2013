from HTMLParser import HTMLParser
import cStringIO
import sys,subprocess,os
import cgi
from django.utils.safestring import mark_safe

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#this is mostly for ckeditor
def strip_paragraph(html):
    html = html.replace("<p>","")
    return html.replace("</p>","")

IBO_TAGS = {'em':'i','strong':'b','sup':'sup','sub':'sub'}
def ibotag2html(string):
    rt = string
    for tag in IBO_TAGS:
        rt = rt.replace("[{0}]".format(IBO_TAGS[tag]),"<{0}>".format(tag))
        rt = rt.replace("[/{0}]".format(IBO_TAGS[tag]),"</{0}>".format(tag))

    return rt



def html2ibotag(string):
    rt = string
    for tag in IBO_TAGS:
        rt = rt.replace("<{0}>".format(tag),"[{0}]".format(IBO_TAGS[tag]))
        rt = rt.replace("</{0}>".format(tag),"[/{0}]".format(IBO_TAGS[tag]))

    return rt

#unnecessary. Element tree does all the escaping for you :)
def clean_html(string):
    return string
    
    #return cgi.escape(string)


#would be nicer with a map
def iboclean(post):
    rt = {}
    for p in post:
        # strip html is too aggressive.
        rt[p] = clean_html(strip_paragraph(html2ibotag(post[p])))

    return rt

#does essentially the opposite as iboclean but on single strings
def prep_for_display(string):
    return mark_safe(ibotag2html(string))

def nl2br(string):
    return string.replace("\n","<br />")

"""
should pipe to php script to get pdf of exam
"""
def xml2pdf(exml,filename='exam1.pdf'):
    php_file = '/var/www/django/ibo2013/xml2pdf/PDFgenIBO2013_15Juli.php'
    phpinput = cStringIO.StringIO(exml)
    #print exml[:2000]
    os.chdir('./xml2pdf/')
    p1 = subprocess.Popen(["php", php_file,filename], stdin = subprocess.PIPE,stdout=subprocess.PIPE)
    output = p1.communicate(phpinput.getvalue())[0]
    os.chdir('..')
    print output
