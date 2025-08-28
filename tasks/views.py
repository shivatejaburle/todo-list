from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, RedirectView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib import messages

# Index View
class IndexView(TemplateView):
    template_name = 'tasks/index.html'

# Task List View
class TaskListView(ListView):
    template_name = 'tasks/task_list.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = self.model.objects.filter(status__in=["Created", "Updated"])
        return queryset
    
# Completed Task List View
class CompletedTaskListView(ListView):
    template_name = 'tasks/task_list_complete.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = self.model.objects.filter(status = "Completed")
        return queryset

# Create Task View
class CreateTaskView(CreateView):
    template_name = 'tasks/task_form.html'
    model = Task
    fields = ['title', 'description']
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
        obj.status = "Created"
        obj.save()

        messages.success(request, "Your task has been created successfully.")
        return redirect(self.success_url)
    
# Update Task View
class UpdateTaskView(UpdateView):
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
        obj.save()

        messages.success(request, "Your task has been updated successfully.")
        return redirect(self.success_url)
    
# Complete Task
class CompleteTask(RedirectView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        # Update the status of the record
        task.status = "Completed"
        task.save()

        messages.success(request, "Your task has been marked as finished.")
        return redirect(self.success_url)
    
# Restore Task
class RestoreTask(RedirectView):
    model = Task
    success_url = reverse_lazy('tasks:task_list_complete')

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        # Update the status of the record
        task.status = "Updated"
        task.save()

        messages.success(request, "Your task has been restored.")
        return redirect(self.success_url)
    
# Delete Task View
class DeleteTaskView(DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('tasks:task_list_complete')
    context_object_name = 'task'