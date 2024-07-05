import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from .models import ReviewStage, Task, Board, Tag
from .forms import TaskForm

# Create your views here.
def list_view(request):
    review_stages = ReviewStage.objects.all()
    tasks = Task.objects.all()

    # Apply filters
    boards = request.GET.getlist('boards')
    tags = request.GET.getlist('tags')
    completed = request.GET.get('completed')
    task_type = request.GET.get('type')
    priority = request.GET.getlist('priority')

    if boards:
        tasks = tasks.filter(board__in=boards)
    if tags:
        tasks = tasks.filter(tags__in=tags)
    if completed:
        tasks = tasks.filter(completed=completed == 'true')
    if task_type:
        tasks = tasks.filter(type=task_type)
    if priority:
        tasks = tasks.filter(priority__in=priority)

    # Date filters
    created_after = request.GET.get('created_after')
    created_before = request.GET.get('created_before')
    updated_after = request.GET.get('updated_after')
    updated_before = request.GET.get('updated_before')
    due_after = request.GET.get('due_after')
    due_before = request.GET.get('due_before')
    review_after = request.GET.get('review_after')
    review_before = request.GET.get('review_before')

    if created_after:
        tasks = tasks.filter(created_at__gte=created_after)
    if created_before:
        tasks = tasks.filter(created_at__lte=created_before)
    if updated_after:
        tasks = tasks.filter(updated_at__gte=updated_after)
    if updated_before:
        tasks = tasks.filter(updated_at__lte=updated_before)
    if due_after:
        tasks = tasks.filter(due_date__gte=due_after)
    if due_before:
        tasks = tasks.filter(due_date__lte=due_before)
    if review_after:
        tasks = tasks.filter(review_date__gte=review_after)
    if review_before:
        tasks = tasks.filter(review_date__lte=review_before)

    # Group tasks by review stage
    for stage in review_stages:
        stage.filtered_tasks = tasks.filter(review_stage=stage)

    context = {
        'review_stages': review_stages,
        'boards': Board.objects.all(),
        'tags': Tag.objects.all(),
        'priorities': Task.PRIORITY_CHOICES,
    }

    if request.htmx:
        return render(request, 'tasks/todo_board.html#kanban_board', context)
    return render(request, 'tasks/todo_board.html', context)

def view_create_update_task(request, id=None):
    if not request.htmx:
        return HttpResponseBadRequest("This view is only accessible via HTMX.")
    
    # Simulate a delay of 0.5 seconds
    time.sleep(0.5)

    # Get or create a task
    if id:
        task = get_object_or_404(Task, id=id)
    else:
        # For now, set board to 'Default'. This will have to change eventually 
        board = Board.objects.get(name="Default")
        review_stage_id = request.GET.get('review_stage')
        review_stage = ReviewStage.objects.get(id=review_stage_id) if review_stage_id else None
        task = Task.objects.create(
            author=request.user,
            board=board,
            review_stage=review_stage,
            created_at = now(),
            )
    
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid(): # why does it not enter here?
        form.instance.updated_at = now()
        task = form.save()
        
    context = {
        'task': task,
        'taskform': form,
    }

    return render(request, 'tasks/todo_board.html#task_update', context)

def view_task(request, id):
    if not request.htmx:
        return HttpResponseBadRequest("This view is only accessible via HTMX.")
    
    # Simulate a delay of 0.5 seconds
    time.sleep(0.5)

    task = get_object_or_404(Task, id=id)
    context = {
        'task': task
    }

    return render(request, 'tasks/todo_board.html#task_detail_content', context)

@require_POST
def toggle_task_completed(request, id):
    if not request.htmx:
        return HttpResponseBadRequest("This view is only accessible via HTMX.")
    
    # toggle the completed state of the task
    task = get_object_or_404(Task, id=id)
    task.completed = not task.completed
    task.completed_at = now() if task.completed else None  # Set or clear the completed_at timestamp

    task.save()
    return HttpResponse(status=204)  # Return a 204 No Content response

@require_POST
def update_subtask_title(request, id):
    subtask = get_object_or_404(Task, id=id)
    new_title = request.POST.get('title', '').strip()
    print('new title: ', new_title)
    if new_title:
        subtask.title = new_title
        subtask.save()
    context={'subtask': subtask}
    return render(request, 'tasks/todo_board.html#subtask_title_form', context)