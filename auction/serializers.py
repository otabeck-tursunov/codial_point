from rest_framework.serializers import ModelSerializer

from .models import *

class AuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'



class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

