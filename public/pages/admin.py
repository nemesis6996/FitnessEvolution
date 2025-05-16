import streamlit as st
import pandas as pd
import random
import plotly.express as px
from utils.database import (
    get_all_exercises, 
    get_exercise_categories, 
    add_exercise, 
    get_workout_templates,
    add_workout_template,
    add_workout_exercise
)

def show():
    st.title("Pannello Amministratore")
    
    # Check if user is admin
    is_admin = st.session_state.user.get('logged_in', False) and st.session_state.user.get('username', '') == 'admin'
    
    if not is_admin:
        st.warning("Devi effettuare l'accesso come amministratore per accedere a questa pagina.")
        return
    
    # Admin tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Gestione Esercizi", "Schede di Allenamento", "Gestione Utenti", "Statistiche"])
    
    # Tab 1: Exercise Management
    with tab1:
        st.subheader("Exercise Database Management")
        
        # Sub-tabs for viewing and adding exercises
        subtab1, subtab2 = st.tabs(["View Exercises", "Add Exercise"])
        
        with subtab1:
            # Get all exercises
            exercises = get_all_exercises()
            
            if exercises:
                # Convert to DataFrame for display
                df = pd.DataFrame(exercises)
                
                # Select columns to display
                display_cols = ['id', 'name', 'category_name', 'difficulty', 'equipment']
                df_display = df[display_cols]
                
                # Display table
                st.dataframe(df_display, use_container_width=True)
                
                # Exercise detail view
                st.subheader("Exercise Details")
                
                # Select exercise to view
                selected_id = st.selectbox(
                    "Select exercise to view details",
                    df['id'].tolist(),
                    format_func=lambda x: df.loc[df['id'] == x, 'name'].iloc[0]
                )
                
                # Get selected exercise
                selected_exercise = df[df['id'] == selected_id].iloc[0]
                
                # Display exercise details
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {selected_exercise['name']}")
                    st.markdown(f"**Category:** {selected_exercise['category_name']}")
                    st.markdown(f"**Difficulty:** {selected_exercise['difficulty']}")
                    st.markdown(f"**Equipment:** {selected_exercise['equipment']}")
                    st.markdown(f"**Muscles Targeted:** {selected_exercise['muscles_targeted']}")
                    
                    st.markdown("### Description")
                    st.write(selected_exercise['description'])
                    
                    st.markdown("### Instructions")
                    instructions = selected_exercise['instructions']
                    if '\n' in instructions:
                        for line in instructions.split('\n'):
                            st.write(line)
                    else:
                        st.write(instructions)
                    
                    if selected_exercise['tips']:
                        st.markdown("### Tips")
                        st.write(selected_exercise['tips'])
                
                with col2:
                    if selected_exercise['image_url']:
                        st.image(selected_exercise['image_url'], use_column_width=True)
                
                # Edit button (in a real app, this would open an edit form)
                if st.button("Edit Exercise"):
                    st.info("In a complete app, this would open an edit form for this exercise.")
            
            else:
                st.info("No exercises found in the database.")
        
        with subtab2:
            # Form for adding new exercise
            st.subheader("Add New Exercise")
            
            with st.form("add_exercise_form"):
                # Basic information
                name = st.text_input("Exercise Name")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get categories for dropdown
                    categories = get_exercise_categories()
                    category_name = st.selectbox("Category", categories)
                    
                    # Convert category name to ID (simplified)
                    category_id = categories.index(category_name) + 1
                    
                    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
                
                with col2:
                    equipment = st.text_input("Equipment", placeholder="e.g., Dumbbells, Barbell, None")
                    muscles_targeted = st.text_input("Muscles Targeted", placeholder="e.g., Chest, Triceps, Shoulders")
                
                # Descriptions
                st.subheader("Descriptions")
                short_description = st.text_input("Short Description", placeholder="Brief summary of the exercise")
                description = st.text_area("Full Description", placeholder="Detailed description of the exercise and its benefits")
                
                # Instructions and tips
                st.subheader("Instructions & Tips")
                instructions = st.text_area("Instructions", placeholder="Step-by-step instructions for performing the exercise")
                tips = st.text_area("Tips", placeholder="Form tips, common mistakes to avoid, etc.")
                
                # Media URLs
                st.subheader("Media")
                image_url = st.text_input("Image URL", placeholder="URL to an image of the exercise")
                video_url = st.text_input("Video URL (optional)", placeholder="URL to a demonstration video")
                
                # Submit button
                submitted = st.form_submit_button("Add Exercise")
                if submitted:
                    # Validate required fields
                    if not name or not category_id or not difficulty or not description or not instructions:
                        st.error("Please fill in all required fields")
                    else:
                        # In a real app, this would add to the database
                        # add_exercise(name, category_id, difficulty, equipment, muscles_targeted,
                        #             description, short_description, instructions, tips, image_url, video_url)
                        st.success(f"Exercise '{name}' added successfully!")
    
    # Tab 2: Workout Plans Management
    with tab2:
        st.subheader("Workout Plans Management")
        
        # Sub-tabs for viewing and adding workout plans
        subtab1, subtab2 = st.tabs(["View Workout Plans", "Add Workout Plan"])
        
        with subtab1:
            # Get all workout templates
            templates = get_workout_templates()
            
            if templates:
                # Convert to DataFrame for display
                df = pd.DataFrame(templates)
                
                # Display table
                st.dataframe(df[['id', 'name', 'difficulty', 'duration', 'goal']], use_container_width=True)
                
                # Workout plan detail view
                st.subheader("Workout Plan Details")
                
                # Select workout to view
                selected_id = st.selectbox(
                    "Select workout to view details",
                    df['id'].tolist(),
                    format_func=lambda x: df.loc[df['id'] == x, 'name'].iloc[0],
                    key="view_workout_select"
                )
                
                # Get selected workout
                selected_workout = df[df['id'] == selected_id].iloc[0]
                
                # Display workout details
                st.markdown(f"### {selected_workout['name']}")
                st.markdown(f"**Difficulty:** {selected_workout['difficulty']}")
                st.markdown(f"**Duration:** {selected_workout['duration']} minutes")
                st.markdown(f"**Goal:** {selected_workout['goal']}")
                
                if selected_workout['description']:
                    st.markdown("### Description")
                    st.write(selected_workout['description'])
                
                # In a real app, this would fetch and display the exercises for this workout
                st.markdown("### Exercises")
                st.info("In a complete app, this would display the exercises for this workout.")
                
                # Edit button (in a real app, this would open an edit form)
                if st.button("Edit Workout Plan"):
                    st.info("In a complete app, this would open an edit form for this workout plan.")
            
            else:
                st.info("No workout plans found in the database.")
        
        with subtab2:
            # Form for adding new workout plan
            st.subheader("Add New Workout Plan")
            
            with st.form("add_workout_form"):
                # Basic information
                name = st.text_input("Workout Name")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
                    duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=45)
                
                with col2:
                    goal = st.text_input("Primary Goal", placeholder="e.g., Strength, Cardio, Weight Loss")
                    is_public = st.checkbox("Public Workout (available to all users)", value=True)
                
                # Description
                description = st.text_area("Description", placeholder="Detailed description of the workout plan")
                
                # Submit button
                submitted = st.form_submit_button("Add Workout Plan")
                if submitted:
                    # Validate required fields
                    if not name or not difficulty or not goal:
                        st.error("Please fill in all required fields")
                    else:
                        # In a real app, this would add to the database
                        # workout_id = add_workout_template(name, description, difficulty, duration, goal, 1, is_public)
                        st.success(f"Workout Plan '{name}' added successfully!")
                        
                        # In a real app, this would then redirect to a page to add exercises to the workout
                        st.info("Next step would be to add exercises to this workout plan.")
    
    # Tab 3: User Management
    with tab3:
        st.subheader("User Management")
        
        # In a real app, this would fetch users from the database
        # For demo, create sample user data
        users = [
            {"id": 1, "username": "admin", "email": "admin@nffitness.com", "first_name": "Admin", "last_name": "User", "is_admin": True},
            {"id": 2, "username": "user", "email": "user@example.com", "first_name": "Sample", "last_name": "User", "is_admin": False},
            {"id": 3, "username": "john_doe", "email": "john@example.com", "first_name": "John", "last_name": "Doe", "is_admin": False},
            {"id": 4, "username": "jane_smith", "email": "jane@example.com", "first_name": "Jane", "last_name": "Smith", "is_admin": False}
        ]
        
        # Convert to DataFrame for display
        users_df = pd.DataFrame(users)
        
        # Display users table
        st.dataframe(users_df, use_container_width=True)
        
        # User detail/edit view
        st.subheader("User Details")
        
        # Select user to view
        selected_user_id = st.selectbox(
            "Select user to view/edit",
            [u["id"] for u in users],
            format_func=lambda x: next((u["username"] for u in users if u["id"] == x), "")
        )
        
        # Get selected user
        selected_user = next((u for u in users if u["id"] == selected_user_id), None)
        
        if selected_user:
            # Display user details with editable fields
            with st.form("edit_user_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    username = st.text_input("Username", value=selected_user["username"])
                    email = st.text_input("Email", value=selected_user["email"])
                
                with col2:
                    first_name = st.text_input("First Name", value=selected_user["first_name"])
                    last_name = st.text_input("Last Name", value=selected_user["last_name"])
                
                is_admin = st.checkbox("Administrator", value=selected_user["is_admin"])
                
                # Submit button
                submitted = st.form_submit_button("Update User")
                if submitted:
                    st.success(f"User '{username}' updated successfully!")
            
            # Delete user button
            if st.button("Delete User"):
                st.warning(f"Are you sure you want to delete user '{selected_user['username']}'?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, Delete"):
                        st.success(f"User '{selected_user['username']}' deleted successfully!")
                with col2:
                    if st.button("Cancel"):
                        st.info("Deletion cancelled.")
    
    # Tab 4: Statistics and Analytics
    with tab4:
        st.subheader("Application Statistics")
        
        # Create some example stats for demonstration
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", "43", "+5")
        
        with col2:
            st.metric("Active Workouts", "156", "+12")
        
        with col3:
            st.metric("Exercises", "95", "+8")
        
        with col4:
            st.metric("Workout Plans", "24", "+3")
        
        # User activity chart (example)
        st.subheader("User Activity")
        
        # Create sample data for user activity
        dates = pd.date_range(end=pd.Timestamp.now(), periods=30).strftime("%Y-%m-%d").tolist()
        active_users = [random.randint(5, 25) for _ in range(30)]
        new_users = [random.randint(0, 5) for _ in range(30)]
        
        # Create DataFrame
        activity_df = pd.DataFrame({
            "Date": dates,
            "Active Users": active_users,
            "New Registrations": new_users
        })
        
        # Plot with Plotly
        fig = px.line(
            activity_df,
            x="Date",
            y=["Active Users", "New Registrations"],
            title="User Activity (Last 30 Days)",
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Most popular exercises chart
        st.subheader("Most Popular Exercises")
        
        # Sample data for popular exercises
        popular_exercises = [
            {"name": "Bench Press", "usage_count": 158},
            {"name": "Squat", "usage_count": 145},
            {"name": "Deadlift", "usage_count": 132},
            {"name": "Plank", "usage_count": 124},
            {"name": "Running", "usage_count": 110},
            {"name": "Push-ups", "usage_count": 95},
            {"name": "Pull-ups", "usage_count": 89},
            {"name": "Jumping Rope", "usage_count": 75}
        ]
        
        # Convert to DataFrame
        popular_df = pd.DataFrame(popular_exercises)
        
        # Create bar chart
        fig = px.bar(
            popular_df,
            x="name",
            y="usage_count",
            title="Most Popular Exercises",
            labels={"name": "Exercise", "usage_count": "Usage Count"},
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # System health statistics
        st.subheader("System Health")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Server Uptime", "99.8%", "+0.2%")
        
        with col2:
            st.metric("Avg Response Time", "245ms", "-15ms")
        
        with col3:
            st.metric("Database Size", "1.2 GB", "+0.1 GB")
        
        # Add note about analytics functionality
        st.info("In a complete app, this section would include more detailed analytics, user behavior patterns, and performance metrics.")
