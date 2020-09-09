from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')




# This  is data model for blog posts
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    #This field is CharField, which translates into a Varchar column in the SQL database
    title = models.CharField(max_length=250)
 
    #This is a field intended to be used in URLs. A slug is a short label that contains only letters, numbers
    # underscores, or hypens.
    slug = models.SlugField(max_length=250,unique_for_date='publish')

    #This field define many-to-one realtionship 
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
    
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.


    




    #The meta class inside the model contains metadata.
    class Meta:
        ordering = ('-publish',)
       

    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                            args=[self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug
                            ]
                            )