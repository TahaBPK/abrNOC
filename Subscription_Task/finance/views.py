from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Customer, Subscription, Invoice

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
    return render(request=request, template_name="finance/plans.html", context=context)


def profile(request, user_id):
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
    updatesubscription = subscriptions.filter(name=plan).update(is_active=False)
    context = {
        'customer': customer,
        'subscriptions': subscriptions,
        'invoices': invoices
    }
    return render(request=request, template_name="finance/profile.html", context=context)
