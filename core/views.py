# Created by Rejone Hossen | Premium Task Manager | 2025

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task, Category, Tag, SharedList
from .forms import TaskForm, CategoryForm, TagForm, SharedListForm
from django.contrib.auth.models import User
from django.utils import timezone



from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')  # Redirect to task dashboard

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful. Welcome, " + user.username + "!")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('order', '-priority', 'due_date')
    categories = Category.objects.filter(user=request.user)
    tags = Tag.objects.filter(user=request.user)
    shared_lists = SharedList.objects.filter(collaborators=request.user)
    
    # Filtering logic
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')
    priority = request.GET.get('priority')
    search_query = request.GET.get('search')
    
    if category_id:
        tasks = tasks.filter(category__id=category_id)
    if tag_id:
        tasks = tasks.filter(tags__id=tag_id)
    if priority:
        tasks = tasks.filter(priority=priority)
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
    
    context = {
        'tasks': tasks,
        'categories': categories,
        'tags': tags,
        'shared_lists': shared_lists,
        'priority_choices': Task.priority,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()  # For many-to-many fields
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'completed': task.completed})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('task_list')
    else:
        form = CategoryForm()
    return render(request, 'tasks/category_form.html', {'form': form})

@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('task_list')
    else:
        form = TagForm()
    return render(request, 'tasks/tag_form.html', {'form': form})

@login_required
def shared_list_create(request):
    if request.method == 'POST':
        form = SharedListForm(request.POST)
        if form.is_valid():
            shared_list = form.save(commit=False)
            shared_list.owner = request.user
            shared_list.save()
            form.save_m2m()  # For collaborators
            messages.success(request, 'Shared list created successfully!')
            return redirect('task_list')
    else:
        form = SharedListForm()
    return render(request, 'tasks/shared_list_form.html', {'form': form})

@login_required
def shared_list_detail(request, pk):
    shared_list = get_object_or_404(SharedList, pk=pk)
    if request.user not in shared_list.collaborators.all() and request.user != shared_list.owner:
        messages.error(request, 'You do not have permission to view this list.')
        return redirect('task_list')
    
    tasks = shared_list.tasks.all().order_by('order', '-priority', 'due_date')
    context = {
        'shared_list': shared_list,
        'tasks': tasks,
    }
    return render(request, 'tasks/shared_list.html', context)

@login_required
def profile(request):
    user = request.user
    tasks_count = Task.objects.filter(user=user).count()
    completed_count = Task.objects.filter(user=user, completed=True).count()
    overdue_count = Task.objects.filter(user=user, due_date__lt=timezone.now(), completed=False).count()
    
    context = {
        'user': user,
        'tasks_count': tasks_count,
        'completed_count': completed_count,
        'overdue_count': overdue_count,
    }
    return render(request, 'tasks/profile.html', context)

@require_POST
@login_required
def update_task_order(request):
    task_order = request.POST.getlist('task_order[]')
    for index, task_id in enumerate(task_order):
        Task.objects.filter(id=task_id, user=request.user).update(order=index)
    return JsonResponse({'status': 'success'})