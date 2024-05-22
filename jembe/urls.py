from django.conf.urls import url
from jembe import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^about/$', views.about, name="about"),
    url(r'^reservation/$', views.NewReservation.as_view(), name="reservation"),
    url(r'^contact/$', views.Contact.as_view(), name="contact"),
    url(r'^payments/$', views.payment, name="payment"),
    url(r'^cart/$', views.cart_view, name="cart"),
    url(r'^removefromcart/(?P<cart_id>\d+)/$', views.removefromcart_view, name="removefromcart"),
    url(r'^removecommande/(?P<commande_id>\d+)/$', views.removeCommande_view, name="removecommande"),
    url(r'^order/$', views.order_view, name="order"),
]