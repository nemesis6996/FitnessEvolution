import os
import json
import streamlit as st
from openai import OpenAI

# Get API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your_openai_api_key")
openai = OpenAI(api_key=OPENAI_API_KEY)

def get_ai_recommendation(user_data):
    """Get AI-powered workout recommendations based on user data"""
    # If no API key is available, return a default recommendation
    if OPENAI_API_KEY == "your_openai_api_key":
        return generate_default_recommendation(user_data)
    
    try:
        # Prepare the prompt with user data
        prompt = f"""
        Generate a personalized fitness recommendation for a user with the following profile:
        - Experience level: {user_data.get('experience_level', 'Beginner')}
        - Height: {user_data.get('height', 175)} cm
        - Weight: {user_data.get('weight', 75)} kg
        - Goals: {', '.join(user_data.get('goals', ['General fitness']))}
        
        Provide a brief, specific recommendation focused on their next workout or exercise suggestion.
        Keep it under 100 words and make it motivational yet practical. 
        Format as a simple paragraph that's ready to display to the user.
        """
        
        # Call OpenAI API to get recommendation
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional fitness coach providing personalized advice."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"AI recommendation error: {str(e)}")
        return generate_default_recommendation(user_data)

def generate_default_recommendation(user_data):
    """Generate a default recommendation when OpenAI API is not available"""
    experience = user_data.get('experience_level', 'Beginner')
    goals = user_data.get('goals', ['General fitness'])
    
    if 'Beginner' in experience:
        return "Start with a full-body workout 3 times this week. Focus on form rather than weight or reps. Try the Beginner Full Body template and complement it with 20 minutes of light cardio on rest days."
    
    elif 'Intermediate' in experience:
        if 'Muscle gain' in goals:
            return "Consider a push/pull/legs split for your next workout cycle. Increase protein intake to 1.6-2g per kg of bodyweight and ensure progressive overload in your key lifts."
        else:
            return "Mix in some HIIT workouts with your strength training to maximize calorie burn and cardiovascular health. Aim for 4-5 sessions this week with proper recovery between workouts."
    
    else:  # Advanced
        return "It's time to add some variety to challenge your muscles in new ways. Try incorporating drop sets or supersets in your next workout. Consider a deload week if you've been pushing hard for more than 8 weeks."

def get_workout_suggestion(user_data, goal):
    """Get AI-suggested workout based on user data and specified goal"""
    # If no API key is available, return a default suggestion
    if OPENAI_API_KEY == "your_openai_api_key":
        return generate_default_workout(user_data, goal)
    
    try:
        # Prepare the prompt with user data
        prompt = f"""
        Create a personalized workout plan for a user with the following profile:
        - Experience level: {user_data.get('experience_level', 'Beginner')}
        - Height: {user_data.get('height', 175)} cm
        - Weight: {user_data.get('weight', 75)} kg
        - Goal: {goal}
        
        Provide a structured workout plan that includes:
        1. Name of the workout
        2. Brief description
        3. Duration (in minutes)
        4. A list of 4-6 exercises with sets and reps
        
        Return the response as JSON in the following format:
        {{
            "name": "Workout Name",
            "description": "Brief description",
            "duration": number_of_minutes,
            "exercises": [
                {{"name": "Exercise 1", "sets": 3, "reps": "8-10", "rest": 60}},
                ...
            ]
        }}
        """
        
        # Call OpenAI API to get workout suggestion
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional fitness coach providing personalized workout plans."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=500
        )
        
        # Parse the JSON response
        workout_plan = json.loads(response.choices[0].message.content)
        return workout_plan
        
    except Exception as e:
        st.error(f"AI workout suggestion error: {str(e)}")
        return generate_default_workout(user_data, goal)

def generate_default_workout(user_data, goal):
    """Generate a default workout when OpenAI API is not available"""
    experience = user_data.get('experience_level', 'Beginner')
    
    if goal.lower() == "strength":
        if 'Beginner' in experience:
            return {
                "name": "Beginner Strength Foundation",
                "description": "A simple full-body workout to build baseline strength",
                "duration": 45,
                "exercises": [
                    {"name": "Bodyweight Squat", "sets": 3, "reps": "10-12", "rest": 60},
                    {"name": "Push-ups", "sets": 3, "reps": "8-10", "rest": 60},
                    {"name": "Dumbbell Rows", "sets": 3, "reps": "10 each side", "rest": 60},
                    {"name": "Plank", "sets": 3, "reps": "30 seconds", "rest": 45}
                ]
            }
        else:
            return {
                "name": "Intermediate Strength Builder",
                "description": "A challenging strength workout with progressive overload",
                "duration": 60,
                "exercises": [
                    {"name": "Barbell Squat", "sets": 4, "reps": "6-8", "rest": 90},
                    {"name": "Bench Press", "sets": 4, "reps": "6-8", "rest": 90},
                    {"name": "Deadlift", "sets": 3, "reps": "5", "rest": 120},
                    {"name": "Pull-ups", "sets": 3, "reps": "8-10", "rest": 90},
                    {"name": "Military Press", "sets": 3, "reps": "8-10", "rest": 90}
                ]
            }
    
    elif goal.lower() == "cardio":
        return {
            "name": "Heart-Pumping Cardio",
            "description": "A mixed cardio session to improve endurance",
            "duration": 30,
            "exercises": [
                {"name": "Jump Rope", "sets": 1, "reps": "3 minutes", "rest": 60},
                {"name": "Jumping Jacks", "sets": 3, "reps": "30 seconds", "rest": 30},
                {"name": "High Knees", "sets": 3, "reps": "30 seconds", "rest": 30},
                {"name": "Burpees", "sets": 3, "reps": "10", "rest": 60},
                {"name": "Mountain Climbers", "sets": 3, "reps": "30 seconds", "rest": 30}
            ]
        }
    
    else:  # Weight loss or general
        return {
            "name": "Full Body Fat Burner",
            "description": "A balanced workout to burn calories and maintain muscle",
            "duration": 45,
            "exercises": [
                {"name": "Bodyweight Squats", "sets": 3, "reps": "15", "rest": 45},
                {"name": "Push-ups", "sets": 3, "reps": "10", "rest": 45},
                {"name": "Walking Lunges", "sets": 2, "reps": "10 each leg", "rest": 45},
                {"name": "Plank", "sets": 3, "reps": "30 seconds", "rest": 30},
                {"name": "Mountain Climbers", "sets": 3, "reps": "20 each leg", "rest": 30}
            ]
        }
