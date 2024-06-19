import json
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Brand, Product
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class RetrieveProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer(many=True)
    total_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "category",
            "image",
            "file",
            "price",
            "stock",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.price * obj.stock

    def get_image(self, obj):
        if settings.DEBUG:
            request = self.context.get("request")
            if obj.image and request:
                return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def get_file(self, obj):
        if settings.DEBUG:
            request = self.context.get("request")
            if obj.file and request:
                return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "category",
            "image",
            "file",
            "price",
            "stock",
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

