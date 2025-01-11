from django.db import models


class Auction(models.Model):
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()

    def __str__(self):
        return self.description

class Product(models.Model):
    name=models.CharField(max_length=100)
    start_point=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/', null=True, blank=True)
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount=models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name