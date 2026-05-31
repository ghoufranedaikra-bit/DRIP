from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    sizes_list = serializers.SerializerMethodField()
    colors_list = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_sizes_list(self, obj):
        return [s.strip() for s in obj.sizes.split(',') if s.strip()]

    def get_colors_list(self, obj):
        return [c.strip() for c in obj.colors.split(',') if c.strip()]