from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index_page(request):
    context = {
        'title': 'landing',
    }
    return render(request, 'indexing/index.html', context)

