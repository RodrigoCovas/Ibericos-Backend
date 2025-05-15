from django.urls import path
from .views import (
    CategoryListCreate,
    CategoryRetrieveUpdateDestroy,
    AuctionListCreate,
    AuctionRetrieveUpdateDestroy,
    BidListCreate,
    BidRetrieveUpdateDestroy,
    UserAuctionListView,
    UserBidListView,
    RatingListCreateView, 
    RatingRetrieveUpdateDestroy,
    CommentListCreateView,
    CommentRetrieveUpdateDestroy,
)

app_name = "auctions"
urlpatterns = [
    path("categories/", CategoryListCreate.as_view(), name="category-list-create"),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdateDestroy.as_view(),
        name="category-detail",
    ),
    path("", AuctionListCreate.as_view(), name="auction-list-create"),
    path("<int:pk>/", AuctionRetrieveUpdateDestroy.as_view(), name="auction-detail"),
    path("<int:auction_id>/bid/", BidListCreate.as_view(), name='bid-list-create'),
    path("<int:auction_id>/bid/<int:pk>/", BidRetrieveUpdateDestroy.as_view(), name='bid-retrieve-update-destroy'),
    path('user_auctions/', UserAuctionListView.as_view(), name='action-from-users'),
    path('user_bids/', UserBidListView.as_view(), name='bid-from-users'),
    path('<int:auction_id>/ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('<int:auction_id>/my_rating/', RatingRetrieveUpdateDestroy.as_view(), name='my-rating-auction'),
    path('<int:auction_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:auction_id>/my_comment/', CommentRetrieveUpdateDestroy.as_view(), name='my-comment-auction'),
]

