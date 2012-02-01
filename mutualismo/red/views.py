from django.views.generic.simple import direct_to_template

def index(request):
    """Index page."""
    return direct_to_template(request, template='index.html',)

def about(request):
    """About page."""
    return direct_to_template(request, template='about.html',)
