from django.db import models


class Site(models.Model):

    name = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)
    

class Page(models.Model):
    '''
        Model for saving web pages
    '''
    uri = models.URLField(max_length=250)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return str(self.title)

class ExceptedPages(models.Model):
    '''
        Model for saving web pages
    '''
    uri = models.URLField(max_length=250)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.uri)

class PageImages(models.Model):

    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    image = models.ImageField()
