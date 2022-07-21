from django.db   import models

from core.models import TimeStampModel


class Post(TimeStampModel):
    
    STATUS_TYPES = [
        ('in_posting', 'Post in posting'),
        ('deleted',    'Post deleted'),
    ]
    
    users   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    tags    = models.ManyToManyField('Tag', related_name='posts')
    content = models.TextField()
    title   = models.CharField(max_length=100)
    views   = models.PositiveIntegerField(default=0)
    status  = models.CharField(max_length=200, choices=STATUS_TYPES, default='in_posting')
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'posts'
        

class Tag(TimeStampModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'    