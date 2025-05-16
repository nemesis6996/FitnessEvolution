import streamlit as st
import pandas as pd
from utils.database import get_exercise_categories, get_exercises_by_category, get_all_exercises

def show():
    st.title("Database Esercizi")
    
    # Search box
    search_query = st.text_input("Cerca esercizi", placeholder="Inserisci nome esercizio, gruppo muscolare o attrezzo")
    
    # Category filter
    categories = get_exercise_categories()
    category_names = {
        "Strength": "Forza",
        "Cardio": "Cardio",
        "Flexibility": "Flessibilità",
        "Functional": "Funzionale",
        "Balance": "Equilibrio",
        "Core": "Core"
    }
    
    italian_categories = ["Tutte le Categorie"] + [category_names.get(cat, cat) for cat in categories]
    selected_italian_category = st.selectbox(
        "Filtra per categoria",
        italian_categories
    )
    
    # Map back to English for database query
    if selected_italian_category == "Tutte le Categorie":
        selected_category = "All Categories"
    else:
        # Find the English key for the selected Italian value
        selected_category = next((key for key, value in category_names.items() 
                                if value == selected_italian_category), selected_italian_category)
    
    # Difficulty filter
    difficulties_map = {
        "Tutti i Livelli": "All Levels",
        "Principiante": "Beginner",
        "Intermedio": "Intermediate",
        "Avanzato": "Advanced"
    }
    
    italian_difficulties = ["Tutti i Livelli", "Principiante", "Intermedio", "Avanzato"]
    selected_italian_difficulty = st.selectbox(
        "Filtra per difficoltà",
        italian_difficulties
    )
    
    # Map back to English
    selected_difficulty = difficulties_map[selected_italian_difficulty]
    
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
    st.write(f"{len(exercises)} esercizi trovati")
    
    # Display exercises
    if not exercises:
        st.info("Nessun esercizio corrisponde ai tuoi criteri. Prova a modificare i filtri.")
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
                            
                            difficulty_it = {"Beginner": "Principiante", "Intermediate": "Intermedio", "Advanced": "Avanzato"}
                            st.markdown(f"**Difficoltà:** {difficulty_it.get(exercise.get('difficulty'), exercise.get('difficulty', 'Non specificato'))}")
                            
                            category_it = category_names.get(exercise.get('category_name', ''), exercise.get('category_name', ''))
                            st.markdown(f"**Categoria:** {category_it or 'Non categorizzato'}")
                            
                            st.markdown(f"**Attrezzi:** {exercise.get('equipment', 'Nessuno richiesto')}")
                            st.markdown(f"**Muscoli:** {exercise.get('muscles_targeted', 'Non specificato')}")
                            
                            st.markdown("### Descrizione")
                            st.write(exercise.get('description', 'Nessuna descrizione disponibile.'))
                            
                            st.markdown("### Istruzioni")
                            instructions = exercise.get('instructions', 'Nessuna istruzione disponibile.')
                            # Split instructions by newlines and format as a numbered list
                            if '\n' in instructions:
                                inst_list = instructions.split('\n')
                                for i, inst in enumerate(inst_list, 1):
                                    if inst.strip():  # Skip empty lines
                                        st.write(f"{inst}")
                            else:
                                st.write(instructions)
                            
                            if exercise.get('tips'):
                                st.markdown("### Consigli")
                                st.write(exercise.get('tips'))
                            
                            # Add to Workout button
                            if st.button("Aggiungi alla Scheda", key=f"add_{exercise['id']}"):
                                if 'workout_builder' not in st.session_state:
                                    st.session_state.workout_builder = []
                                
                                # Check if exercise already in workout builder
                                existing_ids = [ex['id'] for ex in st.session_state.workout_builder]
                                if exercise['id'] not in existing_ids:
                                    st.session_state.workout_builder.append(exercise)
                                    st.success(f"{exercise['name']} aggiunto alla tua scheda")
                                else:
                                    st.info(f"{exercise['name']} è già nella tua scheda")
    
    # Workout Builder section
    if 'workout_builder' in st.session_state and st.session_state.workout_builder:
        st.divider()
        st.subheader("Costruttore Scheda")
        st.write(f"{len(st.session_state.workout_builder)} esercizi nella tua scheda")
        
        # Display selected exercises in a table
        workout_data = []
        for ex in st.session_state.workout_builder:
            category_it = category_names.get(ex.get('category_name', ''), ex.get('category_name', ''))
            difficulty_it = {"Beginner": "Principiante", "Intermediate": "Intermedio", "Advanced": "Avanzato"}
            difficulty_translated = difficulty_it.get(ex.get('difficulty', ''), ex.get('difficulty', ''))
            
            workout_data.append({
                "Exercise": ex['name'],
                "Category": category_it,
                "Difficulty": difficulty_translated,
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
            if st.button("Salva Scheda"):
                if st.session_state.user['logged_in']:
                    st.info("La funzionalità di salvataggio aggiungerà questa scheda al tuo account")
                else:
                    st.warning("Effettua il login per salvare le schede")
        
        with col2:
            if st.button("Cancella Scheda"):
                st.session_state.workout_builder = []
                st.rerun()
