from django.utils import timezone
from rest_framework import serializers

from interview.order.models import Order, OrderTag
from interview.inventory.serializers import InventorySerializer


class OrderTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderTag
        fields = ['id', 'name', 'is_active']


class OrderSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()
    tags = OrderTagSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'inventory', 'start_date', 'embargo_date', 'tags', 'is_active']


class OrderDeactivateSerializer(OrderSerializer):
    def update(self, instance, valiated_data):
        instance.is_active = False
        instance.updated_at = timezone.now()
        instance.save()
        return instance
