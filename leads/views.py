from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm,CustomUserCreationForm
from agents.mixins import OrganiserAndLoginrequired

class SignUpView(generic.CreateView):
    template_name="registration/signup.html"
    form_class=CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView( generic.TemplateView):
    template_name="landing.html"

def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name="leads/lead_list.html"
    context_object_name ="leads"
    
    def get_queryset(self) :
       user = self.request.user
       if user.is_organiser:
         queryset = Lead.objects.filter(organisation =user.userprofile)
       else:
            queryset = Lead.objects.filter(organisation =user.agent.organisation)

            queryset = queryset.filter(agent__user=user)
       return queryset



def lead_list(request):
    leads = Lead.objects.all()
    context= {
        "leads":leads
    }
    return render(request, "leads/lead_list.html", context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name="leads/lead_detail.html"
    queryset =Lead.objects.all()
    context_object_name ="lead"

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context={
         "lead":lead
    }
    return render(request, "leads/lead_detail.html", context)


class LeadCreateView(OrganiserAndLoginrequired, generic.CreateView):
    template_name="leads/lead_create.html"
    form_class=LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        # ToDo send email
        send_mail(
            subject="A lead has been created",
            message= "Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView,self).form_valid(form)
    
    


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        
        form = LeadModelForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect("/leads")

    context = {
        "form": form
    }

    return render(request, "leads/lead_create.html", context)

class LeadUpdateView(OrganiserAndLoginrequired, generic.UpdateView):
    template_name="leads/lead_update.html"
    queryset =Lead.objects.all()
    form_class=LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
          form.save()
          return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganiserAndLoginrequired, generic.DeleteView):
    template_name="leads/lead_delete.html"
    queryset =Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")
    


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

# def lead_update(request, pk):
#    lead = Lead.objects.get(id=pk)
#    form = LeadForm()
#    if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#           first_name = form.cleaned_data['first_name']
#           last_name = form.cleaned_data['last_name']
#           age = form.cleaned_data['age']
#           lead.first_name = first_name
#           lead.last_name = last_name
#           lead.age = age
#           lead.save()
#           return redirect("/leads")
#    context = {
#         "form": form,
#         "lead": lead
#     }
#    return render(request, "leads/lead_update.html", context)

