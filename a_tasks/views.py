import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import ReviewStage, Task, Board

# Create your views here.
def list_view(request):
    review_stages = ReviewStage.objects.all()
    context = {
        'review_stages': review_stages
    }
    return render(request, 'tasks/todo_board.html', context)

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
