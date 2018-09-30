

from rest_framework import serializers

from rango.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
