from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

class Task(models.Model):
    REVIEW_STAGES = [
        ('INBOX', 'Inbox'),
        ('DAILY', 'Review Daily'),
        ('WEEKLY', 'Review Weekly'),
        ('MONTHLY', 'Review Monthly'),
        ('QUARTERLY', 'Review Quarterly'),
        ('PLANNED', 'Subtask in Review/Planned'),
        ('SOMEDAY', 'Someday'),
        ('MAYBE', 'Maybe'),
    ]
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Urgent'),
    ]
    TYPE_CHOICES = [
        ('PROJECT', 'Project'),
        ('NEXT_ACTION', 'Next Action'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_authored')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_assigned')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
    review_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    review_stage = models.CharField(max_length=10, choices=REVIEW_STAGES, default='INBOX', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, null=True, blank=True)
    board = models.ForeignKey('Board', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    tags = models.ManyToManyField('Tag', blank=True)  # Changed to ManyToManyField
    type = models.CharField(max_length=11, choices=TYPE_CHOICES, default='NEXT_ACTION')

    def mark_as_completed(self):
        self.completed = True
        self.completed_at = timezone.now()
        self.save()

    def mark_as_incomplete(self):
        self.completed = False
        self.completed_at = None
        self.save()

    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now().date() and not self.completed

    # def get_absolute_url(self):
    #     return reverse('task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    
    def clean(self):
        if not self.parent_task and not self.review_stage:
            raise ValidationError("Review stage is required for top-level tasks.")
        if self.board and not self.review_stage:
            raise ValidationError("Review stage is required for tasks assigned to a board.")
        if self.review_stage and not (self.board or not self.parent_task):
            raise ValidationError("Review stage should only be set for top-level tasks or tasks assigned to a board.")
        
    def save(self, *args, **kwargs):
        if not self.pk and not self.assignee:  # Only for new tasks without an assignee
            self.assignee = self.author
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-priority', 'due_date', 'created_at']

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # def get_absolute_url(self):
    #     return reverse('board_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Boards"

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # def get_absolute_url(self):
    #     return reverse('tag_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name