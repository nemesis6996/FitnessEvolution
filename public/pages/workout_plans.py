import streamlit as st
import pandas as pd
from utils.database import get_workout_templates, get_workout_exercises, get_workout_template, get_all_exercises
from utils.ai_helper import get_workout_suggestion

def show():
    st.title("Schede di Allenamento")
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Sfoglia Schede", "Crea Scheda Personalizzata", "Generatore Schede AI"])
    
    # Tab 1: Browse existing workout plans
    with tab1:
        st.subheader("Schede Predefinite")
        
        # Get all workout templates
        templates = get_workout_templates()
        
        # Filter controls
        col1, col2 = st.columns(2)
        with col1:
            # Filter by difficulty
            difficulty_map = {
                "Tutti i Livelli": "All Levels", 
                "Principiante": "Beginner", 
                "Intermedio": "Intermediate", 
                "Avanzato": "Advanced"
            }
            it_difficulties = ["Tutti i Livelli", "Principiante", "Intermedio", "Avanzato"]
            selected_it_difficulty = st.selectbox(
                "Filtra per difficoltà",
                it_difficulties,
                key="browse_difficulty"
            )
            selected_difficulty = difficulty_map[selected_it_difficulty]
        
        with col2:
            # Filter by goal
            goal_map = {
                "Tutti gli Obiettivi": "All Goals", 
                "Forza": "Strength", 
                "Cardio": "Cardio", 
                "Perdita Peso": "Weight Loss", 
                "Aumento Massa": "Muscle Gain", 
                "Core": "Core Strength"
            }
            it_goals = ["Tutti gli Obiettivi", "Forza", "Cardio", "Perdita Peso", "Aumento Massa", "Core"]
            selected_it_goal = st.selectbox(
                "Filtra per obiettivo",
                it_goals,
                key="browse_goal"
            )
            selected_goal = goal_map[selected_it_goal]
        
        # Apply filters
        filtered_templates = templates
        if selected_difficulty != "All Levels":
            filtered_templates = [t for t in filtered_templates if t['difficulty'] == selected_difficulty]
        
        if selected_goal != "All Goals":
            filtered_templates = [t for t in filtered_templates if selected_goal.lower() in t['goal'].lower()]
        
        # Display workouts in a grid
        if not filtered_templates:
            st.info("Nessuna scheda corrisponde ai tuoi filtri. Prova a modificare i criteri.")
        else:
            st.write(f"{len(filtered_templates)} schede trovate")
            
            for template in filtered_templates:
                # Traduciamo i nomi delle schede per la visualizzazione
                difficulty_it = {"Beginner": "Principiante", "Intermediate": "Intermedio", "Advanced": "Avanzato"}
                difficulty_display = difficulty_it.get(template['difficulty'], template['difficulty'])
                
                # Traduciamo gli obiettivi per la visualizzazione
                goal_it_rev = {v: k for k, v in goal_map.items() if v != "All Goals"}
                goal_display = goal_it_rev.get(template['goal'], template['goal'])
                
                with st.expander(f"**{template['name']}**", expanded=False):
                    st.write(f"**Difficoltà:** {difficulty_display}")
                    st.write(f"**Durata:** {template['duration']} minuti")
                    st.write(f"**Obiettivo:** {goal_display}")
                    st.write(f"**Descrizione:** {template['description']}")
                    
                    # Get exercises for this workout
                    exercises = get_workout_exercises(template['id'])
                    
                    # Display exercises in a table
                    st.subheader("Esercizi")
                    for i, exercise in enumerate(exercises, 1):
                        cols = st.columns([4, 1, 1, 2])
                        with cols[0]:
                            st.write(f"**{i}. {exercise['exercise_name']}**")
                        with cols[1]:
                            st.write(f"{exercise['sets']} serie")
                        with cols[2]:
                            st.write(f"{exercise['reps']} ripetizioni")
                        with cols[3]:
                            st.write(f"Riposo: {exercise['rest_time']}s")
                    
                    # Add to My Workouts button
                    if st.button("Aggiungi alle Mie Schede", key=f"add_workout_{template['id']}"):
                        if st.session_state.user['logged_in']:
                            # In a real app, this would save to the database
                            st.success(f"{template['name']} aggiunta alle tue schede!")
                        else:
                            st.warning("Effettua il login per salvare le schede")
    
    # Tab 2: Custom workout builder
    with tab2:
        st.subheader("Create Custom Workout Plan")
        
        # Initialize workout builder if not exists
        if 'custom_workout' not in st.session_state:
            st.session_state.custom_workout = {
                'name': '',
                'description': '',
                'difficulty': 'Beginner',
                'duration': 30,
                'goal': 'General Fitness',
                'exercises': []
            }
        
        # Workout details form
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.custom_workout['name'] = st.text_input(
                "Workout Name",
                value=st.session_state.custom_workout['name']
            )
            
            st.session_state.custom_workout['difficulty'] = st.selectbox(
                "Difficulty",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.custom_workout['difficulty'])
            )
            
            st.session_state.custom_workout['goal'] = st.selectbox(
                "Primary Goal",
                ["General Fitness", "Strength", "Muscle Gain", "Weight Loss", "Cardio", "Core Strength"],
                index=["General Fitness", "Strength", "Muscle Gain", "Weight Loss", "Cardio", "Core Strength"].index(st.session_state.custom_workout['goal'])
            )
        
        with col2:
            st.session_state.custom_workout['description'] = st.text_area(
                "Description",
                value=st.session_state.custom_workout['description'],
                height=100
            )
            
            st.session_state.custom_workout['duration'] = st.number_input(
                "Estimated Duration (minutes)",
                min_value=5,
                max_value=120,
                value=st.session_state.custom_workout['duration']
            )
        
        # Exercise selection
        st.subheader("Add Exercises")
        
        # Get all exercises for dropdown
        all_exercises = get_all_exercises()
        exercise_options = {f"{ex['name']} ({ex['category_name']})": ex['id'] for ex in all_exercises}
        
        # Create a form for adding exercises
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            selected_exercise = st.selectbox(
                "Select Exercise",
                list(exercise_options.keys())
            )
            selected_exercise_id = exercise_options[selected_exercise]
        
        with col2:
            sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
        
        with col3:
            reps = st.text_input("Reps", value="10")
        
        with col4:
            rest = st.number_input("Rest (sec)", min_value=0, max_value=180, value=60)
        
        # Add exercise button
        if st.button("Add Exercise"):
            # Find the exercise details
            exercise_details = next((ex for ex in all_exercises if ex['id'] == selected_exercise_id), None)
            
            if exercise_details:
                # Create exercise entry
                exercise_entry = {
                    'id': exercise_details['id'],
                    'name': exercise_details['name'],
                    'category': exercise_details.get('category_name', ''),
                    'sets': sets,
                    'reps': reps,
                    'rest': rest
                }
                
                # Add to workout
                st.session_state.custom_workout['exercises'].append(exercise_entry)
                st.success(f"Added {exercise_details['name']} to your workout")
                st.rerun()
        
        # Display current exercises in workout
        if st.session_state.custom_workout['exercises']:
            st.subheader("Current Workout Plan")
            
            for i, ex in enumerate(st.session_state.custom_workout['exercises']):
                cols = st.columns([3, 1, 1, 1, 1])
                with cols[0]:
                    st.write(f"**{i+1}. {ex['name']}**")
                with cols[1]:
                    st.write(f"{ex['sets']} sets")
                with cols[2]:
                    st.write(f"{ex['reps']} reps")
                with cols[3]:
                    st.write(f"{ex['rest']}s rest")
                with cols[4]:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.custom_workout['exercises'].pop(i)
                        st.rerun()
            
            # Reorder exercises
            if len(st.session_state.custom_workout['exercises']) > 1:
                st.subheader("Reorder Exercises")
                col1, col2 = st.columns(2)
                
                with col1:
                    move_exercise = st.selectbox(
                        "Select exercise to move",
                        [f"{i+1}. {ex['name']}" for i, ex in enumerate(st.session_state.custom_workout['exercises'])]
                    )
                    move_index = int(move_exercise.split('.')[0]) - 1
                
                with col2:
                    direction = st.radio(
                        "Move direction",
                        ["Up", "Down"],
                        horizontal=True
                    )
                    
                    if st.button("Move"):
                        if direction == "Up" and move_index > 0:
                            # Swap with previous exercise
                            st.session_state.custom_workout['exercises'][move_index], st.session_state.custom_workout['exercises'][move_index-1] = \
                                st.session_state.custom_workout['exercises'][move_index-1], st.session_state.custom_workout['exercises'][move_index]
                            st.rerun()
                        elif direction == "Down" and move_index < len(st.session_state.custom_workout['exercises'])-1:
                            # Swap with next exercise
                            st.session_state.custom_workout['exercises'][move_index], st.session_state.custom_workout['exercises'][move_index+1] = \
                                st.session_state.custom_workout['exercises'][move_index+1], st.session_state.custom_workout['exercises'][move_index]
                            st.rerun()
            
            # Save workout button
            if st.button("Save Workout Plan"):
                if not st.session_state.custom_workout['name']:
                    st.error("Please provide a name for your workout")
                elif not st.session_state.custom_workout['exercises']:
                    st.error("Please add at least one exercise to your workout")
                else:
                    if st.session_state.user['logged_in']:
                        # In a real app, this would save to the database
                        st.success(f"Workout '{st.session_state.custom_workout['name']}' saved successfully!")
                        # Clear the form for a new workout
                        st.session_state.custom_workout = {
                            'name': '',
                            'description': '',
                            'difficulty': 'Beginner',
                            'duration': 30,
                            'goal': 'General Fitness',
                            'exercises': []
                        }
                        st.rerun()
                    else:
                        st.warning("Please log in to save workouts")
    
    # Tab 3: AI Workout Generator
    with tab3:
        st.subheader("AI Workout Generator")
        st.write("Let our AI create a personalized workout plan based on your goals.")
        
        # Goal selection
        goal_options = ["Strength", "Muscle Gain", "Weight Loss", "Cardio", "Core Strength"]
        selected_goal = st.selectbox(
            "What's your primary goal?",
            goal_options
        )
        
        # Generate button
        if st.button("Generate Workout Plan"):
            with st.spinner("Generating your personalized workout plan..."):
                # Get AI-suggested workout
                workout = get_workout_suggestion(st.session_state.user, selected_goal)
                
                # Display the generated workout
                st.subheader(workout['name'])
                st.write(f"**Description:** {workout['description']}")
                st.write(f"**Duration:** {workout['duration']} minutes")
                
                # Display exercises
                st.subheader("Exercises")
                for i, exercise in enumerate(workout['exercises'], 1):
                    cols = st.columns([3, 1, 1, 1])
                    with cols[0]:
                        st.write(f"**{i}. {exercise['name']}**")
                    with cols[1]:
                        st.write(f"{exercise['sets']} sets")
                    with cols[2]:
                        st.write(f"{exercise['reps']}")
                    with cols[3]:
                        st.write(f"Rest: {exercise['rest']}s")
                
                # Save generated workout button
                if st.button("Save Generated Workout"):
                    if st.session_state.user['logged_in']:
                        # Convert to custom workout format
                        st.session_state.custom_workout = {
                            'name': workout['name'],
                            'description': workout['description'],
                            'difficulty': st.session_state.user.get('experience_level', 'Beginner'),
                            'duration': workout['duration'],
                            'goal': selected_goal,
                            'exercises': []
                        }
                        
                        # Add exercises
                        for ex in workout['exercises']:
                            st.session_state.custom_workout['exercises'].append({
                                'id': 0,  # Placeholder ID
                                'name': ex['name'],
                                'category': '',
                                'sets': ex['sets'],
                                'reps': ex['reps'],
                                'rest': ex['rest']
                            })
                        
                        st.success(f"Workout '{workout['name']}' saved to your custom workouts!")
                    else:
                        st.warning("Please log in to save workouts")
