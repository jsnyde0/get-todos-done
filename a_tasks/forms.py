from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'review_date', 'board', 
                  'review_stage', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-transparent focus:outline-none focus:ring-2 focus:ring-purple-600 rounded px-2 py-1'}),
            'description': forms.Textarea(attrs={'class': 'bg-gray-800 text-gray-200 w-full p-2 rounded focus:outline-none focus:ring-2 focus:ring-purple-600', 'rows': 4}),
        }