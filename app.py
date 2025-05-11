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
from utils.nemesis_ai import NemesisAI

# Set page configuration
st.set_page_config(
    page_title="NemFit App",
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
    
# Aggiungi lo stato della pagina selezionata per gestire la navigazione
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = "Home"

# Initialize database on app start
initialize_database()

# Sidebar for navigation
with st.sidebar:
    st.image("assets/nemfit_logo.png", width=150)
    st.title("NemFit")
    
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
                    st.error("Inserisci username e password")
        
        with col2:
            if st.button("Registrati"):
                st.info("La funzionalità di registrazione sarà disponibile nella versione completa")
        
        # Social login options
        st.divider()
        st.write("Oppure accedi con:")
        social_col1, social_col2 = st.columns(2)
        with social_col1:
            if st.button("Google", key="google_login"):
                st.session_state.user['logged_in'] = True
                st.session_state.user['username'] = "Utente Google"
                st.rerun()
        
        with social_col2:
            if st.button("Apple ID", key="apple_login"):
                st.session_state.user['logged_in'] = True
                st.session_state.user['username'] = "Utente Apple"
                st.rerun()
    
    else:
        st.success(f"Benvenuto, {st.session_state.user['username']}")
        if st.button("Logout"):
            st.session_state.user['logged_in'] = False
            st.rerun()
    
    st.divider()
    
    # Main navigation
    st.subheader("Menu")
    # Usa la selezione della pagina dallo stato della sessione
    page_options = ["Home", "Esercizi", "Schede Allenamento", "Profilo", "Progressi", "Nemesis AI", "Pannello Admin"]
    index = page_options.index(st.session_state.page_selection) if st.session_state.page_selection in page_options else 0
    
    selected = st.radio(
        "Vai a",
        page_options,
        index=index,
        key="navigation"
    )
    
    # Aggiorna la selezione della pagina nello stato della sessione
    if selected != st.session_state.page_selection:
        st.session_state.page_selection = selected
        st.rerun()

# Main content based on selection
if selected == "Home":
    st.title("Benvenuto in NemFit")
    
    # Main columns for home page
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Il tuo Coach Fitness con Intelligenza Artificiale
        
        NemFit ti aiuta a raggiungere i tuoi obiettivi di fitness con:
        
        - **Database Completo di Esercizi** - Istruzioni dettagliate e guide visive
        - **Schede di Allenamento Intelligenti** - Personalizzate per i tuoi obiettivi
        - **Visualizzazione Avatar 3D** - Monitora la trasformazione del tuo corpo
        - **Raccomandazioni AI** - Ottieni consigli personalizzati
        - **Body Scan** - Crea un avatar realistico con le tue foto
        
        Inizia esplorando gli esercizi o creando una scheda di allenamento!
        """)
        
        # Featured workout section
        st.subheader("Scheda in Evidenza")
        featured_workout = {
            "name": "Forza Corpo Completo",
            "difficulty": "Intermedio",
            "duration": "45 minuti",
            "exercises": ["Squat con Bilanciere", "Panca Piana", "Stacco da Terra", "Trazioni", "Shoulder Press"]
        }
        
        with st.expander("Scheda Forza Corpo Completo", expanded=True):
            st.write(f"**Difficoltà:** {featured_workout['difficulty']}")
            st.write(f"**Durata:** {featured_workout['duration']}")
            st.write("**Esercizi:**")
            for exercise in featured_workout['exercises']:
                st.write(f"- {exercise}")
            
            if st.button("Aggiungi alle Mie Schede"):
                if st.session_state.user['logged_in']:
                    st.session_state.workout_plan.append(featured_workout)
                    st.success("Scheda aggiunta al tuo piano!")
                else:
                    st.warning("Effettua il login per salvare le schede")
    
    with col2:
        # Avatar preview
        st.subheader("Il Tuo Avatar")
        
        if st.session_state.user['logged_in']:
            st.markdown(get_avatar_placeholder(), unsafe_allow_html=True)
            st.caption("L'avatar si aggiorna con i tuoi progressi")
        else:
            st.info("Effettua il login per vedere il tuo avatar fitness")
        
        # AI recommendation section
        st.subheader("Consiglio AI")
        if st.session_state.user['logged_in']:
            with st.spinner("Ottenendo raccomandazioni personalizzate..."):
                recommendation = get_ai_recommendation(st.session_state.user)
                st.info(recommendation)
        else:
            st.info("Effettua il login per ricevere consigli personalizzati dall'AI")
    
    # Featured exercise categories
    st.subheader("Esplora Categorie di Esercizi")
    categories = get_exercise_categories()
    
    # Display categories in a grid
    cols = st.columns(3)
    for i, category in enumerate(categories[:6]):  # Show first 6 categories
        with cols[i % 3]:
            category_names = {
                "Strength": "Forza",
                "Cardio": "Cardio",
                "Flexibility": "Flessibilità",
                "Functional": "Funzionale",
                "Balance": "Equilibrio",
                "Core": "Core"
            }
            it_category = category_names.get(category, category)
            st.markdown(f"### {it_category}")
            # Show a sample exercise from this category
            exercises = get_exercises_by_category(category)
            if exercises:
                sample = exercises[0]
                st.write(f"**{sample['name']}**")
                st.write(sample['short_description'])
                if st.button(f"Esplora {it_category}", key=f"cat_{i}"):
                    st.session_state.selected_category = category
                    # Cambia la selezione a "Esercizi" per navigare alla pagina esercizi
                    st.session_state.page_selection = "Esercizi"
                    st.rerun()
    
    # Testimonials
    st.divider()
    st.subheader("Storie di Successo")
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        #### "Ho perso 15kg in 3 mesi"
        
        Le schede personalizzate e il monitoraggio dei progressi mi hanno aiutato a rimanere motivato.
        
        *- Alessandro M.*
        """)
    
    with cols[1]:
        st.markdown("""
        #### "Finalmente sto sviluppando muscoli"
        
        Le istruzioni degli esercizi e le linee guida sulla forma hanno rivoluzionato la mia tecnica.
        
        *- Giacomo K.*
        """)
    
    with cols[2]:
        st.markdown("""
        #### "Perfetto per principianti"
        
        Il coach AI ha risposto a tutte le mie domande e mi ha tenuto in carreggiata.
        
        *- Marco S.*
        """)

elif selected == "Esercizi":
    import pages.exercises
    pages.exercises.show()

elif selected == "Schede Allenamento":
    import pages.workout_plans
    pages.workout_plans.show()

elif selected == "Profilo":
    import pages.profile
    pages.profile.show()

elif selected == "Progressi":
    import pages.progress
    pages.progress.show()

elif selected == "Nemesis AI":
    import pages.nemesis
    pages.nemesis.show()

elif selected == "Pannello Admin":
    import pages.admin
    pages.admin.show()

# Footer
st.divider()
st.caption("© 2023 NemFit - Applicazione Fitness con Intelligenza Artificiale")
