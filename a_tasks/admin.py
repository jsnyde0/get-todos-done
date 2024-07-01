from django.contrib import admin
from django.utils.html import format_html
from .models import Task, Board, Tag

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'assignee', 'review_stage', 'due_date', 'priority', 'type', 'completed', 'colored_review_stage')
    list_filter = ('review_stage', 'priority', 'type', 'completed', 'board')
    search_fields = ('title', 'description', 'author__username', 'assignee__username')
    autocomplete_fields = ('author', 'assignee', 'parent_task', 'board')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'type', 'parent_task')
        }),
        ('Assignment', {
            'fields': ('author', 'assignee', 'board', 'tags')
        }),
        ('Dates', {
            'fields': ('review_date', 'due_date', 'created_at', 'updated_at', 'completed_at')
        }),
        ('Status', {
            'fields': ('review_stage', 'priority', 'completed')
        }),
    )
    filter_horizontal = ('tags',)

    def colored_review_stage(self, obj):
        colors = {
            'INBOX': 'blue',
            'DAILY': 'green',
            'WEEKLY': 'purple',
            'MONTHLY': 'orange',
            'QUARTERLY': 'red',
            'PLANNED': 'teal',
            'SOMEDAY': 'gray',
            'MAYBE': 'pink',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.review_stage, 'black'),
            obj.get_review_stage_display()
        )
    colored_review_stage.short_description = 'Review Stage'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(author=request.user)
        return qs

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'task_count')
    list_filter = ('user',)
    search_fields = ('name', 'description', 'user__username')
    autocomplete_fields = ('user',)

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Number of Tasks'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'task_count')
    list_filter = ('user',)
    search_fields = ('name', 'description', 'user__username')
    autocomplete_fields = ('user',)

    def task_count(self, obj):
        return obj.task_set.count()
    task_count.short_description = 'Number of Tasks'