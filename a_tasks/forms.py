from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'review_date', 'board', 
                  'review_stage', 'priority', 'type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'bg-transparent focus:outline-none focus:ring-2 focus:ring-purple-600 rounded px-2 py-1 w-full'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-gray-800 text-gray-200 w-full p-2 rounded focus:outline-none focus:ring-2 focus:ring-purple-600',
                'rows': 4
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bg-gray-800 text-gray-200 p-2 rounded w-full'
            }),
            'review_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bg-gray-800 text-gray-200 p-2 rounded w-full'
            }),
            'board': forms.Select(attrs={
                'class': 'bg-gray-800 text-gray-200 p-2 rounded w-full'
            }),
            'review_stage': forms.Select(attrs={
                'class': 'bg-gray-800 text-gray-200 p-2 rounded w-full'
            }),
            'priority': forms.Select(attrs={
                'class': 'bg-gray-800 text-gray-200 p-2 rounded w-full'
            }),
            'type': forms.Select(attrs={
                'class': 'bg-gray-800 text-gray-200 p-2 rounded w-full'
            }),
        }