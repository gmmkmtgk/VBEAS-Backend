import os, re
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
# Rest Frameworks
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

# Models
from api.models import Book, BookSeller

# Create your views here.
def home_index(request):
    return redirect('api/')

def index(request):
    return HttpResponse("Backend Connected")

@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def sellerApi(request):
    if request.method == 'GET':
        seller = BookSeller.objects.all()
        return Response({"data": seller.values()}, status = status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def bookApi(request, ):
    if request.method == "GET":
        books = Book.objects.all()
        return Response({
            'data': books.values()
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getBook(request, book_id):
    try:
        book = Book.objects.filter(id=book_id)
        if len(book.values()) == 0:
            return Response({
                "error":"404 NOT Found",
                'message':f"Book Id does not exit ${book_id}"
            }, status = status.HTTP_404_NOT_FOUND)
    except:
        return Response({
            'error':"404 NOT FOUND",
            'message': "Book Id "+str(book_id) + " does not exist"
        }, status = status.HTTP_404_NOT_FOUND)
    #dat = serializers.serialize('json', book)
    return Response({'data': list(book.values())})

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def getAllSellerBooks(request, sellerId):
    try:
        books = Book.objects.filter(seller__id = sellerId)
        seller = BookSeller.objects.filter(id = sellerId).values()[0]['name']
        return Response({"seller": seller, "data":books.values()})
    except Exception as e:
        return Response({
            "message": e
        })