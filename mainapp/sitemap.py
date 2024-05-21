from django.contrib.sitemaps import Sitemap
from .models import ArticleModel

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return ArticleModel.published.all()
    
    def lastmod(self, obj: ArticleModel):
        return obj.time_updated
    
    
# class CategorySitemap(Sitemap):
#     changefreq = 'weekly'
#     priority = 0,85
    
#     def items(self):
#         return Category.objects.all()