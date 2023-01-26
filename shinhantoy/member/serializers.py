from rest_framework import serializers
from .models import Member
from django.contrib.auth.hashers import make_password

class MemberSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Too Short password')
        return make_password(value)

    class Meta:
        model = Member
        fields = ('id', 'username', 'tel', 'password')
        extra_kwargs = {
            'id' : {
                'read_only' : True,
            }, 
            'password' : {
                'write_only' : True,
            }
        }