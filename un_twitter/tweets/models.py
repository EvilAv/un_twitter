from django.db import models


# Create your models here.
class Test(models.Model):
    text = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

    def serialize(self):
        return {
            'text': self.text
        }


class Date_Test(models.Model):
    test_date = models.DateField()