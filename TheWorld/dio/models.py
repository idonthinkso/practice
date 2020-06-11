# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TBookDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    bookname = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    publisher = models.CharField(max_length=50, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    printing_time = models.DateField(blank=True, null=True)
    impression = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    word_number = models.IntegerField(blank=True, null=True)
    page_number = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=50, blank=True, null=True)
    paper = models.CharField(max_length=50, blank=True, null=True)
    package = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    book_type = models.ForeignKey('TBookType', models.DO_NOTHING, db_column='book_type', blank=True, null=True)
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    comment = models.IntegerField(blank=True, null=True)
    picture = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 't_book_details'


class TBookType(models.Model):
    id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=50, blank=True, null=True)
    super = models.ForeignKey('self', models.DO_NOTHING, db_column='super', blank=True, null=True)

    class Meta:
        db_table = 't_book_type'


class TCart(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(TBookDetails, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 't_cart'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    create_time = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 't_order'


class TOrderDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(TBookDetails, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 't_order_details'


class TUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255, blank=True, null=True)
    salt = models.CharField(max_length=20)

    class Meta:
        db_table = 't_user'


class TUserAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(TUser, models.DO_NOTHING, blank=True, null=True)
    detail = models.CharField(max_length=300, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fixphone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 't_user_address'
