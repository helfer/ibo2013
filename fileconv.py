from ibo2013.question.models import FilenameConversion


with open('ibo13_exams_answers_corrections.txt') as f:
    for line in f:
        (prak,iid,tup,fn,_) = line.split(' ')
        print iid,prak,tup,fn
        fc = FilenameConversion(prakti=prak,individual_id=iid,ctype=tup,filename=fn)
        fc.save()
