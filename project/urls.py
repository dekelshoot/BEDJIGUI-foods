from django.conf.urls import url

from project import views

urlpatterns = [
    url(r'^profile/$', views.Profile.as_view(), name="profile"),
    url(r'^add-reservation/$', views.AddReservation.as_view(), name="add"),
    url(r'^add-menu/$', views.AddMenu.as_view(), name="addmenu"),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^register/$', views.Register.as_view(), name="register"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^view-reservations/$',
        views.view_reservations, name="view_reservations"),
    url(r'^view-commandes/$',
        views.view_commande, name="view_commandes"),
    url(r'^view-menu/$',views.view_menu, name="view_menu"),
    url(r'^update-reservation/(?P<pk>\d+)/$',
        views.UpdateReservation.as_view(), name="update_reservation"),
    url(r'^update-menu/(?P<pk>\d+)/$',
        views.UpdateMenu.as_view(), name="update_menu"),
    url(r'^remove-commande/(?P<commande_id>\d+)/$', views.removeCommande_view, name="remove_commande"),
]
