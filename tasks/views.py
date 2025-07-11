from django.shortcuts import render
from django.views.generic import TemplateView

# Index View
class IndexView(TemplateView):
    template_name = 'tasks/index.html'