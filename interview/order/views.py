from datetime import datetime

from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer, OrderDeactivateSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        date_str = request.GET.get("between_date")
        filter_q = Q()
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            filter_q = (
                Q(start_date__lte=date, embargo_date__gt=date) |
                Q(embargo_date__lte=date, start_date__gt=date)
            )
        serializer = self.serializer_class(self.get_queryset().filter(filter_q), many=True)

        return Response(serializer.data, status=200)


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderDeactivateSerializer

    def patch(self, request: Request, *args, **kwargs) -> Response:
        order = self.get_queryset(id=kwargs['id'])

        serializer = self.serializer_class(order, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
