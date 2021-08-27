from api.views.auth import authenticate
from api.views.index import index, sellerApi, bookApi, getAllSellerBooks, getBook
from django.urls import path

urlpatterns = [
    path('', index, name = 'index'),
    path('auth/authenticate/', authenticate, name = 'auth-authenticate'),
    path('seller/', sellerApi, name='sellerApi'),#All Related Work with Seller from this API
    path('book/', bookApi, name="bookApi"), #All Related Work with this Book from this API
    path('book/<int:book_id>/', getBook, name='getBook'),
    path('seller/filer/<int:sellerId>/', getAllSellerBooks, name = 'getAllSellerBooks'),
]