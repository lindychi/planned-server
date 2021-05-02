from django.db import models
from django.conf import settings

# Create your models here.
class Wiki(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now=True, auto_created=True)

    def get_content(self):
        return self.content.replace('\n','</br>')