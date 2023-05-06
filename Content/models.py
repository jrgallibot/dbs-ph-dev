from django.db import models , transaction
from django.db.models.signals import post_save
from celery import current_app
from django.conf import settings
from apps.utils.models import BaseModel
from ckeditor.fields import RichTextField
import json
import requests
from django.dispatch import receiver
#from .ycontent import QandA , Questions
from datetime import datetime
from .keywordplanner import *
import os

def wordai(content):
            url = 'https://wai.wordai.com/api/rewrite'
            body = {'email': 'isse.mohamed@gmail.com',
                'key': '62916ff1f17b61596edab98affebc9f5',  
                    'input': content,
                    'rewrite_num': 10,
                    'uniqueness': 3,       
                }

            headers = {'content-type': 'application/json'}
            result = requests.post(url, data=json.dumps(body),headers=headers)
            return result
# Create your models here.
class Spintax7(BaseModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Spintax7User')
    runSpintax = models.BooleanField(default=False)
    topic = models.CharField(max_length=300,null = True, blank = True)

    content1 = RichTextField(config_name='Minimal',null = True, blank = True)
    content2 = models.TextField(null = True, blank = True)
    content3 = RichTextField(config_name='Minimal',null = True, blank = True)
    content4 = RichTextField(config_name='Minimal',null = True, blank = True)
    content5 = RichTextField(config_name='Minimal',null = True, blank = True)
    content6 = RichTextField(config_name='Minimal',null = True, blank = True)
    content7 = RichTextField(config_name='Minimal',null = True, blank = True)
    

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Spintax 7"
        verbose_name_plural = "Spintax 7"

    def save(self, *args, **kwargs):
        if self.runSpintax:
            #self.content2 = wordai(self.content1).json()['text']
            #self.content2 = wordai(self.content2)
            #self.content3 = wordai(self.content3)
            #self.content4 = wordai(self.content4)
            #self.content5 = wordai(self.content5)
            #self.content6 = wordai(self.content6)
            #self.content7 = wordai(self.content7)
            print('Send Celery Spintax Task')
            transaction.on_commit(lambda: current_app.send_task("update_spintax7",kwargs={"model_id": self.pk},queue="default",))



        super().save(*args, **kwargs)

#@receiver(post_save, sender=Spintax7)
#def spintax7_post_save(sender, instance, **kwargs):
#    print('Send Spintax7')
#    transaction.on_commit(lambda: current_app.send_task(
#                "update_spintax7",
#                kwargs={"model_id": instance.pk}))


class Yacss(BaseModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Yacss_User')
    runApp = models.BooleanField(default=False)
    topic = models.CharField(max_length=300,null = True, blank = True)
    content = models.TextField(null = True, blank = True)
    questions = models.TextField(null = True, blank = True)
    answers = models.TextField(null = True, blank = True)
    keywords = models.TextField(null = True, blank = True)
    

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Yacss Builder"
        verbose_name_plural = "Yacss Builder"

    def save(self, *args, **kwargs):        
        if self.runApp:
        #    self.keywords = QandA(self.content,self.topic)
        #elif self.topic:
        #    answer = Questions(self.keywords)
        #    self.questions = '\n'.join(answer[0])
        #    self.answers = '\n'.join(answer[1])
            transaction.on_commit(lambda: current_app.send_task("update_yacss",kwargs={"model_id": self.pk},queue="default"))
            self.runApp = False
        super().save(*args, **kwargs)

class KeywordIdeas(BaseModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='KeywordIdeas_User')
    keywords = models.CharField(max_length=300,null = True, blank = True)
    pageUrl = models.URLField(null = True, blank = True, max_length=500)
    result = RichTextField(null = True, blank = True)
    

    def __str__(self):
        if self.keywords:
            ret = self.keywords
        else:
            ret = self.pageUrl

        return ret

    class Meta:
        verbose_name = "Keyword Idea"
        verbose_name_plural = "Keyword Ideas"

    def save(self, *args, **kwargs): 

        credentials = {
            "developer_token": os.environ.get("DEV_token"),
            "refresh_token": os.environ.get("refresh_token"),
            "client_id": os.environ.get("client_id"),
            "client_secret": os.environ.get("client_secret"),
            "use_proto_plus": False}
        googleads_client = GoogleAdsClient.load_from_dict(credentials)
        df = main(googleads_client, "2133384368",["1023191"], "1000", self.keywords, self.pageUrl)
        self.result = df.to_html()
        #print(credentials)
        super().save(*args, **kwargs)