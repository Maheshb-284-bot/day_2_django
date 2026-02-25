from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def task_list(request):
    """Display all tasks and handle adding new tasks."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')

    tasks = Task.objects.order_by('-created_at')
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = total - completed
    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
    }
    return render(request, 'tasks/task_list.html', context)


def task_complete(request, task_id):
    """Toggle the completion status of a task."""
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


def task_delete(request, task_id):
    """Delete a task."""
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('task_list')
