from django.db import models
from webapp.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
class Schedule(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    event = models.TextField(max_length=100)
    date = models.DateField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title



# for automatically generating unique slug for every new event created


def slug_generater(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.reporter.email+"-"+instance.title)

pre_save.connect(slug_generater, sender=Schedule)