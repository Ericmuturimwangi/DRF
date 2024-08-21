from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE

# Create your models here.


class BookModel(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        "auth.User", max_length=100, default=None, null=True, on_delete=CASCADE
    )
    price = models.IntegerField(default=0)
