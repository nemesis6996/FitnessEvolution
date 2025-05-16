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
        st.subheader("Riepilogo Statistiche")
        
        if 'height' in st.session_state.user and 'weight' in st.session_state.user:
            # Calculate BMI
            height_m = st.session_state.user['height'] / 100
            bmi = st.session_state.user['weight'] / (height_m ** 2)
            
            # Display stats
            st.metric("BMI", f"{bmi:.1f}")
            
            # BMI category tradotto in italiano
            bmi_category = ""
            if bmi < 18.5:
                bmi_category = "Sottopeso"
            elif bmi < 25:
                bmi_category = "Peso normale"
            elif bmi < 30:
                bmi_category = "Sovrappeso"
            else:
                bmi_category = "Obesità"
            
            st.info(f"Categoria BMI: {bmi_category}")
        
        # Display goals in italiano
        if 'goals' in st.session_state.user and st.session_state.user['goals']:
            st.write("**I Tuoi Obiettivi:**")
            
            # Mappa per tradurre gli obiettivi in italiano
            goal_map_rev = {
                "Weight Loss": "Perdita di Peso",
                "Muscle Gain": "Aumento Massa", 
                "Strength": "Forza", 
                "Endurance": "Resistenza", 
                "Flexibility": "Flessibilità", 
                "General Fitness": "Fitness Generale"
            }
            
            for goal in st.session_state.user['goals']:
                # Mostra l'obiettivo tradotto in italiano se disponibile
                display_goal = goal_map_rev.get(goal, goal)
                st.write(f"- {display_goal}")
    
    # Body measurements section
    st.divider()
    st.subheader("Misure Corporee")
    
    # Tabs for different measurement options
    tab1, tab2 = st.tabs(["Inserisci Misure", "Storico Misurazioni"])
    
    with tab1:
        # Form for entering measurements
        with st.form("measurements_form"):
            st.write("Inserisci le tue misure corporee attuali")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                chest = st.number_input("Petto (cm)", min_value=50, max_value=150, value=95)
                arms = st.number_input("Braccia (cm)", min_value=20, max_value=60, value=35)
            
            with col2:
                waist = st.number_input("Vita (cm)", min_value=50, max_value=150, value=85)
                thighs = st.number_input("Cosce (cm)", min_value=30, max_value=100, value=55)
            
            with col3:
                hips = st.number_input("Fianchi (cm)", min_value=50, max_value=150, value=100)
                body_fat = st.number_input("Grasso Corporeo (%)", min_value=3.0, max_value=50.0, value=15.0)
            
            measurement_notes = st.text_area("Note", placeholder="Note aggiuntive sulle tue misurazioni")
            
            col1, col2 = st.columns(2)
            with col1:
                ai_assist = st.checkbox("Utilizza l'IA per analizzare le foto caricate", value=True)
                if ai_assist:
                    st.info("L'IA analizzerà le foto che hai caricato per migliorare l'accuratezza delle misurazioni")
            
            # Submit button
            submitted = st.form_submit_button("Salva Misurazioni")
            if submitted:
                # In a real app, this would save to the database
                st.success("Misurazioni salvate con successo!")
                
                # Aggiunge un messaggio divertente/motivazionale
                import random
                messages = [
                    "🏋️‍♂️ Nemesis dice: 'Stai andando alla grande! Non dimenticare l'allenamento di oggi!'",
                    "💪 Nemesis dice: 'Vedo progressi! Continuiamo a spingere!'",
                    "🥦 Nemesis dice: 'Ricordati di bere acqua e mangiare verdure... e poi altri 20 push-up!'",
                    "🏃‍♀️ Nemesis dice: 'Niente scuse oggi! Ti aspetto per l'allenamento gambe!'",
                    "🔥 Nemesis dice: 'Questi numeri sono buoni, ma possiamo migliorarli! Pronto per un'altra sfida?'"
                ]
                st.info(random.choice(messages))
                
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
    st.subheader("Personalizzazione Avatar con IA")
    
    # Aggiungi la funzionalità di caricamento foto/video e analisi IA
    st.markdown("""
    <div style="background-color:#f0f9ff; padding:15px; border-radius:10px; margin-bottom:20px;">
    <h4 style="color:#0072b1;">Crea il tuo avatar con l'assistenza dell'IA 🤖</h4>
    <p>Carica le tue foto o un breve video per creare un avatar personalizzato che si aggiorna con i tuoi progressi.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Carica Foto", "Registra Video"])
    
    with tab1:
        col1, col2 = st.columns([2,1])
        with col1:
            st.write("**Carica le tue foto:**")
            st.file_uploader("Foto frontale", type=["jpg", "jpeg", "png"], key="front_photo")
            st.file_uploader("Foto laterale", type=["jpg", "jpeg", "png"], key="side_photo")
            
            if st.button("Genera Avatar con IA", key="generate_avatar_photo"):
                # Placeholder per la funzionalità reale di generazione avatar
                with st.spinner("L'IA sta analizzando le tue foto e creando il tuo avatar personalizzato..."):
                    # Simulazione breve attesa
                    import time
                    time.sleep(2)
                    st.success("Avatar generato con successo! L'avatar si aggiornerà automaticamente con i tuoi progressi.")
                    
                    # Aggiungiamo un messaggio divertente
                    st.info("🏋️‍♂️ Nemesis dice: 'Ho analizzato il tuo fisico, ora è il momento di farti sudare! Sei pronto per una nuova sfida?'")
        
        with col2:
            st.write("**Suggerimenti:**")
            st.markdown("""
            - Indossa abiti aderenti
            - Scatta foto con buona illuminazione
            - Mantieni una postura neutra
            - Usa uno sfondo semplice
            """)
    
    with tab2:
        st.write("**Registra un breve video a 360°:**")
        st.file_uploader("Carica video", type=["mp4", "mov"], key="body_video")
        
        st.write("Oppure registra direttamente dalla webcam:")
        if st.button("Inizia registrazione", key="start_recording"):
            st.info("Questa funzionalità richiede l'accesso alla fotocamera. Nell'app mobile, questa opzione ti permetterà di registrare un breve video a 360° per un'analisi completa.")
        
        st.write("**Vantaggi dell'analisi video:**")
        st.markdown("""
        - Maggiore precisione nelle misurazioni
        - Rilevamento automatico della postura
        - Suggerimenti personalizzati per il tuo allenamento
        - Aggiornamento più accurato dell'avatar
        """)
    
    # Sezione per le opzioni di personalizzazione
    st.subheader("Opzioni di Personalizzazione")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Personalizza il tuo avatar:**")
        st.color_picker("Colore abiti", "#3498db", key="clothes_color")
        st.selectbox("Stile capelli", ["Corto", "Medio", "Lungo", "Calvo"], key="hair_style")
        st.slider("Altezza muscoli", 1, 10, 5, key="muscle_definition")
    
    with col2:
        st.write("**Impostazioni avanzate:**")
        st.checkbox("Mostra progressi muscolari", value=True, key="show_muscle_progress")
        st.checkbox("Evidenzia aree da allenare", value=True, key="highlight_training_areas")
        st.checkbox("Usa rendering avanzato", value=True, key="use_advanced_rendering")
