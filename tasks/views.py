from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, RedirectView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

# Index View
class IndexView(TemplateView):
    template_name = 'tasks/index.html'

# Task List View
class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'tasks/task_list.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = self.model.objects.filter(task_owner = self.request.user, status__in=["Created", "Updated", "Restored"]).order_by('due_date')
        return queryset
    
# Completed Task List View
class CompletedTaskListView(LoginRequiredMixin, ListView):
    template_name = 'tasks/task_list_complete.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = self.model.objects.filter(task_owner = self.request.user, status = "Completed")
        return queryset
    
# Task Detail View
class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name = 'tasks/task_detail.html'
    model = Task
    context_object_name = 'task'
    pk_url_kwarg = 'pk'

# Create Task View
class CreateTaskView(LoginRequiredMixin, CreateView):
    template_name = 'tasks/task_form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

    def post(self, request):
        form = TaskForm(request.POST)
        if not form.is_valid():
            context = {
                'form':form
            }
            return render(request, self.template_name, context)
        
        # Add the status of the record
        obj = form.save(commit = False)
        obj.task_owner = request.user
        obj.status = "Created"
        obj.save()

        messages.success(request, "Your task has been created successfully.")
        return redirect(self.success_url)
    
# Update Task View
class UpdateTaskView(LoginRequiredMixin, UpdateView):
    template_name = 'tasks/task_form.html'
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks:task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        context['form'] = TaskForm(instance=task)
        context['form_type'] = "update"
        return context

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        form = TaskForm(request.POST, instance=task)
        if not form.is_valid():
            context = {
                'form':form
            }
            return render(request, self.template_name, context)
        
        # Update the status of the record
        obj = form.save(commit = False)
        obj.status = "Updated"
        obj.date = datetime.now()
        obj.save()

        messages.success(request, "Your task has been updated successfully.")
        return redirect(self.success_url)
    
# Complete Task
class CompleteTask(LoginRequiredMixin, RedirectView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        # Update the status of the record
        task.status = "Completed"
        task.date = datetime.now()
        task.save()

        messages.success(request, "Your task has been marked as finished.")
        return redirect(self.success_url)
    
# Restore Task
class RestoreTask(LoginRequiredMixin, RedirectView):
    model = Task
    success_url = reverse_lazy('tasks:task_list_complete')

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        # Update the status of the record
        task.status = "Restored"
        task.date = datetime.now()
        task.save()

        messages.success(request, "Your task has been restored.")
        return redirect(self.success_url)
    
# Delete Task View
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('tasks:task_list_complete')
    context_object_name = 'task'