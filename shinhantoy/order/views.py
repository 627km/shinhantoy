from django.shortcuts import render
from rest_framework import mixins, generics
from .models import Order, Comment
from .serializers import OrderSerializer, CommentSerializer, CommentCreateSerializer, CommentDeleteSerializer
from .paginations import OrderPagination
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class OrderListView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return Order.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)
    
class OrderDetailView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)

class CommentListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    def get_permission_classes(self):
        if self.request.method == "POST":
            return [IsAuthenticated]
        return None

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
       pk = self.kwargs.get('pk')
       return Comment.objects.filter(order_id = pk).order_by('-id')

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

class CommentDeleteVeiw(
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
): 
    serializer_class = CommentDeleteSerializer
    
    def get_queryset(self):
        member_id = self.request.user.id
        return Comment.objects.filter(member_id = member_id)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)
        