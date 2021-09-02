from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class BookSeller(models.Model):
    """
    The Details of a Book Seller
    """
    name = models.CharField(max_length=200, blank=True, null = True)
    contact_no = models.CharField(max_length = 10, blank=True, null=True, unique=True)
    email=models.EmailField(max_length=200,null=True)
    logo = models.ImageField(
        upload_to='book_sellers_logo', null=True, blank=True)
    def __str__(self):
        return f"{self.name}"
    
class Book(models.Model):
    """
    Model to save a Publisher 's Book
    Can be changed or updated
    """
    MEDIUM_CHOICES = (
        ("PAPERBACK", "paperback"),
        ("ELECTRONIC", 'electronic'), 
    )
    title = models.CharField(max_length=600, blank=True, null=True)
    seller = models.ForeignKey(BookSeller, on_delete=models.CASCADE, null = True, blank=True)
    author = models.CharField(max_length=800, null=True, blank=True)
    ISBN = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    year_of_publication = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    discount = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    expected_price = models.FloatField(
        validators=[MinValueValidator(0)], blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    medium = models.CharField(max_length=200, choices=MEDIUM_CHOICES, default= "PAPERBACK")
    image = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    
    # For banning/unbanning products.
    visible = models.BooleanField(default=True)
    # For expiring products after given expiry period.
    expired = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id":self.id,
            "pk" : self.pk,
            "title": self.title,
            "seller":self.seller.name,
            "author":self.author,
            "ISBN":self.ISBN,
            "subject":self.subject,
            "year_of_publication":self.year_of_publication,
            "price":self.price,
            "discount":self.discount,
            "expected_price":self.expected_price,
            "link":self.link,
            "medium":self.medium,
            "image":self.image,
            "thumbnail":self.thumbnail,
            "created_at":self.created_at,
        }

    def __str__(self):
        return f"{self.title}-{self.medium}"
    
    def save(self, *args, **kwargs):
        self.expected_price = round(self.price * \
            (1-((self.discount)/100)))
        if self.pk is None:
            self.image = "http://covers.openlibrary.org/b/isbn/"+str(self.ISBN)+"-M.jpg"
            self.thumbnail = "http://covers.openlibrary.org/b/isbn/"+str(self.ISBN)+"-S.jpg"
        super().save(*args, **kwargs)


class Recommend(models.Model):
    """
    Model to save a user's recommendation. 
    Users can add/delete recommendation from their cart.
    """
    MEDIUM_CHOICES = (
        ("PAPERBACK", "paperback"),
        ("ELECTRONIC", 'electronic'), 
    )
    book = models.ForeignKey(
        Book,
        related_name="recommend",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=600, blank=True, null=True)
    seller_name = models.CharField(max_length=400, blank=True, null=True)
    author = models.CharField(max_length=800, null=True, blank=True)
    price = models.CharField(max_length=800, null=True, blank=True)
    medium = models.CharField(max_length=200, choices=MEDIUM_CHOICES, default= "PAPERBACK")
    seller = models.ForeignKey(
        BookSeller,
        related_name="recommend",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    buyer = models.CharField(max_length=200, blank=True, null = True)
    email=models.EmailField(max_length=200,null=True)
    recommended_to_library = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.buyer
    