from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name="auctions", on_delete=models.CASCADE
    )
    thumbnail = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name="bids", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(CustomUser, related_name='bids', on_delete=models.CASCADE)

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return f"Bid {self.id} for Auction {self.auction.title}"

class Rating(models.Model):
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1,
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        unique_together = ('user', 'auction')  # Un usuario solo puede valorar una vez cada subasta
        ordering = ('id',)

    def __str__(self):
        return f'Rating {self.value} by {self.user} for {self.auction}'
    
class Comment(models.Model):
    title = models.TextField()
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        unique_together = ('user', 'auction')  # Un usuario solo puede comentar una vez en cada subasta
        ordering = ('id',)

    def __str__(self):
        return f'Comment by {self.user} for {self.auction}'