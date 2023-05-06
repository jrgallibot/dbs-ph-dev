from urllib import response
from django.db import models
from django.conf import settings
from apps.utils.models import BaseModel
import CloudFlare
from django.utils import timezone

# Create your models here.
class CloudflareModel(BaseModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='CloudflareModelUser')
	account_id = models.TextField(null = True, blank = True, unique=True)
	account_token = models.TextField(null = True, blank = True, unique=True)
	email = models.EmailField(null = True, blank = True)
	key = models.TextField(null = True, blank = True, unique=True)
	nameServers = models.TextField(null = True, blank = True)
	resP = models.TextField(null = True, blank = True)
	created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
	updated_at = models.DateTimeField(blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	

	def __str__(self):
		return self.email

	class Meta:
		verbose_name = "Cloudflare"
		verbose_name_plural = "Cloudflare"

	def save(self, *args, **kwargs):
		cf = CloudFlare.CloudFlare(email=self.email, token=self.key)
		zones = cf.zones.get(params = {'per_page':100})
		sites = ''
		for zone in zones:
			zone_id = zone['id']
			zone_name = zone['name']
			sites += f"{zone_name}\n"
		self.resP = sites 
		super().save(*args, **kwargs)


class CloudflareModelUrl(models.Model):
	id = models.BigAutoField(primary_key=True)
	cloudfare_model = models.ForeignKey(CloudflareModel, on_delete=models.CASCADE)
	zone_id = models.CharField(max_length=500, blank=True, null=True)
	zone_name = models.CharField(max_length=500, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'Cloudflare_resp_url'


class CloudflarePageRule(models.Model):
	id = models.BigAutoField(primary_key=True)
	resp_url = models.ForeignKey(CloudflareModelUrl, on_delete=models.CASCADE)
	zone_id = models.CharField(max_length=500, blank=True, null=True)
	rule_id = models.CharField(max_length=500, blank=True, null=True)
	targets = models.CharField(max_length=500, blank=True, null=True)
	actions = models.CharField(max_length=500, blank=True, null=True)
	priority = models.TextField(null = True, blank = True)
	resp = models.TextField(null = True, blank = True)

	class Meta:
		managed = False
		db_table = 'Cloudflare_page_rule'


class CloudflareDNSInfo(models.Model):
	id = models.BigAutoField(primary_key=True)
	cloudflare_url = models.ForeignKey(CloudflareModelUrl, on_delete=models.CASCADE)
	record_id = models.CharField(max_length=500, blank=True, null=True)
	name = models.CharField(max_length=500, blank=True, null=True)
	type = models.CharField(max_length=500, blank=True, null=True)
	content = models.TextField(null = True, blank = True)

	class Meta:
		managed = False
		db_table = 'Cloudflare_dns_info'


class CloudflareDNS(BaseModel):

	cloudflaremodel = models.ForeignKey(CloudflareModel, on_delete=models.CASCADE)
	domain = models.CharField(max_length=200,null = True, blank = True,unique=True)
	oldDNS = models.TextField(null = True, blank = True)
	newDNS = models.TextField(null = True, blank = True)
	getDNS = models.BooleanField(default=False)
	updateDNS = models.BooleanField(default=False)
	deleteDNS = models.TextField(null = True, blank = True)
	resP = models.TextField(null = True, blank = True)
	cloudid = models.CharField(max_length=200,null = True, blank = True,unique=True)
	cloudname = models.CharField(max_length=200,null = True, blank = True,unique=True)
	pageRule = models.BooleanField(default=False)
	

	def __str__(self):
		return self.domain

	class Meta:
		verbose_name = "Cloudflare Site DNS"
		verbose_name_plural = "CloudflareDNS"

	def save(self, *args, **kwargs):
		if self.getDNS:
			cf = CloudFlare.CloudFlare(email=self.cloudflaremodel.email, token=self.cloudflaremodel.key)
			try:
				zones = cf.zones.get(params = {'name':self.domain,'per_page':1})
				zone = zones[0]
				
				zone_id = zone['id']
				self.cloudid = zone_id
				dns_records = cf.zones.dns_records.get(zone_id)
				sites = 'name,type,content\n'
				dnsids = ''
				dnsid = ''
				for dns_record in dns_records:
					r_name = dns_record['name']
					r_type = dns_record['type']
					r_value = dns_record['content']
					r_id = dns_record['id']
					sites += f'{r_name },{r_type },{r_value }\n'
					dnsids += f'{r_id},{r_name },{r_type },{r_value }\n'
					dnsid += f'{r_id}\n'
				r = cf.zones.pagerules.get(zone_id)
				self.resP = sites + '---------------------------\n' + dnsids +'---------------------------\n' +  dnsid + str(r)
			except:
				self.resP = 'Error Getting DNS'
		elif self.updateDNS:
			cf = CloudFlare.CloudFlare(email=self.cloudflaremodel.email, token=self.cloudflaremodel.key)
			try:
				zones = cf.zones.get(params = {'name':self.domain,'per_page':1})
				zone = zones[0]
				
				zone_id = zone['id']

				sites = 'name,type,content'.split(',')
				dns_records = []
				for i in self.newDNS.split('\n'):
					dns_records.append(dict(zip(sites,i.replace('\r','').split(','))))
				
				if self.deleteDNS:
					delete_records = self.deleteDNS.split('\n')
					for dns_record_id in delete_records:
						r = cf.zones.dns_records.delete(zone_id, dns_record_id.replace('\r',''))
						self.resP += f'\ndeleted {dns_record_id} record'

				#self.resP = '\n'.join(dns_records)
				self.resP = f'Updated {len(dns_records)} records '
				if self.newDNS:
					for dns_record in dns_records:

						r = cf.zones.dns_records.post(zone_id, data=dns_record)
						self.resP += '\nUpdated DNS Record'


			except:
				self.resP += 'Error Updating DNS'
		elif self.pageRule:
			cf = CloudFlare.CloudFlare(email=self.cloudflaremodel.email, token=self.cloudflaremodel.key)
			zones = cf.zones.get(params = {'name':self.domain,'per_page':1})
			print(zones)
			zone = zones[0]
			zone_id = zone['id']
			url_match=f"{self.domain}/*"
			url_forwarded=f"https://www.{self.domain}/$1"
			targets=[{"target":"url","constraint":{"operator":"matches","value":url_match}}]
			actions=[{"id":"forwarding_url","value":{"status_code":301,"url":url_forwarded}}]
			pagerule_for_redirection = {"status": "active","priority": 1,"actions": actions,"targets": targets}
			r = cf.zones.pagerules.post(zone_id, data=pagerule_for_redirection)
			print('results', r)
			print(r['id'])
		self.updateDNS = False
		self.getDNS = False
		super().save(*args, **kwargs)
