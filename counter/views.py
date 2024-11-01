from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import requests
import re
from .forms import CalorieCalculatorForm
from .models import DiaryEntry, CalorieGoal, SavedEntry
from django.utils import timezone
from datetime import datetime, date as dt_date
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout


@login_required
def home(request):
    form = CalorieCalculatorForm()

    if request.method == 'POST':
        if 'food_name_search' in request.POST:
            food_name = request.POST.get('food_name_search')

            # Nutritionix API
            nutritionix_api_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
            nutritionix_headers = {
                'x-app-id': '13488eb7',
                'x-app-key': '384e715b18d52e9de03d6e5134943ea6',
                'Content-Type': 'application/json'
            }
            nutritionix_data_payload = {
                'query': food_name,
                'num_servings': 1
            }

            try:
                # Fetching data from Nutritionix
                nutritionix_response = requests.post(nutritionix_api_url, headers=nutritionix_headers, json=nutritionix_data_payload)
                nutritionix_response.raise_for_status()
                nutritionix_data = nutritionix_response.json()

                if nutritionix_data and 'foods' in nutritionix_data:
                    food = nutritionix_data['foods'][0]
                    return render(request, 'home.html', {
                        'food_name': food['food_name'],
                        'calories': food['nf_calories'],
                        'protein': food['nf_protein'],
                        'carbohydrates': food['nf_total_carbohydrate'],
                        'fat': food['nf_total_fat'],
                        'cholesterol': food['nf_cholesterol'],
                        'saturated_fat': food['nf_saturated_fat'],
                        'fiber': food['nf_dietary_fiber'],
                        'potassium': food['nf_potassium'],
                        'sodium': food['nf_sodium'],
                        'sugar': food['nf_sugars'],
                        'form': form
                    })
            except requests.exceptions.RequestException as e:
                return render(request, 'home.html', {
                    'form': form,
                    'error': str(e)
                })

    return render(request, 'home.html', {'form': form})

@login_required
def calorie_calculator(request):
    calculated_calories = None

    if request.method == 'POST':
        form = CalorieCalculatorForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            activity_level = form.cleaned_data['activity_level']

            # Calculate BMR using different equations
            if gender == 'male':
                bmr_mifflin = 10 * weight + 6.25 * height - 5 * age + 5
                bmr_harris = 13.397 * weight + 4.799 * height - 5.677 * age + 88.362
            else:
                bmr_mifflin = 10 * weight + 6.25 * height - 5 * age - 161
                bmr_harris = 9.247 * weight + 3.098 * height - 4.330 * age + 447.593

            activity_multipliers = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725,
                'extra_active': 1.9
            }
            activity_factor = activity_multipliers[activity_level]

            tdee_mifflin = bmr_mifflin * activity_factor
            tdee_harris = bmr_harris * activity_factor

            return redirect('calorie_results', 
                            maintain_weight=int(tdee_mifflin), 
                            mild_weight_loss=int(tdee_mifflin * 0.9), 
                            weight_loss=int(tdee_mifflin * 0.8), 
                            extreme_weight_loss=int(tdee_mifflin * 0.61), 
                            mild_weight_gain=int(tdee_mifflin * 1.1), 
                            weight_gain=int(tdee_mifflin * 1.2), 
                            extreme_weight_gain=int(tdee_mifflin * 1.4))
    else:
        form = CalorieCalculatorForm()

    return render(request, 'calorie_calculator.html', {
        'form': form,
        'calculated_calories': calculated_calories
    })

def calorie_results(request, maintain_weight, mild_weight_loss, weight_loss, extreme_weight_loss, mild_weight_gain, weight_gain, extreme_weight_gain):
    calculated_calories = {
        'maintain_weight': maintain_weight,
        'mild_weight_loss': mild_weight_loss,
        'weight_loss': weight_loss,
        'extreme_weight_loss': extreme_weight_loss,
        'mild_weight_gain': mild_weight_gain,
        'weight_gain': weight_gain,
        'extreme_weight_gain': extreme_weight_gain
    }

    zigzag_schedule_1 = [
        {'day': 'Sunday', 'mild_weight_loss': maintain_weight, 'weight_loss': maintain_weight, 'extreme_weight_loss': maintain_weight},
        {'day': 'Monday', 'mild_weight_loss': int(maintain_weight * 0.9), 'weight_loss': int(maintain_weight * 0.8), 'extreme_weight_loss': int(maintain_weight * 0.61)},
        {'day': 'Tuesday', 'mild_weight_loss': int(maintain_weight * 0.9), 'weight_loss': int(maintain_weight * 0.8), 'extreme_weight_loss': int(maintain_weight * 0.61)},
        {'day': 'Wednesday', 'mild_weight_loss': int(maintain_weight * 0.9), 'weight_loss': int(maintain_weight * 0.8), 'extreme_weight_loss': int(maintain_weight * 0.61)},
        {'day': 'Thursday', 'mild_weight_loss': int(maintain_weight * 0.9), 'weight_loss': int(maintain_weight * 0.8), 'extreme_weight_loss': int(maintain_weight * 0.61)},
        {'day': 'Friday', 'mild_weight_loss': int(maintain_weight * 0.9), 'weight_loss': int(maintain_weight * 0.8), 'extreme_weight_loss': int(maintain_weight * 0.61)},
        {'day': 'Saturday', 'mild_weight_loss': maintain_weight, 'weight_loss': maintain_weight, 'extreme_weight_loss': maintain_weight},
    ]

    return render(request, 'calorie_results.html', {
        'calculated_calories': calculated_calories,
        'zigzag_schedule_1': zigzag_schedule_1,
    })

def search_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        nutritionix_api_url = 'https://trackapi.nutritionix.com/v2/search/instant'
        nutritionix_headers = {
            'x-app-id': '13488eb7',
            'x-app-key': '384e715b18d52e9de03d6e5134943ea6',
        }
        nutritionix_params = {
            'query': query,
            'self': True,
            'branded': True,
        }

        try:
            response = requests.get(nutritionix_api_url, headers=nutritionix_headers, params=nutritionix_params)
            response.raise_for_status()
            suggestions = response.json()
            results = []
            if 'common' in suggestions:
                results.extend([{'name': item['food_name'], 'image': item['photo']['thumb']} for item in suggestions['common']])
            if 'branded' in suggestions:
                results.extend([{'name': item['food_name'], 'image': item['photo']['thumb']} for item in suggestions['branded']])
        except requests.exceptions.RequestException as e:
            print(e)
            results = []

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)

def fetch_food_details(request):
    food_name = request.GET.get('food_name', '')
    if food_name:
        nutritionix_api_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
        nutritionix_headers = {
            'x-app-id': '13488eb7',
            'x-app-key': '384e715b18d52e9de03d6e5134943ea6',
            'Content-Type': 'application/json'
        }
        nutritionix_data_payload = {
            'query': food_name,
            'num_servings': 1
        }

        try:
            nutritionix_response = requests.post(nutritionix_api_url, headers=nutritionix_headers, json=nutritionix_data_payload)
            nutritionix_response.raise_for_status()
            nutritionix_data = nutritionix_response.json()

            if nutritionix_data and 'foods' in nutritionix_data:
                food = nutritionix_data['foods'][0]
                return JsonResponse({
                    'food_name': food['food_name'],
                    'calories': food['nf_calories'],
                    'protein': food['nf_protein'],
                    'carbohydrates': food['nf_total_carbohydrate'],
                    'fat': food['nf_total_fat']
                })
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Food not found'}, status=404)

@login_required
def diary(request, date=None):
    if 'date' in request.GET:
        selected_date_str = request.GET['date']
    else:
        selected_date_str = date or dt_date.today().strftime('%Y-%m-%d')
    
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    
    if request.method == 'POST':
        entry_date = selected_date  # Set the entry date initially to the selected date
        if 'date' in request.POST:
            entry_date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        
        if 'daily_goal' in request.POST:
            daily_goal = request.POST.get('daily_goal')
            CalorieGoal.objects.update_or_create(user=request.user, date_set=entry_date, defaults={'goal': daily_goal})
        elif 'food_name' in request.POST:
            food_name = request.POST.get('food_name')
            calories = request.POST.get('calories')
            protein = request.POST.get('protein')
            carbohydrates = request.POST.get('carbohydrates')
            fat = request.POST.get('fat')
            category = request.POST.get('category')
            entry_id = request.POST.get('entry_id', None)
            
            if entry_id:
                entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
                entry.food_name = food_name
                entry.calories = calories
                entry.protein = protein
                entry.carbohydrates = carbohydrates
                entry.fat = fat
                entry.category = category
                entry.date = entry_date
                entry.save()
            else:
                DiaryEntry.objects.create(
                    user=request.user,
                    food_name=food_name,
                    calories=calories,
                    protein=protein,
                    carbohydrates=carbohydrates,
                    fat=fat,
                    category=category,
                    date=entry_date
                )
        
        return redirect('diary_with_date', date=entry_date.strftime('%Y-%m-%d'))
    
    saved_entries = SavedEntry.objects.filter(user=request.user)
    diary_entries = DiaryEntry.objects.filter(user=request.user, date=selected_date)
    total_consumed_calories = sum(entry.calories for entry in diary_entries)
    total_protein = sum(entry.protein for entry in diary_entries)
    total_carbohydrates = sum(entry.carbohydrates for entry in diary_entries)
    total_fat = sum(entry.fat for entry in diary_entries)
    
    try:
        calorie_goal = CalorieGoal.objects.filter(user=request.user, date_set=selected_date).latest('date_set').goal
    except CalorieGoal.DoesNotExist:
        calorie_goal = 0
    
    remaining_calories = calorie_goal - total_consumed_calories
    consumed_percentage = (total_consumed_calories / calorie_goal) * 100 if calorie_goal else 0
    remaining_percentage = 100 - consumed_percentage if calorie_goal else 0

    categories = ['uncategorized', 'breakfast', 'lunch', 'dinner', 'snacks']
    
    return render(request, 'diary.html', {
        'diary_entries': diary_entries,
        'total_consumed_calories': total_consumed_calories,
        'total_protein': total_protein,
        'total_carbohydrates': total_carbohydrates,
        'total_fat': total_fat,
        'calorie_goal': calorie_goal,
        'remaining_calories': remaining_calories,
        'consumed_percentage': consumed_percentage,
        'remaining_percentage': remaining_percentage,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'categories': categories,
        'saved_entries': saved_entries,
    })

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    entry.delete()
    return redirect('diary')

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.food_name = request.POST.get('food_name')
        entry.calories = request.POST.get('calories')
        entry.protein = request.POST.get('protein')
        entry.carbohydrates = request.POST.get('carbohydrates')
        entry.fat = request.POST.get('fat')
        entry.category = request.POST.get('category')
        entry.date = request.POST.get('date', timezone.now())
        entry.save()
        return redirect('diary')
    return render(request, 'edit_entry.html', {'entry': entry})

@login_required
def get_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    return JsonResponse({
        'food_name': entry.food_name,
        'calories': entry.calories,
        'protein': entry.protein,
        'carbohydrates': entry.carbohydrates,
        'fat': entry.fat,
        'category': entry.category,
        'date': entry.date
    })

@login_required
def diary_search_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        nutritionix_api_url = 'https://trackapi.nutritionix.com/v2/search/instant'
        nutritionix_headers = {
            'x-app-id': '13488eb7',
            'x-app-key': '384e715b18d52e9de03d6e5134943ea6',
        }
        nutritionix_params = {
            'query': query,
            'self': True,
            'branded': True,
        }

        try:
            response = requests.get(nutritionix_api_url, headers=nutritionix_headers, params=nutritionix_params)
            response.raise_for_status()
            suggestions = response.json()
            results = []
            if 'common' in suggestions:
                results.extend([{'name': item['food_name'], 'image': item['photo']['thumb']} for item in suggestions['common']])
            if 'branded' in suggestions:
                results.extend([{'name': item['food_name'], 'image': item['photo']['thumb']} for item in suggestions['branded']])
        except requests.exceptions.RequestException as e:
            print(e)
            results = []

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)

@login_required
def save_entry(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        SavedEntry.objects.create(
            user=request.user,
            food_name=data['food_name'],
            calories=data['calories'],
            protein=data['protein'],
            carbohydrates=data['carbohydrates'],
            fat=data['fat']
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def delete_saved_entry(request, entry_id):
    try:
        entry = SavedEntry.objects.get(id=entry_id, user=request.user)
        entry.delete()
        return JsonResponse({'status': 'success'})
    except SavedEntry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Entry not found'}, status=404)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def settings_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Redirect to the same page after saving the form
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'settings.html', {'form': form})

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)