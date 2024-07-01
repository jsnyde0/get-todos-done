from django.shortcuts import render

# Create your views here.
def list_view(request):
    return render(request, 'tasks/todo_board.html', {})