from celery import shared_task
from .models import *
from django.db import transaction
from .ycontent import QandA , Questions

@shared_task(name="update_spintax7")
def update_spintax7(model_id :int):
    model_instance = Spintax7.objects.get(pk=model_id)
    spintax = wordai(model_instance.content1).json()['text']
    model_instance.content2 = spintax
    print('Running Task Spintax')
    model_instance.content2
    model_instance.save()

@shared_task(name="update_yacss", max_retries=1)
def update_yacss(model_id :int):
    model_instance = Yacss.objects.get(pk=model_id)
    if not model_instance.keywords:
        model_instance.keywords = QandA(model_instance.content,model_instance.topic)
    transaction.on_commit(lambda: current_app.send_task("update_yacss_answers",kwargs={"model_id": model_instance.pk}))
    model_instance.save()

@shared_task(name="update_yacss_answers", max_retries=1)
def update_yacss(model_id :int):
    model_instance = Yacss.objects.get(pk=model_id)
    if not model_instance.questions:
        spintax = Questions(model_instance.keywords)
        model_instance.questions = '\n'.join(spintax[0])
        model_instance.answers = '\n'.join(spintax[1])
    model_instance.save()