from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Customer, Subscription, Invoice
import time

Plans_Cost = {
    "Plan 1": 2,
    "Plan 2": 5,
    "Plan 3": 10
}


def index(request):
    return render(request=request, template_name="finance/index.html")


def theregister(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("finance:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="finance/register.html", context={"register_form": form})


def thelogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("finance:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="finance/login.html", context={"login_form": form})


def thelogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("finance:home")


def pricing(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=request.user.id)
        subscriptions = Subscription.objects.filter(customer=customer)
        plan1 = subscriptions.filter(name="Plan 1")
        plan2 = subscriptions.filter(name="Plan 2")
        plan3 = subscriptions.filter(name="Plan 3")
        context = {
            'subscriptions': subscriptions,
            'Plan1': plan1,
            'Plan2': plan2,
            'Plan3': plan3,
        }
    else:
        context = {
        }
    return render(request=request, template_name="finance/plans.html", context=context)


def profile(request, user_id):
    create_invoices(request)
    customer = Customer.objects.get(id=user_id)
    subscriptions = Subscription.objects.filter(customer=customer)
    invoices = Invoice.objects.filter(customer=customer)
    context = {
        'customer': customer,
        'subscriptions': subscriptions,
        'invoices': invoices
    }
    print(context['subscriptions'])
    print(context['invoices'])
    return render(request=request, template_name="finance/profile.html", context=context)


def subscribe(request, plan):
    customer = Customer.objects.get(id=request.user.id)
    subscriptions = Subscription.objects.filter(customer=customer)
    newsubscription = Subscription.objects.create(customer=customer, name=plan, cost=Plans_Cost[plan], is_active=True)

    return redirect("finance:pricing")


def unsubscribe(request, plan):
    customer = Customer.objects.get(id=request.user.id)
    subscriptions = Subscription.objects.filter(customer=customer)
    deletesubscription = subscriptions.filter(name=plan).delete()

    return redirect("finance:pricing")


def active(request, plan):
    customer = Customer.objects.get(id=request.user.id)
    subscriptions = Subscription.objects.filter(customer=customer)
    invoices = Invoice.objects.filter(customer=customer)

    sub = Subscription.objects.get(name=plan)
    sub.start_time = round(time.time() - sub.stop_timer) + sub.start_time
    sub.save()

    updatesubscription = subscriptions.filter(name=plan).update(is_active=True)
    context = {
        'customer': customer,
        'subscriptions': subscriptions,
        'invoices': invoices
    }
    return render(request=request, template_name="finance/profile.html", context=context)


def deactive(request, plan):
    customer = Customer.objects.get(id=request.user.id)
    subscriptions = Subscription.objects.filter(customer=customer)
    invoices = Invoice.objects.filter(customer=customer)

    sub = Subscription.objects.get(name=plan)
    sub.stop_timer = round(time.time())
    sub.save()

    updatesubscription = subscriptions.filter(name=plan).update(is_active=False)
    context = {
        'customer': customer,
        'subscriptions': subscriptions,
        'invoices': invoices
    }
    return render(request=request, template_name="finance/profile.html", context=context)


def create_invoices(request):
    now = round(time.time())
    subscriptions = Subscription.objects.filter(is_active=True)
    for subscription in subscriptions:
        elapsed_time = subscription.start_time + 600
        if elapsed_time <= now:
            subscription_type = Subscription.objects.get(name=subscription.name)
            Invoice.objects.create(customer=subscription.customer, subscription_type=subscription_type,
                                   price=subscription.cost, start_date=subscription.start_time, end_date=now,)

            subscription.start_time = elapsed_time
            subscription.save()

            customer = Customer.objects.get(id=request.user.id)
            customer.credit -= subscription.cost
            customer.save()
