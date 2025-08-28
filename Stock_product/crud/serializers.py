from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, required=False)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions', [])
        stock = Stock.objects.create(**validated_data)
        for position in positions_data:
            StockProduct.objects.create(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions', None)
        if positions_data is not None:
            instance = super().update(instance, validated_data)
        for position in positions_data:
            StockProduct.objects.update_or_create(
                stock=instance,
                product=position['product'],
                defaults={
                    'quantity': position['quantity'],
                    'price': position['price']
                }
            )

        existing_product_ids = [pos_data['product'].id for pos_data in
                                positions_data]
        instance.positions.exclude(product_id__in=existing_product_ids).delete()

        return instance
