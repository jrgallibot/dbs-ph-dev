from rest_framework import serializers
from indexer.models import *
from mobile_friendly.models import *
from image_optimizer.models import *
from apps.users.models import *
from open_ai.models import *
from Cloudflare.models import *

class OpenAiPromptParentSerializers(serializers.ModelSerializer):
    dateadded = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    sub_parent = serializers.CharField(source='get_prompt_sub_parent', read_only=True, allow_null=True)

    class Meta:
        model = OpenAiPromptParent
        fields = ['id', 'name', 'dateadded', 'status', 'sub_parent']


class OpenAiPromptSerializers(serializers.ModelSerializer):
    dateadded = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    
    class Meta:
        model = OpenAiPrompt
        fields = '__all__'


class OpenAiAssistedGCSerializers(serializers.ModelSerializer):
    dateadded = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    prompt = serializers.CharField(source='prompt.name', read_only=True, allow_null=True)

    class Meta:
        model = OpenAiAssistedGC
        fields = '__all__'


class OpenAiAssistedGCHeadersSerializers(serializers.ModelSerializer):
    dateadded = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    ass_id = serializers.CharField(source='ass.id', read_only=True)

    class Meta:
        model = OpenAiAssistedGCHeaders
        fields = '__all__'


class OpenAiContentSerializers(serializers.ModelSerializer):
    dateadded = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    prompt = serializers.CharField(source='get_prompt', read_only=True, allow_null=True)
    
    class Meta:
        model = OpenAiContent
        fields = '__all__'


class ImageOptimizerFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageOptimizerFile
        fields = '__all__'


class ImageOptimizerSerializers(serializers.ModelSerializer):
    datetime_added = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    
    class Meta:
        model = ImageOptimizer
        fields = '__all__'


class IndexApiMethodTypeSerializers(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    
    class Meta:
        model = IndexerApiType
        fields = '__all__'


class IndexApiListSerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    usage = serializers.CharField(source='get_api_usage', read_only=True)
    method = serializers.CharField(source='method.type_method', read_only=True)

    
    class Meta:
        model = IndexApi
        fields = '__all__'


class IndexApiDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = IndexApi
        fields = '__all__'


class UsageIndexListSerializers(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)

    class Meta:
        model = IndexerApiUsageTracking
        fields = '__all__'


class IndexWebsiteListSerializers(serializers.ModelSerializer):
    email = serializers.CharField(source='indexapi.email', read_only=True)
    created_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    
    class Meta:
        model = Website
        fields = '__all__'


class IndexPagesSerializers(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    indexed_date = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    web = serializers.CharField(source='web.website', read_only=True)
    web_id = serializers.CharField(source='web.id', read_only=True)
    
    class Meta:
        model = IndexerPages
        fields = '__all__'


class LogsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    descriptions = serializers.CharField(read_only=True)
    user = serializers.CharField(source='user.first_name', read_only=True)
    datetime_added = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)

    class Meta:
        model = Loghistory
        fields = ['id', 'descriptions', 'user', 'datetime_added']


class SitemapListSerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    apikey = serializers.CharField(source='apikey.email', read_only=True)
    
    class Meta:
        model = Sitemap
        fields = '__all__'


class SitemapPagesSerializers(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%b %d, %Y", read_only=True)
    sitemap = serializers.CharField(source='sitemap.website', read_only=True)
    last_mod = serializers.DateTimeField(source='get_sitemap_lastmod', format="%b %d, %Y", read_only=True)
    updated_at = serializers.DateTimeField(source='get_sitemap_updated_at', format="%b %d, %Y", read_only=True)
    sitemap_id = serializers.CharField(source='sitemap.id', read_only=True)
    lastcrawltime = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)

    class Meta:
        model = SitemapPages
        fields = ['id', 'date_created', 'sitemap', 'last_mod', 'updated_at', 'pages', 'time_executed', 'rank', 'sitemap_id',
                    'conanical_url', 'status', 'lastcrawltime', 'indexStatusResult']
        

#MOBILE FRIENDLY SERIALIZERS
class MobileFriendlyListSerializers(serializers.ModelSerializer):
    email = serializers.CharField(source='api.email', read_only=True)
    date_created = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    
    class Meta:
        model = MobileFriendWeb
        fields = '__all__'

class MobileFriendlyPagesSerializers(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    web = serializers.CharField(source='web.website', read_only=True)
    
    class Meta:
        model = MobileFriendlyPages
        fields = '__all__'


#LIST OF USERS SERIALIZERS
class ListofUsersSerializers(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    last_login = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    client_settings = serializers.CharField(source='get_client_settings', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = '__all__'


#RANK SEARCH
class RankTrackerSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)

    class Meta:
        model = RankTracker
        fields = '__all__'

class RankTrackerHistoryCostSerializer(serializers.ModelSerializer):
    rank_id = serializers.CharField(source='rank.id', read_only=True)
    pages = serializers.CharField(source='rank.url', read_only=True)
    date_updated = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)

    class Meta:
        model = RankTrackerHistoryCost
        fields = ['id', 'rank_id', 'pages', 'date_updated', 'latest_rank_positions']


class RankTrackerCostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    middle_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    total_cost = serializers.CharField(source='get_total_cost', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'total_cost']


# Cloud Flare
class CloudFlareApiSerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%b %d, %Y - %H:%M %p", read_only=True)

    class Meta:
        model = CloudflareModel
        fields = '__all__'


class CloudflareModelUrlSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = CloudflareModelUrl
        fields = '__all__'