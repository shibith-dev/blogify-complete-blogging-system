from .models import Category
from base.models import SocialLink

def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def get_sociallinks(request):
    links = SocialLink.objects.all()
    return dict(social_links=links)
