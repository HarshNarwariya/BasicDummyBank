from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Record
import json

# Create your views here.
@login_required
def index(request):
    data = request.user.record_set.all()[:10]
    last_10_transactions = [[i+1, r.amount] for i, r in enumerate(data)]
    
    return render(request, template_name="Main/index.html", context={
        "last_transactions": last_10_transactions,
    })


class MakeTransaction(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Record
    fields = ['amount', 'is_deposited', 'description']
    template_name = "Main/make_transaction.html"
    success_message = "Transaction was successfull"

    def get_success_url(self) -> str:
        return reverse("main:transactions")

    def form_valid(self, form):
        form.instance.author = self.request.user
        account = self.request.user.account
        amount = form.cleaned_data.get('amount')
        is_deposited = form.cleaned_data.get('is_deposited')
        if is_deposited:
            account.balance += amount
            account.total_deposited += amount
        else:
            if account.balance < amount:
                messages.warning(self.request, f'You don\'t have enough money. Your balance {account.balance}')
                return redirect('main:make_transaction')
            else:
                account.balance -= amount
                account.total_withdrawl += amount
        form.instance.total = account.balance
        account.save()
        return super().form_valid(form)

class RecordList(LoginRequiredMixin, ListView):
    model = Record
    template_name = "Main/record_list.html"
    paginate_by = 25

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)  

class RecordUpdate(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Record
    template_name = "Main/updaterecord.html"
    fields = ['amount', 'is_deposited', 'description']
    success_message = "Transaction was updated successfully"
    
    def get_success_url(self):
        return reverse("main:transactions")

    def post(self, request,  *args, **kwargs):
        self.popped_object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        account = self.request.user.account

        # Remove Old Transaction
        amount = self.popped_object.amount
        is_deposited = self.popped_object.is_deposited
        if is_deposited:
            if account.balance < amount:
                messages.warning(self.request, f'You don\'t have enough money.')
                return redirect('main:transactions')
            else:
                account.balance -= amount
                account.total_deposited -= amount
        else:
            account.balance += amount
            account.total_withdrawl -= amount

        # Add New Transaction
        popped_amount = self.popped_object.amount
        amount = form.cleaned_data.get('amount')
        is_deposited = form.cleaned_data.get('is_deposited')
        if is_deposited:
            account.balance += amount
            account.total_deposited += amount
        else:
            if account.balance < amount:
                messages.warning(self.request, f'You don\'t have enough money')
                return redirect('main:transactions')
            else:
                account.balance -= amount
                account.total_withdrawl += amount
        form.instance.total = account.balance
        account.save()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class RecordDelete(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Record
    success_message = "Work was deleted successfully"

    def form_valid(self, form):
        record = self.object
        account = self.request.user.account
        if record.is_deposited:
            account.total_deposited -= record.amount
            account.balance -= record.amount
        else:
            account.total_withdrawl -= record.amount
            account.balance += record.amount
        account.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:transactions")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False