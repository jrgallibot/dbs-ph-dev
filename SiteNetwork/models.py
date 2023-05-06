from django.db import models
from django.conf import settings
from apps.utils.models import BaseModel
import whois
# Create your models here.
import pandas as pd
from ckeditor.fields import RichTextField
from urllib.parse import urlparse
import requests
class Sites(BaseModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='SiteNetworkUser')
    site = models.URLField(null = True, blank = True)
    status = models.CharField(max_length=60,null = True, blank = True)
    niche = models.CharField(max_length=60,null = True, blank = True)
    

    def __str__(self):
        return self.site

    class Meta:
        verbose_name = "Potential Site"
        verbose_name_plural = "Potential Sites"


# Create your models here.
class Backlinks(BaseModel):

    Page = models.ForeignKey(Sites, on_delete=models.CASCADE)
    backlink = models.URLField(null = True, blank = True)
    anchor = models.CharField(max_length=60,null = True, blank = True)
    rebuildPage = models.CharField(max_length=60,null = True, blank = True)
    numberOfLinks = models.IntegerField(default=1,null = True, blank = True)
    DR = models.IntegerField(default=0,null = True, blank = True)
    traffic = models.IntegerField(default=0,null = True, blank = True)
    

    def __str__(self):
        return self.backlink

    class Meta:
        verbose_name = "Backlink"
        verbose_name_plural = "Backlinks"


class DigitalProperty(BaseModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='DigitalPropertyUser')
    domain = models.URLField(null = True, blank = True, unique=True)
    nameserver = models.TextField(null = True, blank = True)
    registrar = models.CharField(max_length=300,null = True, blank = True)
    expireDate = models.DateField(null = True, blank = True)
    traffic =  models.IntegerField(default=0,null = True, blank = True)
    status = models.CharField(max_length=300,null = True, blank = True, default = 'PBN')
    niche = models.CharField(max_length=300,null = True, blank = True)
    importance = models.CharField(max_length=300,null = True, blank = True)
    notes = models.TextField(null = True, blank = True)
    backlinks = RichTextField(null = True, blank = True)
    Whois = models.BooleanField(default=True)
    urlshortner = models.TextField(null = True, blank = True)
    

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = "Digital Property"
        verbose_name_plural = "Digital Properties"

    def save(self, *args, **kwargs):
        if self.Whois:
            w = whois.whois(self.domain)
            if type(w.expiration_date) is list:
                self.expireDate = w.expiration_date[0]
            else:
                self.expireDate = w.expiration_date
            self.nameserver = '\n'.join(w.name_servers)
            self.registrar = w.registrar
            #self.notes = w
            u = urlparse(self.domain)
            r = requests.get(f'https://apiv2.ahrefs.com/?from=backlinks_one_per_domain&target={u.netloc}&mode=subdomains&limit=10&order_by=total_backlinks%3Adesc&output=json&token=CmM6tB8o70dCs7GGuwrPqVB_y4dPE1gRZ77nS_Sv')
            df = pd.DataFrame.from_dict(r.json()['refpages'])
            self.backlinks = df[['url_from','title','domain_rating','ahrefs_top','ahrefs_rank','total_backlinks','url_to','link_type','anchor','last_visited',]].to_html()
            self.Whois = False


        super().save(*args, **kwargs)
