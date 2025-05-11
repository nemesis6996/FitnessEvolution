import streamlit as st
import pandas as pd
from utils.avatar import get_customized_avatar_html

def show():
    st.title("Il Mio Profilo")
    
    if not st.session_state.user['logged_in']:
        st.warning("Effettua il login per visualizzare e modificare il tuo profilo")
        return
    
    # Main layout with columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Profile information form
        st.subheader("Informazioni Personali")
        
        # Get existing user data
        user_data = st.session_state.user
        
        # Form for user details
        with st.form("profile_form"):
            # Basic information
            first_name = st.text_input("Nome", value=user_data.get('first_name', ''))
            last_name = st.text_input("Cognome", value=user_data.get('last_name', ''))
            email = st.text_input("Email", value=user_data.get('email', ''))
            
            # Physical stats
            st.subheader("Statistiche Fisiche")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                height = st.number_input("Altezza (cm)", min_value=120, max_value=220, value=user_data.get('height', 175))
            
            with col2:
                weight = st.number_input("Peso (kg)", min_value=30, max_value=200, value=user_data.get('weight', 75))
            
            with col3:
                # Traduci le opzioni
                level_map = {
                    "Principiante": "Beginner",
                    "Intermedio": "Intermediate", 
                    "Avanzato": "Advanced"
                }
                levels_it = ["Principiante", "Intermedio", "Avanzato"]
                
                # Converti il valore attuale in italiano
                current_level = user_data.get('experience_level', 'Beginner')
                for it_level, en_level in level_map.items():
                    if en_level == current_level:
                        current_it_level = it_level
                        break
                else:
                    current_it_level = "Principiante"
                
                selected_it_level = st.selectbox(
                    "Livello di Esperienza",
                    levels_it,
                    index=levels_it.index(current_it_level)
                )
                experience_level = level_map[selected_it_level]
            
            # Fitness goals
            st.subheader("Obiettivi di Fitness")
            
            # Traduci le opzioni degli obiettivi
            goals_map = {
                "Perdita di Peso": "Weight Loss", 
                "Aumento Massa": "Muscle Gain", 
                "Forza": "Strength", 
                "Resistenza": "Endurance", 
                "Flessibilità": "Flexibility", 
                "Fitness Generale": "General Fitness"
            }
            goals_it = list(goals_map.keys())
            
            # Converti i valori attuali in italiano
            current_goals = user_data.get('goals', ["General Fitness"])
            current_goals_it = []
            
            for en_goal in current_goals:
                for it_goal, en_goal_map in goals_map.items():
                    if en_goal_map == en_goal:
                        current_goals_it.append(it_goal)
                        break
            
            selected_goals_it = st.multiselect(
                "Seleziona i tuoi obiettivi di fitness",
                goals_it,
                default=current_goals_it
            )
            
            # Converti indietro in inglese per il backend
            goals = [goals_map[goal_it] for goal_it in selected_goals_it]
            
            # Additional notes
            notes = st.text_area("Note Aggiuntive", value=user_data.get('notes', ''))
            
            # Submit button
            submitted = st.form_submit_button("Salva Profilo")
            if submitted:
                # Update session state with new values
                st.session_state.user.update({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'height': height,
                    'weight': weight,
                    'experience_level': experience_level,
                    'goals': goals,
                    'notes': notes
                })
                
                # In a real app, this would save to the database
                st.success("Profile updated successfully!")
    
    with col2:
        # Avatar visualization
        st.subheader("Il Tuo Avatar 3D")
        
        # Get customized avatar HTML
        avatar_html = get_customized_avatar_html(st.session_state.user)
        st.markdown(avatar_html, unsafe_allow_html=True)
        
        st.caption("L'avatar si aggiorna automaticamente in base ai tuoi progressi")
        
        # Profile stats in a card
        st.subheader("Stats Summary")
        
        if 'height' in st.session_state.user and 'weight' in st.session_state.user:
            # Calculate BMI
            height_m = st.session_state.user['height'] / 100
            bmi = st.session_state.user['weight'] / (height_m ** 2)
            
            # Display stats
            st.metric("BMI", f"{bmi:.1f}")
            
            # BMI category
            bmi_category = ""
            if bmi < 18.5:
                bmi_category = "Underweight"
            elif bmi < 25:
                bmi_category = "Normal weight"
            elif bmi < 30:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obesity"
            
            st.info(f"BMI Category: {bmi_category}")
        
        # Display goals
        if 'goals' in st.session_state.user and st.session_state.user['goals']:
            st.write("**Your Goals:**")
            for goal in st.session_state.user['goals']:
                st.write(f"- {goal}")
    
    # Body measurements section
    st.divider()
    st.subheader("Body Measurements")
    
    # Tabs for different measurement options
    tab1, tab2 = st.tabs(["Enter Measurements", "Measurement History"])
    
    with tab1:
        # Form for entering measurements
        with st.form("measurements_form"):
            st.write("Enter your current body measurements")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                chest = st.number_input("Chest (cm)", min_value=50, max_value=150, value=95)
                arms = st.number_input("Arms (cm)", min_value=20, max_value=60, value=35)
            
            with col2:
                waist = st.number_input("Waist (cm)", min_value=50, max_value=150, value=85)
                thighs = st.number_input("Thighs (cm)", min_value=30, max_value=100, value=55)
            
            with col3:
                hips = st.number_input("Hips (cm)", min_value=50, max_value=150, value=100)
                body_fat = st.number_input("Body Fat (%)", min_value=3.0, max_value=50.0, value=15.0)
            
            measurement_notes = st.text_area("Notes", placeholder="Any additional notes about your measurements")
            
            # Submit button
            submitted = st.form_submit_button("Save Measurements")
            if submitted:
                # In a real app, this would save to the database
                st.success("Measurements saved successfully!")
                
                # Update session state for demo
                if 'measurements' not in st.session_state:
                    st.session_state.measurements = []
                
                import datetime
                st.session_state.measurements.append({
                    'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                    'chest': chest,
                    'waist': waist,
                    'hips': hips,
                    'arms': arms,
                    'thighs': thighs,
                    'body_fat': body_fat,
                    'notes': measurement_notes
                })
    
    with tab2:
        # Show measurement history
        if 'measurements' in st.session_state and st.session_state.measurements:
            # Convert to DataFrame for display
            df = pd.DataFrame(st.session_state.measurements)
            
            # Reverse order to show newest first
            df = df.iloc[::-1].reset_index(drop=True)
            
            # Display as a table
            st.dataframe(df)
            
            # Option to visualize progress
            if st.button("View Progress Charts"):
                st.session_state.show_progress = True
                st.rerun()
        else:
            st.info("No measurement history available. Add measurements to track your progress.")
    
    # Avatar customization section
    st.divider()
    st.subheader("Avatar Customization")
    
    st.info("In a complete mobile app version, this section would allow detailed body scanning and avatar customization.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Body Scanning Options:**")
        st.write("- Front-facing photo upload")
        st.write("- Side profile photo upload")
        st.write("- Manual measurement input")
        st.write("- AI-assisted body analysis")
    
    with col2:
        st.write("**Customization Options:**")
        st.write("- Skin tone")
        st.write("- Hair style and color")
        st.write("- Clothing and accessories")
        st.write("- Facial features")
