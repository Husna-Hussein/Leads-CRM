from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from  django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name ="agents/agent_list.html"
    

    def get_queryset(self):
        return Agent.objects.all()
