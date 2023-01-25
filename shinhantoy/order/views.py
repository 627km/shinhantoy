from django.shortcuts import render
from rest_framework import mixins, generics
from .models import Order
from .serializers import OrderSerializer
from .paginations import OrderPagination

# Create your views here.
class OrderListView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return Order.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)
    
    