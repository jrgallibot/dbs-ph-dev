from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import IndexApi, Website, Sitemap
from .forms import IndexerForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import resolve
from django.db import transaction
from celery import current_app


@login_required
def indexing(request):
    context = {
        'title': 'landing',
    }
    return render(request, 'indexing/landing.html', context)


class IndexApiListView(ListView):
    model = IndexApi

    def get_queryset(self):
        return IndexApi.objects.filter(user=self.request.user).order_by("-id")


class IndexApiDetailView(DetailView):
    context_object_name = 'indexapi'

    def get_queryset(self):
        return IndexApi.objects.filter(user=self.request.user).order_by("-id")


class IndexApiCreateView(LoginRequiredMixin, CreateView):
    model = IndexApi
    fields = ['email', 'indexApi']

    def form_valid(self, form):
        # form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # return super().form_valid(form)
        current_url = reverse('indexer_app:IndexApilist')
        return HttpResponseRedirect(f'{current_url}edit/{pk}')


class IndexApiUpdateView(LoginRequiredMixin, UpdateView):
    model = IndexApi
    fields = ['email', 'indexApi']

    template_name_suffix = '_update_form'
    success_url = '/indexer/'

    def get_success_url(self):
        return reverse('indexer_app:indexerupdate', args=(self.object.id,))


class WebsiteListView(ListView):
    model = Website

    def get_queryset(self):
        return Website.objects.filter(indexapi__user=self.request.user).order_by("-id")


class WebsiteDetailView(DetailView):
    context_object_name = 'website'

    def get_queryset(self):
        return Website.objects.filter(indexapi__user=self.request.user).order_by("-id")


class WebsiteCreateView(LoginRequiredMixin, CreateView):
    model = Website
    fields = ['indexapi', 'website', 'pages', 'jsonFile', 'JsonResponse']

    def form_valid(self, form):
        # form.instance.indexapi.user = self.request.user
        self.object = form.save(commit=False)
        self.object.indexapi.user = self.request.user
        self.object.save()
        # return super().form_valid(form)
        pk = self.object.id
        current_url = reverse('indexer_app:IndexApilist')
        return HttpResponseRedirect(f'{current_url}pages/edit/{pk}')


class WebsiteUpdateView(LoginRequiredMixin, UpdateView):
    model = Website
    fields = ['indexapi', 'website', 'pages', 'jsonFile', 'JsonResponse', 'check_index', 'index_now', 'RunIndexer5']

    template_name_suffix = '_update_form'

    def form_valid(self, form):
        transaction.on_commit(lambda: current_app.send_task(
            "update_index_rate",
            kwargs={"model_id": self.object.id},
            queue="default",
            ignore_result=False,
        ))
        return super(WebsiteUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('indexer_app:websiteupdate', args=(self.object.id,))


class SitemapCreateView(LoginRequiredMixin, CreateView):
    model = Sitemap
    fields = ['website', 'results']

    def form_valid(self, form):
        # form.instance.indexapi.user = self.request.user
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        pk = self.object.id
        current_url = reverse('indexer_app:sitemaplist')
        transaction.on_commit(lambda: current_app.send_task(
            "update_sitemap_task",
            kwargs={"model_id": self.object.id},
            queue="default",
            ignore_result=False,
        ))
        return HttpResponseRedirect(f'{current_url}edit/{pk}')


class SitemapUpdateView(LoginRequiredMixin, UpdateView):
    model = Sitemap
    fields = ['website', 'results']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('indexer_app:sitemapupdate', args=(self.object.id,))


class SitemapListView(ListView):
    model = Sitemap

    def get_queryset(self):
        return Sitemap.objects.filter(user=self.request.user).order_by("-id")
