from django.db import models


class State(models.Model):
    name = models.CharField(max_length=255)
    joined = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name