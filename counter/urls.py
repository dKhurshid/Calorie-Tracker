from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('calorie_calculator/', views.calorie_calculator, name='calorie_calculator'),
    path('calorie_results/<int:maintain_weight>/<int:mild_weight_loss>/<int:weight_loss>/<int:extreme_weight_loss>/<int:mild_weight_gain>/<int:weight_gain>/<int:extreme_weight_gain>/', views.calorie_results, name='calorie_results'),
    path('diary/', views.diary, name='diary'),
    path('diary/<str:date>/', views.diary, name='diary_with_date'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('get_entry/<int:entry_id>/', views.get_entry, name='get_entry'),
    path('diary_search_suggestions/', views.diary_search_suggestions, name='diary_search_suggestions'),
    path('fetch_food_details/', views.fetch_food_details, name='fetch_food_details'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('save_entry/', views.save_entry, name='save_entry'),
    path('delete_saved_entry/<int:entry_id>/', views.delete_saved_entry, name='delete_saved_entry'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='signup'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.CustomLogoutView.as_view(next_page='login'), name='logout'),
]
