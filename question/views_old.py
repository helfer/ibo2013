#just a few old views parked here that I don't think we'll ever use again. Not even sure they work any more.


@login_required
@permission_check
def translation_overview(request,exam_id,lang_id=1,permissions=None):

    raise Exception("deprecated function")

    try:
        exam_id = int(exam_id)
        target_language_id = int(lang_id)
        exam = Exam.objects.get(id=exam_id)
        language = Language.objects.get(id=target_language_id)
    except KeyError:
        raise Http404()

    questions = exam.examquestion_set.order_by('position')

    #selects all the most recent english versions of questions from this exam
    query = """SELECT * FROM (

        SELECT eq.*, vn.version, vn.id as vid
        FROM question_examquestion eq
        LEFT OUTER JOIN (
            SELECT *
            FROM question_versionnode
            WHERE language_id ='%s'
        ) AS vn ON eq.question_id = vn.question_id
        WHERE eq.exam_id='%s'
        ORDER BY position, version DESC
        ) AS t1
        GROUP BY position"""
    q1params = [1,exam_id] #todo: english = 1 is hardcoded as primary language

    primary_versions = ExamQuestion.objects.raw(query,q1params)

    #selects the most recent target translatsion versions of questions in exam
    query2 = """SELECT t1.*,tr.origin_id,tr.target_id FROM (
        SELECT eq.*, vn.version, vn.id as vid 
        FROM question_examquestion eq
        LEFT OUTER JOIN (
            SELECT *
            FROM question_versionnode
            WHERE language_id ='%s'
        ) AS vn ON eq.question_id = vn.question_id
        WHERE eq.exam_id='%s'
        ORDER BY position, version DESC
        )t1
        LEFT JOIN question_translation tr ON t1.vid = tr.target_id
        GROUP BY position"""
    q2params = [target_language_id,exam_id]

    target_versions = ExamQuestion.objects.raw(query2,q2params)

    pv = list(primary_versions)
    tv = list(target_versions)
    assert len(pv) == len(tv) #if not, you screwed up the queries

    questions = []
    for i in range(len(pv)):
        questions.append({"primary":pv[i],"target":tv[i]})
        if tv[i].vid is None:
            questions[i]["status"] = "not started"
        elif tv[i].origin_id != pv[i].vid:
            questions[i]["status"] = "needs update"
        else:
            questions[i]["status"] = "OK"
            
    return render_to_response('translation_overview.html',{'exam':exam,'questions':questions,'target_language_id':target_language_id})


