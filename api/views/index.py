import os, re, random
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
# Rest Frameworks
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

# Models
from api.models import Book, BookSeller, Recommend

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


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def searchBooks(request):
    data = request.data
    # value = []
    search_types = ['search', 'author', 'subject', 'title']
    for fields in data:
        if fields['field'] not in search_types:
            return Response({
                'status' : "failed",
                'message' :'Filed not in types',
            }, status = status.HTTP_200_OK)
        else :
            try:
                query = fields['value']
                book_data = Book.objects.filter(author__icontains = query) | Book.objects.filter(subject__icontains = query) | Book.objects.filter(title__icontains = query)

                # Brute Force Filter to check the above django Template Filters
                # books = Book.objects.all()
                # print(book_data.values()[0:2])
                # res = list(books.values())
                # for book in res:
                #     if query in book['title'].lower():
                #         value.append(book)
                #     elif query in book['subject'].lower():
                #         value.append(book)
                #     elif query in book['author'].lower():
                #         value.append(book)


            except Exception as e:
                return Response({
                    "message": e
                });
    res = list(book_data.values())
    random.shuffle(res)
    return Response({
                'status':'success',
                'data' : res,
                # 'secondary': value
            }, status = status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def recommendApi(request):    
    if request.method == 'POST':
        data = request.data
        try:
            book_id = data['book_id']
            book = Book.objects.get(id=book_id)
        except:
            return Response({
                'message':'Book Doesnt Exist'
            }, status=status.HTTP_400_BAD_REQUEST)

        buyer_email = request.data['email']
        username, domain = buyer_email.split('@')
        if domain != "lnmiit.ac.in":
            return Response(
                {"error": "Can only be accessed by LNMIIT Mail"}, status=status.HTTP_400_BAD_REQUEST
            )

        buyer_name = request.data['name']
        if len(buyer_name) == 0:
            return Response({
                'error':"Something went Wrong."
            }, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            recommend = Recommend()
            recommend.buyer = buyer_name
            recommend.email = buyer_email
            recommend.book = book
            recommend.title = book.title
            recommend.author = book.author
            recommend.price = book.expected_price
            recommend.medium = book.medium
            recommend.seller_name = book.seller.name
            recommend.seller = book.seller
            recommend.recommended_to_library = True
            recommend.save()
            return Response({
                'status': 'success',
                'message':"Book Recommended",
                'recommendation_id':recommend.id
            }, status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'message': e
            })

@api_view(['POST', 'GET'])
@csrf_exempt
def cartApi(request):
    if request.method == 'POST':
        data = request.data
        buyer_email = request.data['email']
        username, domain = buyer_email.split('@')
        if domain != "lnmiit.ac.in":
            return Response(
                {"error": "Can only be accessed by LNMIIT Mail"}, status=status.HTTP_400_BAD_REQUEST
            )
        recommend = Recommend.objects.filter(email = buyer_email)
        return Response({
            'status':"Success",
            'data':recommend.values(),
        }, status = status.HTTP_200_OK)
