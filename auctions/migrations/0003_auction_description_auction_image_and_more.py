# Generated by Django 4.0 on 2022-01-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_category_comment_bid_auction_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
        migrations.RemoveField(
            model_name='auction',
            name='categories',
        ),
        migrations.AddField(
            model_name='auction',
            name='categories',
            field=models.CharField(choices=[('MOT', 'Motors'), ('FAS', 'Fashion'), ('ELE', 'Electronics'), ('ART', 'Collectibles & Art'), ('HOM', 'Home & Garden'), ('SPO', 'Sporting Goods'), ('TOY', 'Toys'), ('BUS', 'Business & Industrial'), ('MUS', 'Music'), ('NON', 'NONE')], default='NON', max_length=3),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
