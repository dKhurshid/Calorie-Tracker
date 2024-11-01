from django.contrib import admin
from .models import DiaryEntry, CalorieGoal
from .models import SavedEntry

@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'calories', 'protein', 'carbohydrates', 'fat', 'category', 'date','user')
    list_filter = ('category', 'date')
    search_fields = ('food_name','user__username')

@admin.register(CalorieGoal)
class CalorieGoalAdmin(admin.ModelAdmin):
    list_display = ('goal', 'date_set','user')
    list_filter = ('date_set',)
    search_fields = ('goal','user__username')

@admin.register(SavedEntry)
class SavedEntryAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'calories', 'protein', 'carbohydrates', 'fat', 'user')
    search_fields = ('food_name', 'user__username')