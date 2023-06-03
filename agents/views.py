from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.shortcuts import reverse
from django.views import generic
from  django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginrequired

class AgentListView(OrganiserAndLoginrequired, generic.ListView):
    template_name ="agents/agent_list.html"
    

    def get_queryset(self):
        organisation = self.request.user.userprofile

        return Agent.objects.filter(organisation=organisation)
    
class AgentCreateView(OrganiserAndLoginrequired, generic.CreateView):
    template_name ="agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self) :
        return reverse("agents:agent-list")


    def form_valid(self, form):
         agent = form.save(commit =False)
         agent.organisation = self.request.user.userprofile
         agent.save()
         return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganiserAndLoginrequired, generic.DetailView):
    template_name="agents/agent_detail.html"
    context_object_name = "agent"

    
    def get_queryset(self):
        organisation = self.request.user.userprofile

        return Agent.objects.filter(organisation=organisation)
    
    
class AgentUpdateView(OrganiserAndLoginrequired, generic.UpdateView):
    template_name ="agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self) :
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        return Agent.objects.all()
    

class AgentDeleteView(OrganiserAndLoginrequired, generic.DeleteView):
    template_name="agents/agent_delete.html"
    context_object_name = "agent"

    
    def get_success_url(self) :
        return reverse("agents:agent-list")

    
    def get_queryset(self):
        organisation = self.request.user.userprofile

        return Agent.objects.filter(organisation=organisation)
    


