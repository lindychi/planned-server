from django.contrib import admin
from .models import IterTodo, Todo

# Register your models here.
admin.site.register(Todo)
admin.site.register(IterTodo)