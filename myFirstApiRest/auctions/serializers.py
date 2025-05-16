from rest_framework import serializers
from .models import Category, Auction, Bid, Rating, Comment
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from datetime import timedelta

class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    auctioneer = serializers.PrimaryKeyRelatedField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    last_call = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate_closing_date(self, value):
        # Ensure closing date is greater than now
        if value <= timezone.now():
            raise serializers.ValidationError("Closing date must be greater than now.")
        
        # Ensure closing date is at least 15 days after now
        if value - timezone.now() < timedelta(days=15):
            raise serializers.ValidationError("Closing date must be at least 15 days after creation date.")

        return value
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 2)
        return 1.0
    
    def get_last_call(self, obj):
        #return not obj.bids.all().exists()
        tr = obj.closing_date - timezone.now()
        return tr < timedelta(hours=1) and not obj.bids.all().exists()



class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def validate_closing_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(f"Closing date must be greater than now.")

        return value
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 2)
        return 1.0
    
class BidListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    bidder = serializers.StringRelatedField(read_only=True)
    # auction = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'price', 'creation_date', 'bidder']
        extra_kwargs = {'auction': {'required': False}}

class BidDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    bidder = serializers.StringRelatedField(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'price', 'creation_date', 'bidder']

class RatingListCreateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'value', 'auction', 'user']
        extra_kwargs = {'auction': {'required': False}}

    def validate_value(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("El valor debe estar entre 1 y 5.")
        return value

class RatingDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'value', 'user', 'auction']

class CommentListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    edit_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'title', 'text', 'creation_date', 'edit_date', 'auction', 'user']
        extra_kwargs = {'auction': {'required': False}}


class CommentDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    edit_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    auction = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'title', 'text', 'creation_date', 'edit_date', 'user', 'auction']