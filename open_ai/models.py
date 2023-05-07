from django.db import models
import uuid
from indexer.models import IndexApi
from django.utils import timezone
from django.conf import settings


class OpenAiContent(models.Model):
	id = models.BigAutoField(primary_key=True)
	keyword = models.TextField(blank=True, null=True)
	results = models.JSONField(verbose_name='Result')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	dateadded = models.DateTimeField(blank=True, null=True, default=timezone.now)
	status = models.CharField(max_length=100, blank=True, null=True)

	@property
	def get_prompt(self):
		data = OpenAiCGPrompt.objects.filter(cg_id = self.id).first()
		if data:
			return data.prompt.name
		
	class Meta:
		managed = False
		db_table = 'open_ai_content_generate'


class OpenAiContentResults(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	results = models.JSONField(verbose_name='Result')
	order_by = models.IntegerField(blank=True, null=True)
	content = models.ForeignKey(OpenAiContent, on_delete=models.CASCADE)
	

	class Meta:
		managed = False
		db_table = 'open_ai_content_results'


class OpenAiKey(models.Model):
	id = models.BigAutoField(primary_key=True)
	api = models.TextField(blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'open_ai_key'



class OpenAiPrompt(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	prompt = models.TextField(blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	order = models.IntegerField(blank=True, null=True)
	dateadded = models.DateTimeField(blank=True, null=True, default=timezone.now)
	updated_at = models.DateTimeField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'open_ai_prompt'


class OpenAiPromptParent(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	dateadded = models.DateTimeField(blank=True, null=True, default=timezone.now)

	@property
	def get_prompt_sub_parent(self):
		data = OpenAiPromptSubParent.objects.filter(parent_id = self.id).all()
		return data

	class Meta:
		managed = False
		db_table = 'open_ai_prompt_parent'


class OpenAiAssistedGC(models.Model):
	id = models.BigAutoField(primary_key=True)
	title = models.TextField(blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	dateadded = models.DateTimeField(blank=True, null=True, default=timezone.now)
	status = models.IntegerField(blank=True, null=True)
	prompt = models.ForeignKey(OpenAiPromptParent, on_delete=models.CASCADE)
	is_cg = models.IntegerField(blank=True, null=True)
	cg_status = models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'open_ai_assisted_gc'


class OpenAiAssistedGCHeaders(models.Model):
	id = models.BigAutoField(primary_key=True)
	headers = models.TextField(blank=True, null=True)
	ass = models.ForeignKey(OpenAiAssistedGC, on_delete=models.CASCADE)
	dateadded = models.DateTimeField(blank=True, null=True, default=timezone.now)
	status = models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'open_ai_assisted_gc_headers'


class OpenAiAssistedGCResults(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	results = models.JSONField(verbose_name='Result')
	order_by = models.IntegerField(blank=True, null=True)
	headers = models.ForeignKey(OpenAiAssistedGCHeaders, on_delete=models.CASCADE)
	

	class Meta:
		managed = False
		db_table = 'open_ai_assisted_gc_headers_results'


class OpenAiPromptSubParent(models.Model):
	id = models.BigAutoField(primary_key=True)
	parent = models.ForeignKey(OpenAiPromptParent, on_delete=models.CASCADE)
	prompt = models.ForeignKey(OpenAiPrompt, on_delete=models.CASCADE)

	class Meta:
		managed = False
		db_table = 'open_ai_prompt_sub_parent'


class OpenAiCGPrompt(models.Model):
	id = models.BigAutoField(primary_key=True)
	prompt = models.ForeignKey(OpenAiPromptParent, on_delete=models.CASCADE)
	cg = models.ForeignKey(OpenAiContent, on_delete=models.CASCADE)
	dateadded = models.DateTimeField(blank=True, null=True, default=timezone.now)

	class Meta:
		managed = False
		db_table = 'open_ai_cg_prompt'