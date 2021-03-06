from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api.views import *
from api.views.order import OrderViewSet
from api.views.reason import ReasonViewSet

router = DefaultRouter()
# Define url in here
router.register(r'user', UserViewSet, base_name="user")
router.register(r'action', ActionViewSet, base_name="action")
router.register(r'type', TypeViewSet, base_name="type")
router.register(r'product', ProductViewSet, base_name="product")
router.register(r'cart', CartViewSet, base_name="cart")
router.register(r'history', HistoryViewSet, base_name="history")
router.register(r'order', OrderViewSet, base_name="order")
router.register(r'comment', CommentViewSet, base_name="comment")
router.register(r'reply', ReplyViewSet, base_name="reply")
router.register(r'reason', ReasonViewSet, base_name="reason")
router.register(r'waiting_list', WaitinglistViewSet, base_name="waiting_list")
urlpatterns = [
    url(r'^', include(router.urls))
]
