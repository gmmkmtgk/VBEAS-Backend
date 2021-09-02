from api.models import Book, BookSeller, Recommend
from django.contrib import admin

from import_export import resources, fields
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'title', 'seller', 'author', 'ISBN', 'subject', 'year_of_publication',
                'price', 'discount', 'expected_price', 'link', 'medium')

class BookSellerResource(resources.ModelResource):
    class Meta:
        model = BookSeller
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'name', 'contact_no', 'email')

class BookSellerAdmin(ImportExportActionModelAdmin):
    resource_class = BookSellerResource
    pass

class BookAdmin(ImportExportActionModelAdmin):
    resource_class = BookResource
    pass


admin.site.register(BookSeller, BookSellerAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Recommend)




