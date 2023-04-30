from django.db import models
from custom_users.models import CustomUser
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist


# Create your models here.
class Dialogue(models.Model):
    side_a = models.ForeignKey(CustomUser, related_name='side_a', on_delete=models.CASCADE)
    side_b = models.ForeignKey(CustomUser, related_name='side_b', on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.side_b == self.side_a:
            raise ValidationError('You cant have dialogue with yourself')
        else:
            d_list1 = Dialogue.objects.filter(side_a=self.side_a, side_b=self.side_b)
            d_list2 = Dialogue.objects.filter(side_a=self.side_b, side_b=self.side_a)
            if d_list1 or d_list2:
                raise ValidationError('You already have dialogue with this person')

    def get_date(self):
        return timezone.localtime(self.last_activity).strftime('%d %b %Y')

    def get_time(self):
        return timezone.localtime(self.last_activity).strftime('%H:%M')

    class Meta:
        ordering = ['-last_activity']

