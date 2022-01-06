from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ItemModel,InvoiceModel
from django.conf import settings
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        return user

    class Meta:
        model = UserModel
        fields = ( "id", "username", "password", "email")

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemModel
        fields = ("name", "quantity", "unit_price", "tax")

class InvoiceSerializer(serializers.ModelSerializer):

    invoice = serializers.SerializerMethodField()
    class Meta:
        model = InvoiceModel
        fields = ("id","invoice","date_created")

    def get_invoice(self, invoice):
        request = self.context.get("request","n")
        invoice_url = invoice.invoice
        invoice_url.name=settings.MEDIA_URL+invoice_url.name
        # settings.MEDIA_URL +

        return request.build_absolute_uri(invoice_url)