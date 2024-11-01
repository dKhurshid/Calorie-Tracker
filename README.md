Calorie Tracking App
A user-focused calorie tracking application designed to help users set and manage their daily calorie intake goals, record food entries, and track nutrition with ease. Built with Django and integrated with the API Ninjas nutrition database, this app provides users with a straightforward way to monitor their daily food intake and maintain dietary goals.

Features
User Authentication: Secure registration and login with JWT tokens for personalized user sessions.
Custom Food Entries: Users can add food items manually with detailed calorie and nutrient information.
API Integration: Fetch accurate nutritional data by simply entering a food name, making tracking quick and easy.
Calorie Goals: Set personalized daily calorie goals and track progress throughout the day.
Daily Diary: Log daily meals and review calorie intake over time.
User-Specific Data: Each user has individual calorie goals and diary entries for tailored tracking.
Tech Stack
Backend: Django, SQLite for database management
Frontend: HTML, CSS, JavaScript for responsive and intuitive user interfaces
API: API Ninjas for fetching nutrition data
Authentication: JWT tokens for secure user authentication
Getting Started
Prerequisites
Python 3.x installed
Virtual environment (recommended)
Installation
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/calorie-tracking-app.git
cd calorie-tracking-app
Set Up Virtual Environment (optional but recommended)

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Set Up the Database

bash
Copy code
python manage.py migrate
Run the Application

bash
Copy code
python manage.py runserver
Access the App
Open your browser and go to http://127.0.0.1:8000/

Usage
Sign Up to create a new account or Log In to an existing account.
Set Your Calorie Goal in the profile section.
Add Food Entries manually or use the API Search to get detailed nutritional information.
Log Daily Meals and track your calorie intake throughout the day.
Future Enhancements
Integrate additional nutrition APIs to expand food database options.
Add visualizations for daily, weekly, and monthly calorie intake.
Implement meal categorization (e.g., breakfast, lunch, dinner).
Add a feature for tracking exercise and calories burned.
Contributing
Feel free to contribute by forking this repository, making changes, and submitting a pull request. Suggestions for new features and improvements are always welcome!
