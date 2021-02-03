from django.contrib.sitemaps import Sitemap
from .models import Post

# XML data which can be analysed by browsers
class PostSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated