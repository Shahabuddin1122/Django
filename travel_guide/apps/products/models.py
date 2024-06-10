import uuid

from django.db import models


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# Create your models here.
class product(BaseModel):
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    image = models.TextField(blank=True, null=True)
    category = models.TextField()
    subcategory = models.TextField()
