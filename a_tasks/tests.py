from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task, Board

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.board = Board.objects.create(user=self.user, name='TestBoard')

    def test_assignee_default_to_author(self):
        # Create a task without specifying an assignee
        task = Task.objects.create(
            title='Test Task',
            author=self.user,
            board=self.board,
            review_stage='INBOX'
        )
        
        # Check if the assignee is automatically set to the author
        self.assertEqual(task.assignee, self.user)

    def test_assignee_remains_when_specified(self):
        # Create another user to be the assignee
        other_user = User.objects.create_user(username='otheruser', password='12345')
        
        # Create a task with a specific assignee
        task = Task.objects.create(
            title='Test Task',
            author=self.user,
            assignee=other_user,
            board=self.board,
            review_stage='INBOX'
        )
        
        # Check if the assignee remains as specified
        self.assertEqual(task.assignee, other_user)