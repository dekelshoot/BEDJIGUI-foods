from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView
from project.forms import UpdateUser, ReservationForm, LoginForm, RegisterForm,MenuForm
from django.contrib import messages
from django.db.models import Sum
from project.models import User, Reservation,Menu,Commande,Cart_List


class Profile(LoginRequiredMixin, UpdateView):
    """admin user view and update profile"""
    form_class = UpdateUser
    model = User
    template_name = "super/profile.html"
    login_url = "/login/"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, ("your profile has been updated successfully"))
        return redirect('/profile')




class Register(View):
    form_class = RegisterForm
    template_name = "auth/register.html"

    
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            messages.success(request,
                             "your account has been created successfully")
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect('/dashboard')
                    else:
                        return redirect('/')
                    # if user.user_type == 'guest':
                    #     return redirect('/resturant')
                    # elif user.user_type == 'admin':
                    #     return redirect('/dashboard')
        return render(request, self.template_name, {'form': form})


class Login(View):
    """ Login View."""
    form_class = LoginForm
    template_name = "auth/login.html"

    def get(self, request):
        logout(request)
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            messages.success(request, "you have logged in successfully ")
            if user is not None:
                print("staff: ",user)
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect('/dashboard')
                    else:
                        return redirect('/')
            else:
                error = "username or password is incorrect"
        return render(
            request, self.template_name, {'form': form, 'error': error})


class LogoutView(View):
    """ Custom Logout View."""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


@login_required(login_url="/login/")
def dashboard(request):
    """Admin dashboard view."""
    reservations = Reservation.objects.all()
    users = User.objects.all()
    menu = Menu.objects.all()
    commande = Commande.objects.all()
    pending = Reservation.objects.filter(status="pending")
    confirmed = Reservation.objects.filter(status="confirmed")
    return render(request, "super/dashboard.html",
                  {'users': users,
                   'menu':menu,
                   'commande':commande,
                   'reservations': reservations,
                   'pending': pending, 'confirmed': confirmed})


class AddReservation(LoginRequiredMixin, CreateView):
    """Admin user add new reservation."""
    template_name = "super/new_reserve.html"
    form_class = ReservationForm
    login_url = '/login/'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.save()
        # send a flash message to the user
        messages.success(
            self.request,
            "you have successfully added a new table reservation ")
        # redirect the user back to his/her dashboard
        return redirect("/dashboard")
    
class AddMenu(LoginRequiredMixin, CreateView):
    """Admin user add new reservation."""
    template_name = "super/new_menu.html"
    form_class = MenuForm
    login_url = '/login/'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.save()
        # send a flash message to the user
        messages.success(
            self.request,
            "you have successfully added a new menu ")
        # redirect the user back to his/her dashboard
        return redirect("/dashboard")


class UpdateReservation(LoginRequiredMixin, UpdateView):
    """Admin user updates all the reservation."""
    form_class = ReservationForm
    template_name = "super/update_reserve.html"
    model = Reservation

    def get_object(self, *args, **kwargs):
        obj = get_object_or_404(Reservation, pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "you have successfully updated the reservation")
        return redirect('/dashboard')
    
class UpdateMenu(LoginRequiredMixin, UpdateView):
    """Admin user updates all the reservation."""
    form_class = MenuForm
    template_name = "super/update_menu.html"
    model = Menu

    def get_object(self, *args, **kwargs):
        obj = get_object_or_404(Menu, pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "you have successfully updated the Menu")
        return redirect('/dashboard')


@login_required(login_url="/login/")
def view_reservations(request):
    """Admin user view all the reservations."""
    reservations = Reservation.objects.all()
    return render(request,
                  "super/view_reserve.html",
                  {'reservations': reservations})

@login_required(login_url="/login/")
def view_menu(request):
    """Admin user view all the menu."""
    menu = Menu.objects.all()
    return render(request,
                  "super/view_menu.html",
                  {'menu': menu})

@login_required(login_url="/login/")
def view_commande(request):
    """Admin user view all the commande."""
    
    commandes = {}
    i=1
    for commande in Commande.objects.all():
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
    return render(request,
                  "super/view_commande.html",
                  {'commandes': commandes})

@login_required(login_url="/login/")
def removeCommande_view(request,commande_id):
	item_toremove = Commande.objects.get(pk=commande_id)
	item_toremove.delete()
	messages.info(request,"Cette commande a été supprimé .")
	return HttpResponseRedirect(reverse("view_commandes"))
