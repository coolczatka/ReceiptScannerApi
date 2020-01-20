from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import (permission_classes,action)
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)
from .permissions import (AllowOwner_p,AllowOwner_r,UserPermissions)
from .services.ReceiptImageService import ReceiptImageService
import datetime
import regex

from django.http import HttpResponseForbidden
# Create your views here.


@permission_classes([UserPermissions])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes([AllowOwner_r, IsAuthenticated])
class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user).order_by("-date")

    def create(self, request, *args, **kwargs):
        serializer = ReceiptSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)



@permission_classes([IsAuthenticated])
class PictureViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Picture.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if(not serializer.is_valid()):
            print(serializer.errors)
        serializer.save()
        name = serializer.data['picture'].split('/')[1]
        path = settings.MEDIA_ROOT+'/'+name
        ris = ReceiptImageService(path)
        ris.findCorners()
        ris.getText()
        data = ris.extractData()
        shops = Shop.objects.all()
        flag = False
        for shop in shops:
            r = regex.compile('(' + shop.name + '){e<=1}', regex.IGNORECASE)
            if r.search(data['shop']):
                data['shop']=shop.name
                flag = True
                break
        if not flag:
            data['shop']= ''
        return Response({'shop':data['shop'],'date':data['date'],'products':data['products']})
        # return Response({'shop':'biedronka','date':'2019-08-09','products':[{'name':'n1','amount':'1.0','price':'19.99'},{'name':'produkt','amount':'2.0','price':'24.99'}]})

@permission_classes([AllowOwner_p, IsAuthenticated])
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(receipt=Receipt.objects.get(pk=self.kwargs['receipt_id']))

    def create(self, request, *args, **kwargs):
        try:
            request.data['amount'] = round(request.data['amount'],2)
            request.data['price'] = round(request.data['price'],2)
            serializer = ProductSerializer(data=request.data)
            receipt = Receipt.objects.get(pk=self.kwargs['receipt_id'])
            serializer.is_valid(raise_exception=True)
            serializer.save(receipt=receipt)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,status=201,headers=headers)
        except Exception as e:
            print("blad: {0}".format(e)+"\n"+str(serializer.data))

@permission_classes([AllowAny]) #tymczasowo
class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

@api_view()
@permission_classes([IsAuthenticated])
def sumOfMounth(request):
    data=[]
    months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
    for i in range(1,13):
        receipts = Receipt.objects.filter(user=request.user,date__year=request.GET['year'],date__month=i)
        sum = 0
        for receipt in receipts:
            products = Product.objects.filter(receipt=receipt)
            for product in products:
                sum += product.price*product.amount
        data.append({'month':months[i-1],'sum':sum})
    return Response(data,200)

@api_view()
@permission_classes([IsAuthenticated])
def pieData(request):
    data = Shop.objects.raw("Select * from inz_shop group by category;")
    categories = []
    dic= {}
    for d in data:
        categories.append(d.category)
        dic[d.category]=0
    dic['nieznany']=0
    receipts = Receipt.objects.filter(user=request.user, date__year=request.GET['year'])
    for receipt in receipts:
        products = Product.objects.filter(receipt=receipt)
        try:
            shop = Shop.objects.get(name__iexact=receipt.shop)
            category = shop.category
        except Shop.DoesNotExist:
            shop=None
            category = 'nieznany'
        for product in products:
            dic[category] += product.price * product.amount
    total = sum(dic.values())
    result = []
    for key in dic:
        try:
            result.append({'category':key,'percent':round(dic[key]/total*100,2)})
        except ZeroDivisionError:
            dic[key] = 'Nan'
    return Response(result,200)

