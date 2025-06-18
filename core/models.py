# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
# Created by Rejone Hossen | Premium Task Manager | 2025
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



def user_profile_image_path(instance, filename):
    return f'profile_pics/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_image_path,
        default='default_profile.png',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    theme = models.CharField(
        max_length=10,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )
    is_premium = models.BooleanField(default=True)  # All users premium by default in your project
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


PRIORITY_CHOICES = [
    ('H', 'High 🔥'),
    ('M', 'Medium ⭐'),
    ('L', 'Low ✅'),
]

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#3B82F6')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"#{self.name}"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-priority', 'due_date']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return self.due_date and timezone.now() > self.due_date

    @property
    def time_left(self):
        if not self.due_date:
            return None
        delta = self.due_date - timezone.now()
        if delta.total_seconds() < 0:
            return "Overdue"
        days = delta.days
        hours = delta.seconds // 3600
        if days > 0:
            return f"{days}d {hours}h left"
        return f"{hours}h left"

class SharedList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_lists')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    collaborators = models.ManyToManyField(User, related_name='collaborating_lists')
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return self.title