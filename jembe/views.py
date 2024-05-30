from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView,View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from project.models import User, Reservation,Menu,Table_List,Commande
from jembe.forms import ReservationForm, LoginForm, RegisterForm
from jembe.forms import ReservationForm, ContactForm
from django.db.models import Sum

import random
import string
import io
from django.http import FileResponse


from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

@login_required(login_url="/login/")
def home(request):
    # Définition du contexte pour passer des données à votre modèle
    context = {
		"menu" : Menu.objects.all(), # Récupère tous les objets Menu depuis la base de données
	}
    # Rend la page d'accueil (index.html) en utilisant le contexte défini
    return render(request, "index.html",context)

@login_required(login_url="/login/")
def about(request):
    # Rend la page about.html
    return render(request, "about.html")


class NewReservation(CreateView):
    # Spécifie le template utilisé pour rendre la page de réservation
    template_name = "reservation.html"
    # Spécifie le formulaire utilisé pour saisir les informations de réservation
    form_class = ReservationForm
    # Spécifie le modèle sur lequel cette vue est basée
    model = Reservation
    
    def get_form_kwargs(self):
        # Récupère les arguments du formulaire et les met à jour avec les valeurs initiales
        kwargs = super().get_form_kwargs()
        kwargs.update({'initial': {
             'email': self.request.user.email,
             'first_name': self.request.user.username,
             }})
        return kwargs
    
    def get_context_data(self, **kwargs):
        # Ajoute les réservations existantes de l'utilisateur connecté au contexte
        context = super().get_context_data(**kwargs)
        context['reservation'] = Reservation.objects.filter(first_name=self.request.user.username)
        return context
 
    def form_valid(self, form):
        # Enregistre la nouvelle réservation dans la base de données
        new = form.save(commit=False)
        new.save()
        # Envoie un message de succès à l'utilisateur
        messages.success(
            self.request,
            "Vous avez réservé avec succès une nouvelle table. Confirmez en payant la table."
        )
        # Redirige l'utilisateur vers la page de paiement
        return redirect("/payments")
class Contact(CreateView):
    # Spécifie le template utilisé pour rendre la page de contact
    template_name = "contact.html"
    # Spécifie le formulaire utilisé pour saisir les informations de contact
    form_class = ContactForm

    def form_valid(self, form):
        # Enregistre le nouveau message dans la base de données
        new = form.save(commit=False)
        new.save()
        # Envoie un message de succès à l'utilisateur
        messages.success(
            self.request,
            "Votre message a été envoyé avec succès."
        )
        # Redirige l'utilisateur vers la page de contact
        return redirect("/contact")

@login_required(login_url="/login/")
def payment(request):
    # Rend la page de paiement
    return render(request, "payment.html")

@login_required(login_url="/login/")
def table_view(request):
    if request.method == "POST":
        # Gère l'ajout d'un menu au panier
        item_id = request.POST.get("item_id")
        user = request.user
        p = Menu.objects.get(pk=item_id)
        print(item_id)
        total_price = p.prix 
        new_table = Table_List(user_id=user, menu_id=Menu.objects.get(pk = item_id),  calculated_price=total_price)

		# add item to table
        new_table.save()

		# return HttpResponseRedirect(reverse("table"))
        messages.success(request, "Menu ajouté dans à la commande !")
        return HttpResponseRedirect(reverse("home"))
        # return render(request, "orders/index.html", {"message": "Meal added to table!"})
    else:
        # Affiche le contenu actuel du panier
        commandes = {}
        i=1
        for commande in Commande.objects.filter(user_id=request.user.id):
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
        try:
            table = Table_List.objects.filter(user_id=request.user, is_current=True)
        except Table_List.DoesNotExist:
            raise Http404("table does not exist")
		
        total_price = table.aggregate(Sum('calculated_price'))['calculated_price__sum']

        table_ordered = Table_List.objects.filter(user_id=request.user, is_current=False)

        context = {

        "commandes":commandes,
        "table_items" : table,
        "total_price": total_price,
        "table_items_ordered" : table_ordered,
        }

        return render(request, "table.html", context)
    
@login_required(login_url="/login/")
def removefromtable_view(request, table_id):
	# Supprime un élément du panier
	item_toremove = Table_List.objects.get(pk=table_id)
	item_toremove.delete()
	messages.info(request,"Ce Menu a été supprimé de votre Commande.")
	return HttpResponseRedirect(reverse("table"))

@login_required(login_url="/login/")
def order_view(request):
	# passer une commande
	if request.method == "POST":
		user = request.user
		items = request.POST.getlist("table_id")
		print(items)

		new_order = Commande(user_id=user)

		new_order.save()

		for item in items:
			new_order.table_id.add(item)

		# set current attribute to False 
		table = Table_List.objects.filter(user_id=request.user)
		for item in table:
			item.is_current=False
			item.save()
	messages.success(request,"Merci d'avoir fait vos achats chez nous, votre commande a été passée.")
	return HttpResponseRedirect(reverse("home"))

@login_required(login_url="/login/")
def removeCommande_view(request,commande_id):
     # Supprime une commande
	item_toremove = Commande.objects.get(pk=commande_id)
	item_toremove.delete()
	messages.info(request,"Cette commande a été supprimé .")
	return HttpResponseRedirect(reverse("table"))

@login_required(login_url="/login/")
def removeReservation_view(request,reservation_id):
     # Supprime une réservation
	item_toremove = Reservation.objects.get(pk=reservation_id)
	item_toremove.delete()
	messages.info(request,"Cette réservation a été supprimé .")
	return HttpResponseRedirect(reverse("reservation"))

@login_required(login_url="/login/")
def downloadFacture_view(request,commande_id): 
    # Télécharge une facture 
    commande = Commande.objects.get(pk=commande_id)

    commandes={}
    commandes["id"]= 'F'+ ''.join(random.choice(string.ascii_lowercase) for i in range(6))  
    commandes["Nom_du_client"] = request.user.first_name + ' ' + request.user.last_name
    commandes["adresse_du_client"] =request.user.adresse
    commandes["Email_du_client"] =request.user.email
    commandes["Numero_de_telephone_du_client"] =request.user.telephone
    commandes["items"] = [] 
    tables= Table_List.objects.filter(commande=commande)
    for table in tables:
        c= table
        commandes["items"].append({"description": str(table).split(', - prix: € ')[0], "quantity": 1, "unit_price": int(str(table).split(', - prix: € ')[-1].split(".")[0])})
    #Générer une facture
    generate_invoice("media/facture.pdf", commandes)
    print(commandes.items())
    messages.info(request,"Cette commande a été téléchargé .")

    
    # Récupérez le fichier à télécharger
    filename = "media/facture.pdf"
    file = open(filename, 'rb')
    
    response = FileResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(commandes["id"])
    return response


def generate_invoice(filename, invoice_data):
        #Génère une facture
        # Création du document PDF
        document = SimpleDocTemplate(filename, pagesize=A4)
        content = []

        # Style des paragraphes
        styles = getSampleStyleSheet()
        style_title = styles['Heading1']
        style_normal = styles['Normal']

        # En-tête
        title = Paragraph("BEDJIGUI foods FACTURE", style_title)
        content.append(title)
        content.append(Spacer(1, 12))

        # Informations de la facture
        for key, value in invoice_data.items():
            if key != "items":
                info = f"<b>{key.capitalize()} :</b> {value}"
                content.append(Paragraph(info, style_normal))
        content.append(Spacer(1, 12))

        # Tableau des Menus
        items = invoice_data.get("items", [])
        table_data = [["designation", "Quantité", "Prix unitaire", "Total"]]
        for item in items:
            description = item.get("description", "")
            quantity = item.get("quantity", 0)
            unit_price = item.get("unit_price", 0)
            total = quantity * unit_price
            table_data.append([description, quantity, unit_price, total])
        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12)]))
        content.append(table)
        content.append(Spacer(1, 12))

        # Total de la facture
        total_amount = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in items)
        total_text = f"<b>Total :</b> {total_amount}"
        content.append(Paragraph(total_text, style_normal))

        # Générer le PDF
        document.build(content)