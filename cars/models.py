from django.db import models

# Create your models here.

from django.db.models import Max


class CarModel(models.Model):
    choose = (('blue', 'Blue'), ('red', 'Red'))
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=50, choices=choose)
    seq_number = models.IntegerField(default=0)

    class Meta:
        ordering = ['seq_number']

    def __str__(self):
        return self.name

    def handle_number_create(self):
        pk = self.objects.order_by('-id')[0]
        queryset = self.objects.get(id=pk.id)
        highest = self.objects.aggregate(Max("seq_number"))
        queryset.seq_number = highest['seq_number__max'] + 1
        queryset.save()
