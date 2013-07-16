from ibo2013.question.models import *

def run():
    vnodes = VersionNode.objects.all().order_by('question','language')
    
    noncom = 0
    qid = 0
    bad = 0
    good = 0
    for vnode in vnodes:
        if vnode.question_id != qid:
            qid = vnode.question_id
            eng = VersionNode.objects.filter(language=1,question=vnode.question,committed=True).order_by('-timestamp')[0]
            #ru = VersionNode.objects.filter(language=2,question=vnode.question).order_by('-timestamp')[0]
        if vnode.language_id not in (1,2):
            try:
                tr = Translation.objects.get(target=vnode)
            except:
                print "ERROR"
                print vnode
                tr = Translation(language=vnode.language,target=vnode,origin=eng)
                #tr.save()
                bad += 1
            if tr.origin != eng:
                #print tr,"is not",eng
		print tr.origin.version,eng.version
                bad += 1
                tr.origin = eng
                #tr.save()
            else:
                good += 1
                #print "tr okay"
        else:
            if vnode.committed == False:
                vnode.committed = True
                #vnode.save()
                #print "committed English or Russian"            
                noncom += 1

    print "bad",bad
    print "good",good
    print "noncom",noncom
