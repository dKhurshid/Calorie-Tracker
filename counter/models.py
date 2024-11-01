from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class DiaryEntry(models.Model):
    CATEGORY_CHOICES = [
        ('uncategorized', 'Uncategorized'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make the user field nullable
    food_name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='uncategorized')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.food_name} - {self.calories} kcal"

class CalorieGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make the user field nullable
    goal = models.PositiveIntegerField()
    date_set = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.goal} kcal set on {self.date_set}"

class SavedEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make the user field nullable
    food_name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.food_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
