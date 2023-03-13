from datetime import date
from django.shortcuts import render
from django.http import HttpResponse

from ReplyAPI.models import User
from .forms import RegisterForm ,PaymentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                return HttpResponse(status=409)
            dob = form.cleaned_data['dob']
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                return HttpResponse(status=403)
            form.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
    else:
        form = RegisterForm()
        if 'success' in request.GET:
            success = True
        else:
            success = False
        return render(request, 'register.html', {'form': form, 'success': success})
def login(request):
    return render(request, 'login.html')

def payment(request):
    form = PaymentForm()
    credit_card = request.POST['credit_card']
    amount = request.POST['amount']
    credit_cards = User.objects.filter(credit_card__isnull=False).values_list('credit_card', flat=True)
    if len(str(credit_card)) != 16 or len(str(amount)) != 3:
        return HttpResponse(status=400)
    if credit_card not in credit_cards:
         return HttpResponse(status=404)
    else:   
        return HttpResponse(status=201)

def credit_card(request):

    # users_with_credit_cards = User.objects.exclude(credit_card='')
    # users_without_credit_cards = User.objects.filter(credit_card='')

    # context = {
    #     'users_with_credit_cards': users_with_credit_cards,
    #     'users_without_credit_cards': users_without_credit_cards
    # }
    no_credit_users = []
    credit_cards = []
    for user in User.objects.all():
        if user.credit_card is None:
            no_credit_users.append(user)
        else: credit_cards.append(user)

    context = {
        'users_with_credit_cards': credit_cards,
        'users_without_credit_cards': no_credit_users
    }
    return render(request, 'credit_card.html', context)