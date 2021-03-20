from django.conf import settings
from django.db import models

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('Todo', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=2048)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return "[{0}] {1}".format(self.user, self.name)

    def get_child(self):
        return Todo.objects.filter(parent=self)