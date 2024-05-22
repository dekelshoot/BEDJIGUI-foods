from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView,View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from project.models import User, Reservation,Menu,Cart_List,Commande
from jembe.forms import ReservationForm, LoginForm, RegisterForm
from jembe.forms import ReservationForm, ContactForm
from django.db.models import Sum

@login_required(login_url="/login/")
def home(request):
    context = {
		"menu" : Menu.objects.all(),
	}
    return render(request, "index.html",context)

@login_required(login_url="/login/")
def about(request):
    return render(request, "about.html")

# class Profile(LoginRequiredMixin, UpdateView):
#     """admin user view and update profile"""
#     form_class = UpdateUser
#     model = User
#     template_name = "super/profile.html"
#     login_url = "/login/"

#     def get_object(self, queryset=None):
#         return self.request.user

#     def form_valid(self, form):
#         form.save()
#         messages.success(
#             self.request, ("your profile has been updated successfully"))
#         return redirect('/profile')





class NewReservation(CreateView):
    template_name = "reservation.html"
    form_class = ReservationForm
    model = Reservation
    # print(User.)
    def form_valid(self, form):
        new = form.save(commit=False)
        new.save()
        # sends a flash message to the user
        messages.success(
            self.request,
            "you have successfully booked a new" +
            " table confirm your by paying for the table ")
        # redirect the user back to his/her dashboard
        return redirect("/payments")


class Contact(CreateView):
    template_name = "contact.html"
    form_class = ContactForm

    def form_valid(self, form):
        new = form.save(commit=False)
        new.save()
        # send a flash message to the user
        messages.success(
            self.request,
            "your message was sent successfully")
        # redirect the user back to contact page
        return redirect("/contact")


@login_required(login_url="/login/")
def payment(request):
    return render(request, "payment.html")

@login_required(login_url="/login/")
def cart_view(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        user = request.user
        p = Menu.objects.get(pk=item_id)
        print(item_id)
        total_price = p.prix 
        new_cart = Cart_List(user_id=user, menu_id=Menu.objects.get(pk = item_id),  calculated_price=total_price)

		# add item to cart
        new_cart.save()

		# return HttpResponseRedirect(reverse("cart"))
        messages.success(request, "Menu ajouté dans à la commande !")
        return HttpResponseRedirect(reverse("home"))
        # return render(request, "orders/index.html", {"message": "Meal added to cart!"})
    else:

        commandes = {}
        i=1
        for commande in Commande.objects.filter(user_id=request.user.id):
            commandes[i] ={}
            commandes[i]["commande"] =commande
            commandes[i]["carts"] =[]
            commandes[i]["date"] =commande.created_at
            commandes[i]["id"] =commande.id
            carts= Cart_List.objects.filter(commande=commande)
            commandes[i]["total"] =carts.aggregate(Sum('calculated_price'))['calculated_price__sum']
            for cart in carts:
                 commandes[i]["carts"].append(cart)
            i=i+1
        print(commandes.items())
        try:
            cart = Cart_List.objects.filter(user_id=request.user, is_current=True)
        except Cart_List.DoesNotExist:
            raise Http404("Cart does not exist")
		
        total_price = cart.aggregate(Sum('calculated_price'))['calculated_price__sum']

        cart_ordered = Cart_List.objects.filter(user_id=request.user, is_current=False)

        context = {
        "carts":carts,
        "commandes":commandes,
        "cart_items" : cart,
        "total_price": total_price,
        "cart_items_ordered" : cart_ordered,
        }

        return render(request, "cart.html", context)
    
@login_required(login_url="/login/")
def removefromcart_view(request, cart_id):
	# view topping from cart

	item_toremove = Cart_List.objects.get(pk=cart_id)
	item_toremove.delete()
	messages.info(request,"Ce Menu a été supprimé de votre Commande.")
	return HttpResponseRedirect(reverse("cart"))

@login_required(login_url="/login/")
def order_view(request):
	# place an order

	if request.method == "POST":
		user = request.user
		items = request.POST.getlist("cart_id")
		print(items)

		new_order = Commande(user_id=user)

		new_order.save()

		for item in items:
			new_order.cart_id.add(item)

		# set current attribute to False 
		cart = Cart_List.objects.filter(user_id=request.user)
		for item in cart:
			item.is_current=False
			item.save()
	messages.success(request,"Merci d'avoir fait vos achats chez nous, votre commande a été passée.")
	return HttpResponseRedirect(reverse("home"))

@login_required(login_url="/login/")
def removeCommande_view(request,commande_id):
	item_toremove = Commande.objects.get(pk=commande_id)
	item_toremove.delete()
	messages.info(request,"Cette commande a été supprimé .")
	return HttpResponseRedirect(reverse("cart"))
