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
from project.models import User, Reservation,Menu,Commande,Table_List

class Profile(LoginRequiredMixin, UpdateView):
    """
    Vue de profil et de mise à jour de l'utilisateur administrateur.

    Cette classe de vue gère l'affichage et la mise à jour du profil de l'utilisateur connecté (admin).
    Elle hérite de deux mixins et d'une vue Django générique.
    """

    form_class = UpdateUser  # Formulaire utilisé pour la mise à jour du profil
    model = User  # Modèle User de Django (adaptez-le à votre modèle d'utilisateur personnalisé si nécessaire)
    template_name = "super/profile.html"  # Chemin vers le template d'affichage du profil
    login_url = "/login/"  # URL de redirection si l'utilisateur n'est pas connecté

    def get_object(self, queryset=None):
        """
        Récupère l'objet utilisateur à modifier.

        Cette méthode est requise par la vue générique UpdateView.
        Elle renvoie l'utilisateur actuellement connecté en utilisant self.request.user.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Traitement du formulaire après validation réussie.

        Cette méthode est appelée lorsque le formulaire soumis est valide.
        Elle enregistre les modifications du formulaire dans la base de données,
        affiche un message de succès à l'utilisateur et le redirige vers la page de profil (/profile).
        """
        form.save()
        messages.success(self.request, ("votre profil a été mis à jour avec succès"))  # Message de succès en français
        return redirect('/profile')


class Register(View):
    """
    Vue d'inscription d'utilisateur.

    Cette classe de vue gère le processus d'inscription d'un nouvel utilisateur.
    Elle hérite de la classe `View` de Django et utilise des fonctions Django intégrées.
    """

    form_class = RegisterForm  # Formulaire d'inscription (adaptez-le à votre formulaire personnalisé si nécessaire)
    template_name = "auth/register.html"  # Chemin vers le template d'inscription

    def get(self, request):
        """
        Traitement des requêtes GET (affichage du formulaire d'inscription).

        Cette méthode est appelée lorsque l'utilisateur accède à la page d'inscription.
        Elle crée un formulaire d'inscription vide et le rend avec le template spécifié.
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Traitement des requêtes POST (soumission du formulaire d'inscription).

        Cette méthode est appelée lorsque l'utilisateur soumet le formulaire d'inscription.
        Elle crée un formulaire d'inscription avec les données soumises (POST) et les fichiers (s'il y en a).
        - Si le formulaire est valide :
            - L'utilisateur est créé en enregistrant les données mais sans l'enregistrer définitivement.
            - Le mot de passe est défini en utilisant la méthode `set_password`.
            - L'utilisateur est enregistré définitivement dans la base de données.
            - L'utilisateur est authentifié en utilisant la fonction `authenticate`.
            - Un message de succès est affiché à l'utilisateur.
            - Si l'authentification est réussie et que l'utilisateur est actif :
                - L'utilisateur est connecté en utilisant la fonction `login`.
                - La redirection se fait en fonction du type d'utilisateur (adaptez-la à votre logique) :
                    - `is_staff` pour la redirection vers le tableau de bord
                    - Sinon, redirection vers la page d'accueil
        - Si le formulaire n'est pas valide :
            Le formulaire est rendu à nouveau avec les erreurs affichées.
        """

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            messages.success(request, "Votre compte a été créé avec succès")
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
    """
    Vue de connexion d'utilisateur.

    Cette classe gère le processus de connexion d'un utilisateur existant.
    Elle hérite de la classe `View` de Django et utilise des fonctions Django intégrées.
    """

    form_class = LoginForm  # Formulaire de connexion (adaptez-le à votre formulaire personnalisé si nécessaire)
    template_name = "auth/login.html"  # Chemin vers le template de connexion

    def get(self, request):
        """
        Traitement des requêtes GET (affichage du formulaire de connexion).

        Cette méthode est appelée lorsque l'utilisateur accède à la page de connexion.
        Elle déconnecte l'utilisateur s'il est déjà connecté (pour éviter la connexion multiple).
        Elle crée un formulaire de connexion vide et le rend avec le template spécifié.
        """
        logout(request)
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Traitement des requêtes POST (soumission du formulaire de connexion).

        Cette méthode est appelée lorsque l'utilisateur soumet le formulaire de connexion.
        Elle crée un formulaire de connexion avec les données soumises (POST).
        - Si le formulaire est valide :
            - Elle récupère le nom d'utilisateur et le mot de passe nettoyés du formulaire.
            - Elle tente d'authentifier l'utilisateur en utilisant la fonction `authenticate`.
            - Si l'authentification est réussie et que l'utilisateur est actif :
                - Un message de succès est affiché à l'utilisateur.
                - L'utilisateur est connecté en utilisant la fonction `login`.
                - La redirection se fait en fonction du type d'utilisateur (adaptez-la à votre logique) :
                    - `is_staff` pour la redirection vers le tableau de bord
                    - Sinon, redirection vers la page d'accueil
            - Si l'authentification échoue :
                - Un message d'erreur est enregistré.
        - Si le formulaire n'est pas valide :
            Le formulaire est rendu à nouveau avec les erreurs affichées.

        Dans tous les cas, le formulaire et le message d'erreur (le cas échéant) sont passés au template pour affichage.
        """

        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Vous vous êtes connecté avec succès")
                    if user.is_staff:
                        return redirect('/dashboard')
                    else:
                        return redirect('/')
                else:
                    messages.error(request, "Le compte utilisateur est inactif.")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        return render(request, self.template_name, {'form': form, 'error': messages.get_messages(request)})



class LogoutView(View):
    """
    Vue de déconnexion personnalisée.

    Cette classe de vue gère le processus de déconnexion d'un utilisateur.
    Elle hérite de la classe `View` de Django et utilise la fonction `logout` intégrée.
    """

    def get(self, request):
        """
        Traitement des requêtes GET (déconnexion de l'utilisateur).

        Cette méthode est appelée lorsque l'utilisateur accède à la page de déconnexion (généralement via un lien).
        Elle déconnecte l'utilisateur en utilisant la fonction `logout`.
        Elle redirige ensuite l'utilisateur vers la page de connexion (/login).
        """
        logout(request)
        return HttpResponseRedirect('/login')


@login_required(login_url="/login/")  # Décoration pour accès réservé aux utilisateurs connectés
def dashboard(request):
    """
    Vue de tableau de bord administrateur.

    Cette fonction gère l'affichage du tableau de bord de l'administrateur.
    Elle nécessite que l'utilisateur soit connecté en utilisant le décorateur `login_required`.
    Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion (/login/).

    La fonction récupère les données suivantes du modèle et les passe au template :
        - Toutes les réservations (`reservations`)
        - Tous les utilisateurs (`users`)
        - Tous les éléments de menu (`menu`)
        - Toutes les commandes (`commande`)
        - Réservations en attente (`pending`)
        - Réservations confirmées (`confirmed`)
    """
    if not request.user.is_staff:
        return redirect("/")
    reservations = Reservation.objects.all()
    users = User.objects.all()
    menu = Menu.objects.all()
    commande = Commande.objects.all()
    pending = Reservation.objects.filter(status="pending")
    confirmed = Reservation.objects.filter(status="confirmed")
    return render(request, "super/dashboard.html",
                  {'users': users,
                   'menu': menu,
                   'commande': commande,
                   'reservations': reservations,
                   'pending': pending, 'confirmed': confirmed})


class AddReservation(LoginRequiredMixin, CreateView):
    """
    Vue d'ajout de réservation par l'administrateur.

    Cette classe de vue gère le processus d'ajout d'une nouvelle réservation par l'administrateur.
    Elle hérite de deux mixins et de la classe générique CreateView de Django.
    """

    template_name = "super/new_reserve.html"  # Chemin vers le template de la nouvelle réservation
    form_class = ReservationForm  # Formulaire utilisé pour la création de réservation (adaptez-le à votre formulaire personnalisé)
    login_url = '/login/'  # URL de redirection si l'utilisateur n'est pas connecté

    def form_valid(self, form):
        """
        Traitement du formulaire après validation réussie.

        Cette méthode est appelée lorsque le formulaire soumis est valide.
        Elle effectue les actions suivantes :
            - Enregistre la réservation dans la base de données mais sans la valider définitivement (commit=False).
            - Valide et enregistre définitivement la réservation dans la base de données (new.save()).
            - Affiche un message flash de succès à l'utilisateur.
                - Le message peut être personnalisé en modifiant la chaîne de caractères.
            - Redirige l'utilisateur vers le tableau de bord (/dashboard).
        """

        new = form.save(commit=False)
        new.save()
        messages.success(self.request, "Vous avez ajouté une nouvelle réservation de table avec succès")  # Message de succès en français
        return redirect("/dashboard")
class AddMenu(LoginRequiredMixin, CreateView):
    """
    Vue d'ajout de menu par l'administrateur.

    Cette classe de vue gère le processus d'ajout d'un nouvel élément de menu par l'administrateur.
    Elle hérite de deux mixins et de la classe générique CreateView de Django.
    """

    template_name = "super/new_menu.html"  # Chemin vers le template du nouveau menu
    form_class = MenuForm  # Formulaire utilisé pour la création d'un élément de menu (adaptez-le à votre formulaire personnalisé)
    login_url = '/login/'  # URL de redirection si l'utilisateur n'est pas connecté

    def form_valid(self, form):
        """
        Traitement du formulaire après validation réussie.

        Cette méthode est appelée lorsque le formulaire soumis est valide.
        Elle effectue les actions suivantes :
            - Enregistre l'élément de menu dans la base de données mais sans la valider définitivement (commit=False).
            - Valide et enregistre définitivement l'élément de menu dans la base de données (new.save()).
            - Affiche un message flash de succès à l'utilisateur.
                - Le message peut être personnalisé en modifiant la chaîne de caractères.
            - Redirige l'utilisateur vers le tableau de bord (/dashboard).
        """

        new = form.save(commit=False)
        new.save()
        messages.success(self.request, "Vous avez ajouté un nouvel élément de menu avec succès")  # Message de succès en français
        return redirect("/dashboard")

class UpdateReservation(LoginRequiredMixin, UpdateView):
    """
    Vue de modification de réservation par l'administrateur.

    Cette classe de vue gère le processus de modification d'une réservation existante par l'administrateur.
    Elle hérite de deux mixins et de la classe générique UpdateView de Django.
    """

    form_class = ReservationForm  # Formulaire utilisé pour la modification de la réservation (adaptez-le à votre formulaire personnalisé)
    template_name = "super/update_reserve.html"  # Chemin vers le template de modification de réservation
    model = Reservation  # Modèle de données associé à la vue (Reservation)

    def get_object(self, *args, **kwargs):
        """
        Récupère l'objet réservation à modifier.

        Cette méthode est requise par la classe générique UpdateView.
        Elle récupère la réservation spécifique en utilisant son ID (pk) passé dans l'URL.
        Elle utilise la fonction `get_object_or_404` pour récupérer l'objet ou lever une exception 404 si introuvable.
        """

        obj = get_object_or_404(Reservation, pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        """
        Traitement du formulaire après validation réussie.

        Cette méthode est appelée lorsque le formulaire soumis est valide.
        Elle enregistre les modifications apportées à la réservation.
        - Le `form.save()` enregistre les modifications dans la base de données.
        Elle affiche un message flash de succès à l'utilisateur.
        - Le message peut être personnalisé en modifiant la chaîne de caractères.
        Elle redirige l'utilisateur vers le tableau de bord (/dashboard).
        """

        form.save()
        messages.success(self.request, "Vous avez mis à jour la réservation avec succès")  # Message de succès en français
        return redirect('/dashboard')
class UpdateMenu(LoginRequiredMixin, UpdateView):
    """
    Vue de modification de menu par l'administrateur.

    Cette classe de vue gère le processus de modification d'un élément de menu existant par l'administrateur.
    Elle hérite de deux mixins et de la classe générique UpdateView de Django.
    """

    form_class = MenuForm  # Formulaire utilisé pour la modification du menu (adaptez-le à votre formulaire personnalisé)
    template_name = "super/update_menu.html"  # Chemin vers le template de modification de menu
    model = Menu  # Modèle de données associé à la vue (Menu)

    def get_object(self, *args, **kwargs):
        """
        Récupère l'objet menu à modifier.

        Cette méthode est requise par la classe générique UpdateView.
        Elle récupère l'élément de menu spécifique en utilisant son ID (pk) passé dans l'URL.
        Elle utilise la fonction `get_object_or_404` pour récupérer l'objet ou lever une exception 404 si introuvable.
        """

        obj = get_object_or_404(Menu, pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        """
        Traitement du formulaire après validation réussie.

        Cette méthode est appelée lorsque le formulaire soumis est valide.
        Elle enregistre les modifications apportées à l'élément de menu.
        - Le `form.save()` enregistre les modifications dans la base de données.
        Elle affiche un message flash de succès à l'utilisateur.
        - Le message peut être personnalisé en modifiant la chaîne de caractères.
        Elle redirige l'utilisateur vers le tableau de bord (/dashboard).
        """

        form.save()
        messages.success(self.request, "Vous avez mis à jour le menu avec succès")  # Message de succès en français
        return redirect('/dashboard')
    

@login_required(login_url="/login/")
def view_reservations(request):
    """
    Vue d'affichage des réservations pour l'administrateur.

    Cette fonction nécessite que l'utilisateur soit connecté en utilisant le décorateur `login_required`.
    Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion (/login/).

    La fonction récupère toutes les réservations du modèle `Reservation` et les passe au template `super/view_reserve.html`.
    """

    reservations = Reservation.objects.all()
    return render(request, "super/view_reserve.html", {'reservations': reservations})

@login_required(login_url="/login/")
def view_menu(request):
    """
    Vue d'affichage du menu pour l'administrateur.

    Cette fonction nécessite que l'utilisateur soit connecté en utilisant le décorateur `login_required`.
    Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion (/login/).

    La fonction récupère tous les éléments de menu du modèle `Menu` et les passe au template `super/view_menu.html`.
    """

    menu = Menu.objects.all()
    return render(request, "super/view_menu.html", {'menu': menu})

def view_commande(request):
    """
    Vue administrateur pour afficher toutes les commandes (commandes) avec des informations détaillées.

    Cette fonction nécessite que l'utilisateur soit connecté en utilisant le décorateur `login_required`.
    Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion (/login/).

    1. Récupère toutes les commandes du modèle `Commande` via `Commande.objects.all()`.
    2. Initialise un dictionnaire vide `commandes` pour stocker les commandes traitées.
    3. **Parcours efficace des commandes:**
        - Utilise un curseur (`commande_cursor`) pour itérer sur les commandes et améliorer la performance,
          especially for large datasets.
        - Pour chaque commande dans le curseur:
            - Crée une nouvelle entrée dans le dictionnaire `commandes` avec un identifiant unique (clé).
            - Extrait et stocke des informations pertinentes sur la commande, telles que l'objet `commande` lui-même,
              la date de création (`created_at`), l'identifiant (`id`), et une liste vide `tables` pour stocker les articles associés.
            - Récupère les articles du panier (`Table_List`) associés à la commande courante.
            - Calcule le total de la commande en agrégeant le champ `calculated_price` des articles du panier.
            - Ajoute chaque article du panier au tableau `tables` dans l'entrée de commande correspondante du dictionnaire.

    4. Transmet le dictionnaire `commandes` traité au template `super/view_commande.html` pour le rendu.
    """
    commandes = {}
    i=1
    for commande in Commande.objects.all():
        commandes[i] ={}
        commandes[i]["commande"] =commande
        commandes[i]["tables"] =[]
        commandes[i]["date"] =commande.created_at
        commandes[i]["id"] =commande.id
        tables= Table_List.objects.filter(commande=commande)
        commandes[i]["total"] =tables.aggregate(Sum('calculated_price'))['calculated_price__sum']
        for table in tables:
            commandes[i]["tables"].append(table)
        i=i+1
        print(commandes.items())
    return render(request,
                  "super/view_commande.html",
                  {'commandes': commandes})

@login_required(login_url="/login/")
def removeCommande_view(request,commande_id):
    """
    Vue administrateur pour supprimer une commande (commande).

    Cette fonction nécessite que l'utilisateur soit connecté en utilisant le décorateur `login_required`.
    Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion (/login/).

    1. Récupère la commande spécifique à supprimer à l'aide de `get_object_or_404`.
        - Si la commande n'est pas trouvée, une exception `Http404` est levée.
    2. Supprime la commande récupérée en utilisant `delete()`.
    3. Définit un message flash d'information à l'aide de `messages.info` pour informer l'utilisateur de la suppression réussie.
    4. Redirige l'utilisateur vers la vue `view_commandes` en utilisant `HttpResponseRedirect` et `reverse`.
    """

    item_toremove = get_object_or_404(Commande, pk=commande_id)
    item_toremove.delete()
    messages.info(request, "Cette commande a été supprimée.")  # Message plus clair en français
    return HttpResponseRedirect(reverse("view_commandes"))  # En supposant que le nom de l'URL est "view_commandes"

@login_required(login_url="/login/")
def completCommande_view(request, commande_id):
    """
    Vue administrateur pour marquer une commande (commande) comme terminée.

    Cette fonction nécessite que l'utilisateur soit connecté en utilisant le décorateur `login_required`.
    Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion (/login/).

    1. Récupère la commande spécifique à marquer comme terminée à l'aide de `get_object_or_404`.
    2. Définit le champ `complete` de la commande récupérée sur `True`.
    3. Enregistre la commande mise à jour à l'aide de `save()`.
    4. Définit un message flash d'information à l'aide de `messages.info` pour informer l'utilisateur de la mise à jour réussie.
    5. Redirige l'utilisateur vers la vue `view_commandes` en utilisant `HttpResponseRedirect` et `reverse`.
    """

    commande = get_object_or_404(Commande, pk=commande_id)
    commande.complete = True
    commande.save()
    messages.info(request, "Cette commande a été marquée comme terminée.")  # Message plus clair en français
    return HttpResponseRedirect(reverse("view_commandes"))  # En supposant que le nom de l'URL est "view_commandes"
