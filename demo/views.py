from django.shortcuts import render

from .seach_service import SearchService


search_service = SearchService()

def index(request):
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request, "index.html", context=data)

def movie(request, id):
    return render(request, f"movies/{id}.html")

def search(request):
    context = {}

    if request.POST.get('query'):
        context['query'] = request.POST.get('query')
        context['data'] = search_service.search(request.POST.get('query'))

    return render(request, "index.html", context)