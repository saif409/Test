from django import template
from survey.models import Answer
register = template.Library()


@register.filter("findAnswers")
def findAnswers(qid):
    anss =  []
    for q in Answer.objects.filter(question_id=qid).all():
        if q:
            anss.append(q)
        else:
            "nf"
    print(anss)
    return anss

