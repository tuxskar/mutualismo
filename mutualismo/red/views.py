from django.shortcuts import render_to_response

def index(request):
    """Index page."""
    return render_to_response('index.html',)

def about(request):
    """About page."""
    return render_to_response('about.html',)
