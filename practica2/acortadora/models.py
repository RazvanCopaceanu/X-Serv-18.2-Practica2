from django.db import models

class Urls(models.Model):
    nombre = models.URLField()
    def __str__(self):
        return self.nombre
