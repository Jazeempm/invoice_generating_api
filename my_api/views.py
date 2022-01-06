from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView
from django.contrib.auth import get_user_model
from .models import ItemModel,InvoiceModel
from .serializers import ItemSerializer
from .serializers import UserSerializer,InvoiceSerializer
import pdfkit
from django.template.loader import get_template
from io import BytesIO
from django.core.files import File
from rest_framework import status
from django.conf import settings

# Create your views here.
class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'Message': 'You have successfully register'}, status=status.HTTP_201_CREATED, headers=headers)


class ProductListView(ListCreateAPIView):
    model = ItemModel
    permission_classes = [
        permissions.IsAuthenticated  # Or
    ]
    serializer_class = ItemSerializer

    def get_queryset(self):
        return ItemModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemView(RetrieveUpdateDestroyAPIView):
    model = ItemModel
    serializer_class = ItemSerializer
    permission_classes = [
        permissions.IsAuthenticated  # Or
    ]

    def get_queryset(self):
        return ItemModel.objects.filter(user=self.request.user)


class GenerateInvoice(APIView):
    def post(self, request):
        item_lst = request.data['items']
        discount = request.data['discount']
        subtotal_without_tax = 0
        subtotal_with_tax = 0
        response_list = []
        for l_item in item_lst:
            err=None
            try:
                itm = ItemModel.objects.get(id=l_item["item_id"])
                if l_item["quantity"] > itm.quantity:
                    err = f"product {itm.id}.{itm.name} has only {itm.quantity} items left"
            except Exception as arg:
                err=str(arg)

            if err:
                return Response(
                                 {
                                      "Error_list": err
                                 },
                                 status=status.HTTP_400_BAD_REQUEST
                            )
            item_total = itm.unit_price * l_item["quantity"]

            tax = item_total* itm.tax / 100
            item_total_wtax = item_total + tax

            subtotal_without_tax += item_total
            subtotal_with_tax += item_total_wtax

            dic = {"id": itm.id,
                   "name": itm.name,
                   "unit_price": itm.unit_price,
                   "quantity":l_item["quantity"],
                   "tax": itm.tax,
                   "item_total": item_total
                   }
            response_list.append(dic)

        final_amount = subtotal_with_tax - (subtotal_with_tax * discount / 100)
        final_response = {"item_list": response_list,
                          "subtotal_without_tax": subtotal_without_tax,
                          "subtotal_with_tax": subtotal_with_tax,
                          "final_amount": final_amount,
                          "discount":discount,
                          }
        file=generate_pdf(invoice=final_response)
        serializer=InvoiceSerializer(file,many=False,context={'request': request})
        return Response(serializer.data)


def generate_pdf(invoice):

    path_wkhtmltopdf = settings.PATH_WKHTMLTOPDF
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    template_name = 'pdf.html'
    template = get_template(template_name)
    html = template.render({'invoice': invoice})
    pdf = pdfkit.from_string(html, False, options={}, configuration=config)
    receipt_file = File(BytesIO(pdf),"invoice.pdf")
    file=InvoiceModel(invoice=receipt_file)
    file.save()
    file=InvoiceModel.objects.get(id=file.id)
    return file
