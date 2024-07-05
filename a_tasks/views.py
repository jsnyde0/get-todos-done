import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from .models import ReviewStage, Task, Board
from .forms import TaskForm

# Create your views here.
def list_view(request):
    review_stages = ReviewStage.objects.all()
    context = {
        'review_stages': review_stages
    }
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
        print(f"Review stage sent with request: {review_stage}")
        task = Task.objects.create(
            author=request.user,
            board=board,
            review_stage=review_stage,
            created_at = now(),
            )
    
    print(f"Task review stage before form: {task.review_stage}")
    form = TaskForm(request.POST or None, instance=task)
    print(f"POST data: {request.POST}")
    if form.is_valid(): # why does it not enter here?
        form.instance.updated_at = now()
        task = form.save()
    else:
        print("Form is not valid. Errors:", form.errors)
        print(f"Form data: {form.data}")
        
    print(f"Task review stage after form processing: {task.review_stage}")

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