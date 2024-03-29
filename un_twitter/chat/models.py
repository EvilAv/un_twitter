from django.db import models
from custom_users.models import CustomUser
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist


# Create your models here.
class Dialogue(models.Model):
    side_a = models.ForeignKey(CustomUser, related_name='side_a', on_delete=models.CASCADE)
    side_b = models.ForeignKey(CustomUser, related_name='side_b', on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)
    msg_count = models.IntegerField(default=0)
    is_read_by_side_a = models.BooleanField(default=True)
    is_read_by_side_b = models.BooleanField(default=True)

    def clean(self):
        if self.side_b == self.side_a:
            raise ValidationError('You cant have dialogue with yourself')
        else:
            d_list1 = Dialogue.objects.filter(side_a=self.side_a, side_b=self.side_b)
            d_list2 = Dialogue.objects.filter(side_a=self.side_b, side_b=self.side_a)
            if d_list1 and d_list1[0].pk != self.pk:
                raise ValidationError('You already have dialogue with this person')
            if d_list2 and d_list2[0].pk != self.pk:
                raise ValidationError('You already have dialogue with this person')

    def get_date(self):
        return timezone.localtime(self.last_activity).strftime('%d %b %Y')

    def get_time(self):
        return timezone.localtime(self.last_activity).strftime('%H:%M')

    def self_check(self):
        if self.msg_count <= 0:
            self.delete()

    class Meta:
        ordering = ['-last_activity']


class Message(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def get_date(self):
        return timezone.localtime(self.date).strftime('%d %b %Y')

    def get_time(self):
        return timezone.localtime(self.date).strftime('%H:%M')

    def mark_as_read(self):
        if not self.read:
            self.read = True
            dialogue = self.dialogue

            if dialogue.side_a != self.author:
                dialogue.is_read_by_side_a = True
            else:
                dialogue.is_read_by_side_b = True
            dialogue.save()
            self.save()

    def save(self, *args, **kwargs):
        if not self.read:
            self.dialogue.msg_count += 1
            self.dialogue.last_activity = self.date
            if self.dialogue.side_a == self.author:
                self.dialogue.is_read_by_side_b = False
            else:
                self.dialogue.is_read_by_side_a = False
            self.dialogue.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.dialogue.msg_count -= 1
        if self.dialogue.msg_count > 0:
            self.dialogue.last_activity = Message.objects.filter(dialogue=self.dialogue).reverse()[0].date
        self.dialogue.save()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return str(self.text) + ' status: ' + str(self.read)
