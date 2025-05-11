import streamlit as st
import pandas as pd
from utils.database import get_exercise_categories, get_exercises_by_category, get_all_exercises

def show():
    st.title("Exercise Database")
    
    # Search box
    search_query = st.text_input("Search exercises", placeholder="Enter exercise name, muscle group, or equipment")
    
    # Category filter
    categories = get_exercise_categories()
    selected_category = st.selectbox(
        "Filter by category",
        ["All Categories"] + categories
    )
    
    # Difficulty filter
    difficulties = ["All Levels", "Beginner", "Intermediate", "Advanced"]
    selected_difficulty = st.selectbox(
        "Filter by difficulty",
        difficulties
    )
    
    # Get exercises based on filters
    if selected_category == "All Categories":
        exercises = get_all_exercises()
    else:
        exercises = get_exercises_by_category(selected_category)
    
    # Filter by difficulty if not "All Levels"
    if selected_difficulty != "All Levels":
        exercises = [ex for ex in exercises if ex['difficulty'] == selected_difficulty]
    
    # Filter by search query if provided
    if search_query:
        # Convert to lowercase for case-insensitive search
        query = search_query.lower()
        filtered_exercises = []
        
        for ex in exercises:
            # Check if query appears in various fields
            if (query in ex['name'].lower() or 
                query in ex.get('muscles_targeted', '').lower() or 
                query in ex.get('equipment', '').lower() or 
                query in ex.get('description', '').lower()):
                filtered_exercises.append(ex)
        
        exercises = filtered_exercises
    
    # Display number of exercises found
    st.write(f"{len(exercises)} exercises found")
    
    # Display exercises
    if not exercises:
        st.info("No exercises match your criteria. Try adjusting your filters.")
    else:
        # Display exercises in a grid layout
        cols_per_row = 2
        rows = (len(exercises) + cols_per_row - 1) // cols_per_row  # Ceiling division
        
        for row in range(rows):
            cols = st.columns(cols_per_row)
            for col in range(cols_per_row):
                index = row * cols_per_row + col
                if index < len(exercises):
                    exercise = exercises[index]
                    with cols[col]:
                        with st.expander(f"**{exercise['name']}**", expanded=False):
                            if exercise.get('image_url'):
                                st.image(exercise['image_url'], use_column_width=True)
                            
                            st.markdown(f"**Difficulty:** {exercise.get('difficulty', 'Not specified')}")
                            st.markdown(f"**Category:** {exercise.get('category_name', 'Not categorized')}")
                            st.markdown(f"**Equipment:** {exercise.get('equipment', 'None required')}")
                            st.markdown(f"**Muscles:** {exercise.get('muscles_targeted', 'Not specified')}")
                            
                            st.markdown("### Description")
                            st.write(exercise.get('description', 'No description available.'))
                            
                            st.markdown("### Instructions")
                            instructions = exercise.get('instructions', 'No instructions available.')
                            # Split instructions by newlines and format as a numbered list
                            if '\n' in instructions:
                                inst_list = instructions.split('\n')
                                for i, inst in enumerate(inst_list, 1):
                                    if inst.strip():  # Skip empty lines
                                        st.write(f"{inst}")
                            else:
                                st.write(instructions)
                            
                            if exercise.get('tips'):
                                st.markdown("### Tips")
                                st.write(exercise.get('tips'))
                            
                            # Add to Workout button
                            if st.button("Add to Workout", key=f"add_{exercise['id']}"):
                                if 'workout_builder' not in st.session_state:
                                    st.session_state.workout_builder = []
                                
                                # Check if exercise already in workout builder
                                existing_ids = [ex['id'] for ex in st.session_state.workout_builder]
                                if exercise['id'] not in existing_ids:
                                    st.session_state.workout_builder.append(exercise)
                                    st.success(f"{exercise['name']} added to workout builder")
                                else:
                                    st.info(f"{exercise['name']} is already in your workout")
    
    # Workout Builder section
    if 'workout_builder' in st.session_state and st.session_state.workout_builder:
        st.divider()
        st.subheader("Workout Builder")
        st.write(f"{len(st.session_state.workout_builder)} exercises in your workout")
        
        # Display selected exercises in a table
        workout_data = []
        for ex in st.session_state.workout_builder:
            workout_data.append({
                "Exercise": ex['name'],
                "Category": ex.get('category_name', ''),
                "Difficulty": ex.get('difficulty', ''),
                "Remove": ex['id']
            })
        
        df = pd.DataFrame(workout_data)
        
        # Display the workout table
        for i, row in df.iterrows():
            cols = st.columns([3, 2, 2, 1])
            with cols[0]:
                st.write(row["Exercise"])
            with cols[1]:
                st.write(row["Category"])
            with cols[2]:
                st.write(row["Difficulty"])
            with cols[3]:
                if st.button("❌", key=f"remove_{row['Remove']}"):
                    st.session_state.workout_builder = [
                        ex for ex in st.session_state.workout_builder if ex['id'] != row['Remove']
                    ]
                    st.rerun()
        
        # Buttons for workout actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Workout"):
                if st.session_state.user['logged_in']:
                    st.info("Save functionality would save this workout to your account")
                else:
                    st.warning("Please log in to save workouts")
        
        with col2:
            if st.button("Clear Workout"):
                st.session_state.workout_builder = []
                st.rerun()
