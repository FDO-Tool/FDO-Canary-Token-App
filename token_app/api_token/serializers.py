from rest_framework import serializers
from .models import Subdomain

class SubdomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdomain
        fields = '__all__'
