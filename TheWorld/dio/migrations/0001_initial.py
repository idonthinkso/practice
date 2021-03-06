# Generated by Django 2.0.6 on 2019-12-19 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TBookDetails',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('bookname', models.CharField(blank=True, max_length=50, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('author', models.CharField(blank=True, max_length=50, null=True)),
                ('publisher', models.CharField(blank=True, max_length=50, null=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('edition', models.IntegerField(blank=True, null=True)),
                ('printing_time', models.DateField(blank=True, null=True)),
                ('impression', models.IntegerField(blank=True, null=True)),
                ('isbn', models.CharField(blank=True, db_column='ISBN', max_length=50, null=True)),
                ('word_number', models.IntegerField(blank=True, null=True)),
                ('page_number', models.IntegerField(blank=True, null=True)),
                ('format', models.CharField(blank=True, max_length=50, null=True)),
                ('paper', models.CharField(blank=True, max_length=50, null=True)),
                ('package', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('comment', models.IntegerField(blank=True, null=True)),
                ('picture', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 't_book_details',
            },
        ),
        migrations.CreateModel(
            name='TBookType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(blank=True, max_length=50, null=True)),
                ('super', models.ForeignKey(blank=True, db_column='super', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TBookType')),
            ],
            options={
                'db_table': 't_book_type',
            },
        ),
        migrations.CreateModel(
            name='TCart',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TBookDetails')),
            ],
            options={
                'db_table': 't_cart',
            },
        ),
        migrations.CreateModel(
            name='TOrder',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('create_time', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_order',
            },
        ),
        migrations.CreateModel(
            name='TOrderDetails',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TBookDetails')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TOrder')),
            ],
            options={
                'db_table': 't_order_details',
            },
        ),
        migrations.CreateModel(
            name='TUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('salt', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 't_user',
            },
        ),
        migrations.CreateModel(
            name='TUserAddress',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('detail', models.CharField(blank=True, max_length=300, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('fixphone', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TUser')),
            ],
            options={
                'db_table': 't_user_address',
            },
        ),
        migrations.AddField(
            model_name='torder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TUser'),
        ),
        migrations.AddField(
            model_name='tcart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TUser'),
        ),
        migrations.AddField(
            model_name='tbookdetails',
            name='book_type',
            field=models.ForeignKey(blank=True, db_column='book_type', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dio.TBookType'),
        ),
    ]
