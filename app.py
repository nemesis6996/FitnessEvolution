import streamlit as st
import os
import sys
from PIL import Image
import base64
from io import BytesIO

# Add the directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import utilities
from utils.database import initialize_database, get_exercise_categories, get_exercises_by_category
from utils.ai_helper import get_ai_recommendation
from utils.avatar import get_avatar_placeholder

# Set page configuration
st.set_page_config(
    page_title="NF Fitness App",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states if not already done
if 'user' not in st.session_state:
    st.session_state.user = {
        'logged_in': False,
        'username': '',
        'height': 175,  # cm
        'weight': 75,   # kg
        'goals': [],
        'experience_level': 'Beginner'
    }

if 'workout_plan' not in st.session_state:
    st.session_state.workout_plan = []

# Initialize database on app start
initialize_database()

# Sidebar for navigation
with st.sidebar:
    st.image("assets/logo.svg", width=150)
    st.title("NF Fitness")
    
    # Login/profile section in sidebar
    if not st.session_state.user['logged_in']:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                # Simple mock login for demo purposes
                if username and password:
                    st.session_state.user['logged_in'] = True
                    st.session_state.user['username'] = username
                    st.rerun()
                else:
                    st.error("Please enter username and password")
        
        with col2:
            if st.button("Sign Up"):
                st.info("Sign up functionality would be implemented in a production app")
    
    else:
        st.success(f"Logged in as {st.session_state.user['username']}")
        if st.button("Logout"):
            st.session_state.user['logged_in'] = False
            st.rerun()
    
    st.divider()
    
    # Main navigation
    st.subheader("Navigation")
    selected = st.radio(
        "Go to",
        ["Home", "Exercises", "Workout Plans", "My Profile", "Progress Tracking", "Admin Panel"],
        index=0
    )

# Main content based on selection
if selected == "Home":
    st.title("Welcome to NF Fitness")
    
    # Main columns for home page
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## AI-Powered Fitness Coach
        
        NF Fitness helps you achieve your fitness goals with:
        
        - **Comprehensive Exercise Database** - Detailed instructions and visual guides
        - **Smart Workout Plans** - Personalized for your goals
        - **3D Avatar Visualization** - Track your body transformation
        - **AI Recommendations** - Get personalized advice
        
        Get started by exploring exercises or creating a workout plan!
        """)
        
        # Featured workout section
        st.subheader("Featured Workout Plan")
        featured_workout = {
            "name": "Full Body Strength",
            "difficulty": "Intermediate",
            "duration": "45 minutes",
            "exercises": ["Barbell Squat", "Bench Press", "Deadlift", "Pull-ups", "Overhead Press"]
        }
        
        with st.expander("Full Body Strength Workout", expanded=True):
            st.write(f"**Difficulty:** {featured_workout['difficulty']}")
            st.write(f"**Duration:** {featured_workout['duration']}")
            st.write("**Exercises:**")
            for exercise in featured_workout['exercises']:
                st.write(f"- {exercise}")
            
            if st.button("Add to My Workouts"):
                if st.session_state.user['logged_in']:
                    st.session_state.workout_plan.append(featured_workout)
                    st.success("Workout added to your plan!")
                else:
                    st.warning("Please log in to save workouts")
    
    with col2:
        # Avatar preview
        st.subheader("Your Avatar")
        
        if st.session_state.user['logged_in']:
            st.markdown(get_avatar_placeholder(), unsafe_allow_html=True)
            st.caption("Avatar updates as you progress")
        else:
            st.info("Log in to see your fitness avatar")
        
        # AI recommendation section
        st.subheader("AI Recommendation")
        if st.session_state.user['logged_in']:
            with st.spinner("Getting personalized recommendations..."):
                recommendation = get_ai_recommendation(st.session_state.user)
                st.info(recommendation)
        else:
            st.info("Log in to get personalized AI recommendations")
    
    # Featured exercise categories
    st.subheader("Explore Exercise Categories")
    categories = get_exercise_categories()
    
    # Display categories in a grid
    cols = st.columns(3)
    for i, category in enumerate(categories[:6]):  # Show first 6 categories
        with cols[i % 3]:
            st.markdown(f"### {category}")
            # Show a sample exercise from this category
            exercises = get_exercises_by_category(category)
            if exercises:
                sample = exercises[0]
                st.write(f"**{sample['name']}**")
                st.write(sample['short_description'])
                if st.button(f"Explore {category}", key=f"cat_{i}"):
                    st.session_state.selected_category = category
                    st.rerun()
    
    # Testimonials
    st.divider()
    st.subheader("User Success Stories")
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        #### "Lost 15kg in 3 months"
        
        The custom workout plans and progress tracking helped me stay motivated.
        
        *- Alex M.*
        """)
    
    with cols[1]:
        st.markdown("""
        #### "Finally building muscle"
        
        The exercise instructions and form guidelines were game-changing for my technique.
        
        *- Jamie K.*
        """)
    
    with cols[2]:
        st.markdown("""
        #### "Perfect for beginners"
        
        The AI coach answered all my questions and kept me on track.
        
        *- Taylor S.*
        """)

elif selected == "Exercises":
    import pages.exercises
    pages.exercises.show()

elif selected == "Workout Plans":
    import pages.workout_plans
    pages.workout_plans.show()

elif selected == "My Profile":
    import pages.profile
    pages.profile.show()

elif selected == "Progress Tracking":
    import pages.progress
    pages.progress.show()

elif selected == "Admin Panel":
    import pages.admin
    pages.admin.show()

# Footer
st.divider()
st.caption("© 2023 NF Fitness - AI-Powered Fitness Application")
