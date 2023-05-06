from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from wagtail.models import Page, Site

from apps.content.models import ContentPage, BlogIndexPage, BlogPage


class Command(BaseCommand):
    help = 'Bootstraps your initial Wagtail / blog set up'

    def handle(self, **options):
        bootstrap_initial_content()


def bootstrap_initial_content():
    root_page = Page.objects.get(slug='root').specific
    print('creating your content homepage...')
    try:
        landing_page = ContentPage.objects.get(slug='content')
    except ContentPage.DoesNotExist:
        landing_page = ContentPage(
            slug='content',
            title="Welcome to your content area!",
            body='This is where your blog lives. You can also create other pages here. '
                 'Everything here can be edited in <a href="/cms">the content admin</a>.',
        )
        root_page.add_child(instance=landing_page)
        landing_page.save()
    site = Site.objects.get()
    site.root_page = landing_page
    site.save()

    print('creating your blog index page...')
    try:
        blog_index = BlogIndexPage.objects.get(slug='blog')
    except BlogIndexPage.DoesNotExist:
        blog_index = BlogIndexPage(
            slug='blog',
            title='Blog',
            intro='Welcome to our blog!',
        )
        landing_page.add_child(instance=blog_index)
        blog_index.save()

    print('creating some blog posts...')
    try:
        blog_post = BlogPage(
            slug='pegasus-and-wagtail',
            title='Pegasus and Wagtail',
            date=datetime.today(),
            intro='A introduction to using Wagtail with Pegasus',
            body=BLOG_POST_HTML,
        )
        blog_index.add_child(instance=blog_post)
        blog_post.save()
        blog_post_2 = BlogPage(
            slug=f'another-post',
            title=f'Another Blog Post',
            date=datetime.today() - timedelta(days=1),
            intro='A second post, with other interesting information.',
            body='This is the body of the post. You can edit these in <a href="/cms">the content admin</a>.',
        )
        blog_index.add_child(instance=blog_post_2)
        blog_post_2.save()
    except ValidationError:
        # probably already ran bootstrap
        print('Blog posts already found... leaving things alone')

BLOG_POST_HTML = """<h2 data-block-key="bl7pc">What is Wagtail?</h2><p data-block-key="1cn7m"><a href="https://wagtail.org/">Wagtail</a> is a powerful CMS (Content Management System) built on top of Django. You can use it to create rich websites that can be edited directly via an authoring admin interface without writing any code. It&#x27;s great for creating marketing sites, blogs, and other mostly-static content.</p><h2 data-block-key="4j1t8">How do I use it?</h2><p data-block-key="464op">If you&#x27;re reading this page, <b>you already are</b>! This page is created with wagtail. What&#x27;s really great about Wagtail is that you can use it to create and edit content without writing any code.</p><p data-block-key="e0136">To see it in action, head over to <a href="/cms">the content admin</a> section of your app (you&#x27;ll have to <a href="https://docs.saaspegasus.com/cookbooks.html?highlight=superuser#use-the-django-admin-ui">be a superuser</a> to access this). From there find the page with the title &quot;Pegasus and Wagtail&quot; and try modifying it via the &quot;edit&quot; button. You can add sections, images, and more!</p><h2 data-block-key="4ic6d">Next steps</h2><p data-block-key="5gvdg">Now that you&#x27;ve seen how easy it is to add content to your site, try adding some more. Create a few more blog posts, try adding images, different styles of text, even embedded videos!</p><hr/><p data-block-key="5mvpd"><i>For more information on how this works - check out the </i><a href="https://docs.saaspegasus.com/wagtail"><i>SaaS Pegasus docs on wagtail</i></a><i>.</i></p>"""
