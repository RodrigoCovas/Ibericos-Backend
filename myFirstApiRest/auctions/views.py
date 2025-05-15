from rest_framework import generics
from .models import Category, Auction, Bid, Rating, Comment
from .serializers import (
    CategoryListCreateSerializer,
    CategoryDetailSerializer,
    AuctionListCreateSerializer,
    AuctionDetailSerializer,
    BidListCreateSerializer,
    BidDetailSerializer,
    RatingListCreateSerializer, 
    RatingDetailSerializer,
    CommentListCreateSerializer,
    CommentDetailSerializer,
)
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from .permissions import IsOwnerOrAdmin


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer


class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class AuctionListCreate(generics.ListCreateAPIView):
    serializer_class = AuctionListCreateSerializer

    def get_queryset(self): 
        queryset = Auction.objects.all() 
        params = self.request.query_params 
        search = params.get('search', None) 
        if search: 
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search)) 
        return queryset 

    def perform_create(self, serializer):
        # Automatically set auctioneer as the logged-in user
        serializer.save(auctioneer=self.request.user)

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]   
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)

class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidListCreateSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return Bid.objects.filter(auction_id=auction_id).order_by('-price')

    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Bid.objects.all()
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return super().get_queryset().filter(auction_id=auction_id)
    
class UserBidListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Obtener las pujas del usuario autenticado
        user_bids = Bid.objects.filter(bidder=request.user)
        serializer = BidListCreateSerializer(user_bids, many=True)
        return Response(serializer.data)
    
class RatingListCreateView(generics.ListCreateAPIView):
    serializer_class = RatingListCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Rating.objects.filter(auction_id=auction_id)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        auction = Auction.objects.get(pk=auction_id)
        serializer.save(user=self.request.user, auction=auction)

class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Rating.objects.filter(auction_id=auction_id, user=self.request.user)

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        if not obj:
            return Response({
                "value": None
            })
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_object(self):
        obj = self.get_queryset().first()
        if not obj:
            raise NotFound("No has valorado esta subasta.")
        return obj
    
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentListCreateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Comment.objects.filter(auction_id=auction_id)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        auction = Auction.objects.get(pk=auction_id)
        serializer.save(user=self.request.user, auction=auction)

class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Comment.objects.filter(auction_id=auction_id, user=self.request.user)

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        if not obj:
            return Response({
                "value": None
            })
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_object(self):
        obj = self.get_queryset().first()
        if not obj:
            raise NotFound("No has comentado en esta subasta.")
        return obj