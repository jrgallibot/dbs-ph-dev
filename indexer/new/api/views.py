from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from indexer.models import *
from apps.users.models import *
from mobile_friendly.models import *
from image_optimizer.models import *
from open_ai.models import *
from Cloudflare.models import *
from . serializers import IndexApiListSerializers, IndexApiDetailSerializers, IndexWebsiteListSerializers, IndexPagesSerializers, \
	LogsSerializer, UsageIndexListSerializers, IndexApiMethodTypeSerializers, MobileFriendlyListSerializers, MobileFriendlyPagesSerializers, \
	SitemapListSerializers, SitemapPagesSerializers, ListofUsersSerializers, RankTrackerSerializer, RankTrackerHistoryCostSerializer, \
	RankTrackerCostSerializer, ImageOptimizerSerializers, ImageOptimizerFileSerializers, OpenAiContentSerializers, OpenAiAssistedGCSerializers, \
	OpenAiAssistedGCHeadersSerializers, OpenAiPromptSerializers, OpenAiPromptParentSerializers, CloudFlareApiSerializers, CloudflareModelUrlSerializers


class CloudflareModelUrllListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = CloudflareModelUrlSerializers

	def get_queryset(self):
		return CloudflareModelUrl.objects.filter(cloudfare_model_id=self.kwargs['pk'])
	

class CloudflareModelListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = CloudFlareApiSerializers

	def get_queryset(self):
		return CloudflareModel.objects.filter(user_id=self.kwargs['pk']).order_by('-created_at')
		# check_is_super_admin = CustomUser.objects.filter(id = self.kwargs['pk']).first()
		# if check_is_super_admin.is_superuser == True:
		# 	print('is_super_admin')
		# 	return CloudflareModel.objects.all().order_by('-created_at')
		# else:
		# 	print('is_not_super_admin')
		# 	return CloudflareModel.objects.filter(user_id=self.kwargs['pk']).order_by('-created_at')
			


class OpenAiPromptParentListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = OpenAiPromptParentSerializers

	def get_queryset(self):
		return OpenAiPromptParent.objects.all().order_by('-dateadded')


class OpenAiPromptListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = OpenAiPromptSerializers

	def get_queryset(self):
		return OpenAiPrompt.objects.all().order_by('-dateadded')

class OpenAiAssistedGCHeadersListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = OpenAiAssistedGCHeadersSerializers

	def get_queryset(self):
		return OpenAiAssistedGCHeaders.objects.filter(ass_id=self.kwargs['pk'])


class OpenAiAssistedGCListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = OpenAiAssistedGCSerializers

	def get_queryset(self):
		return OpenAiAssistedGC.objects.filter(user_id=self.kwargs['pk'])


class OpenAiContentListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = OpenAiContentSerializers

	def get_queryset(self):
		return OpenAiContent.objects.filter(user_id=self.kwargs['pk'])


class ImageOptimizerListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ImageOptimizerSerializers

	def get_queryset(self):
		return ImageOptimizer.objects.filter(user_id=self.kwargs['pk'])


class ImageOptimizerFileView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ImageOptimizerFileSerializers

	def get_queryset(self):
		return ImageOptimizerFile.objects.filter(img_op_id=self.kwargs['pk'])


class RankSearchListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = RankTrackerSerializer

	def get_queryset(self):
		return RankTracker.objects.filter(user_id=self.kwargs['pk'])


class RankSearchOverALlTotalCostListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = RankTrackerCostSerializer

	def get_queryset(self):
		user_id = CustomUser.objects.values_list('id')
		return CustomUser.objects.all()



class RankTrackerHistoryCostView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = RankTrackerHistoryCostSerializer

	def get_queryset(self, **kwargs):
		return RankTrackerHistoryCost.objects.filter(rank_id=self.kwargs['pk'])


class ListofusersView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ListofUsersSerializers

	def get_queryset(self):
		return CustomUser.objects.all().order_by("-date_joined")


class IndexApiTypeMethodView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexApiMethodTypeSerializers

	def get_queryset(self):
		return IndexerApiType.objects.all().order_by("-date_added")


class IndexApiTypeDetailView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexApiMethodTypeSerializers

	def get_queryset(self, **kwargs):
		return IndexerApiType.objects.filter(id=self.kwargs['pk'])


class IndexApiListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexApiListSerializers

	def get_queryset(self):
		return IndexApi.objects.all().order_by("-id")


class UsageIndexListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = UsageIndexListSerializers

	def get_queryset(self, **kwargs):
		return IndexerApiUsageTracking.objects.filter(api_id = self.kwargs['pk']).order_by("-date_created")


class IndexApiDetailView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexApiDetailSerializers

	def get_queryset(self, **kwargs):
		return IndexApi.objects.filter(id=self.kwargs['pk'])


class IndexWebsitesListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexWebsiteListSerializers

	def get_queryset(self):
		return Website.objects.all()



class IndexWebPagesDetailView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexPagesSerializers

	def get_queryset(self, **kwargs):
		return IndexerPages.objects.filter(web_id=self.kwargs['pk'])


class LogsView(LoginRequiredMixin, generics.ListAPIView):
	queryset = Loghistory.objects.all().order_by('-datetime_added')
	serializer_class = LogsSerializer
	permission_classes = [IsAuthenticated]



#MOBIE FRIENDLY VIEWS
class MobileFriendlyListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = MobileFriendlyListSerializers

	def get_queryset(self):
		return MobileFriendWeb.objects.all()


class MobileFriendlyPagesView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = MobileFriendlyPagesSerializers

	def get_queryset(self):
		return MobileFriendlyPages.objects.filter(web_id=self.kwargs['pk'])


#USER SIDE
class UserIndexApiListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexApiListSerializers

	def get_queryset(self):
		return IndexApi.objects.filter(user_id=self.kwargs['pk']).order_by("-id")


class UserIndexApiListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexApiListSerializers

	def get_queryset(self):
		return IndexApi.objects.filter(user_id=self.kwargs['pk']).order_by("-id")


class UserIndexWebsitesListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexWebsiteListSerializers

	def get_queryset(self):
		return Website.objects.filter(user_id=self.kwargs['pk']).order_by("-id")


class UserIndexWebPagesDetailView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = IndexPagesSerializers

	def get_queryset(self, **kwargs):
		return IndexerPages.objects.filter(web_id=self.kwargs['pk'])

class UserMobileFriendlyListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = MobileFriendlyListSerializers

	def get_queryset(self):
		return MobileFriendWeb.objects.filter(user_id=self.kwargs['pk']).order_by("-id")


class UserMobileFriendlyPagesView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = MobileFriendlyPagesSerializers

	def get_queryset(self):
		return MobileFriendlyPages.objects.filter(web_id=self.kwargs['pk'])


class UserSiteMapListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = SitemapListSerializers

	def get_queryset(self):
		return Sitemap.objects.filter(user_id=self.kwargs['pk']).order_by("-id")


class UserSiteMapPagesView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = SitemapPagesSerializers

	def get_queryset(self):
		return SitemapPages.objects.filter(sitemap_id=self.kwargs['pk'])


class SiteMapListView(LoginRequiredMixin, generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = SitemapListSerializers

	def get_queryset(self):
		return Sitemap.objects.all().order_by("-id")