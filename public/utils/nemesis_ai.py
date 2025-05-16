import streamlit as st
import os
import json
from openai import OpenAI

# Get API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your_openai_api_key")
openai = OpenAI(api_key=OPENAI_API_KEY)

class NemesisAI:
    """
    Nemesis - L'assistente AI di NemFit
    Gestisce tutte le interazioni con l'utente e fornisce consigli personalizzati
    """
    
    def __init__(self):
        self.system_prompt = """
        Sei Nemesis, l'assistente AI personale dell'app di fitness NemFit. 
        Il tuo compito è aiutare gli utenti con i loro obiettivi di fitness, rispondere alle domande 
        sugli esercizi, offrire consigli su nutrizione e allenamento, e motivare gli utenti.
        
        Rispondi sempre in italiano, in modo amichevole ma professionale.
        Considera i seguenti principi quando interagisci con l'utente:
        
        1. Personalizzazione: Adatta i consigli in base ai dati dell'utente quando disponibili
        2. Supporto: Offri incoraggiamento e motivazione positiva
        3. Conoscenza: Fornisci informazioni scientifiche e basate sull'evidenza
        4. Sicurezza: Ricorda agli utenti di consultare professionisti per problemi di salute specifici
        5. Rispetto: Non giudicare mai gli utenti per il loro livello di fitness o le loro scelte
        
        Non usare mai un linguaggio che faccia sentire l'utente in colpa o inadeguato.
        """
        
        # Inizializza la cronologia delle conversazioni se non esiste
        if 'nemesis_history' not in st.session_state:
            st.session_state.nemesis_history = []
    
    def generate_response(self, user_message, user_data=None):
        """
        Genera una risposta basata sul messaggio dell'utente e sui dati utente disponibili
        
        Args:
            user_message: Il messaggio dell'utente
            user_data: Dizionario contenente dati dell'utente (opzionale)
            
        Returns:
            La risposta dell'assistente
        """
        
        # Se non c'è una API key valida, fornisci una risposta predefinita
        if OPENAI_API_KEY == "your_openai_api_key":
            return self.get_default_response(user_message, user_data)
        
        try:
            # Prepara i dati utente per includerli nel contesto
            user_context = ""
            if user_data and user_data.get('logged_in', False):
                user_context = f"""
                Informazioni sull'utente:
                - Nome: {user_data.get('username', 'Utente')}
                - Livello di esperienza: {user_data.get('experience_level', 'Non specificato')}
                - Altezza: {user_data.get('height', 'Non specificata')} cm
                - Peso: {user_data.get('weight', 'Non specificato')} kg
                - Obiettivi: {', '.join(user_data.get('goals', ['Non specificati']))}
                """
            
            # Costruisci i messaggi per l'API
            messages = [
                {"role": "system", "content": self.system_prompt + user_context}
            ]
            
            # Aggiungi la cronologia della conversazione recente (ultimi 5 messaggi)
            recent_history = st.session_state.nemesis_history[-5:] if st.session_state.nemesis_history else []
            messages.extend(recent_history)
            
            # Aggiungi il messaggio attuale dell'utente
            messages.append({"role": "user", "content": user_message})
            
            # Chiama l'API di OpenAI
            # Il modello più recente di OpenAI è "gpt-4o" rilasciato il 13 maggio 2024.
            # Non modificare a meno che non sia esplicitamente richiesto dall'utente
            
            # Converti il dizionario in formato corretto per l'API
            api_messages = []
            for msg in messages:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
                
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=api_messages,
                max_tokens=500,
                temperature=0.7,
            )
            
            # Estrai la risposta
            assistant_message = response.choices[0].message.content
            
            # Aggiorna la cronologia della conversazione
            st.session_state.nemesis_history.append({"role": "user", "content": user_message})
            st.session_state.nemesis_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            st.error(f"Errore nell'assistente Nemesis: {str(e)}")
            return self.get_default_response(user_message, user_data)
    
    def get_default_response(self, user_message, user_data=None):
        """
        Fornisce una risposta predefinita quando l'API non è disponibile
        """
        # Risposte predefinite basate su parole chiave nel messaggio dell'utente
        msg = user_message.lower()
        
        if any(word in msg for word in ["ciao", "salve", "buongiorno", "buonasera", "hey"]):
            return "Ciao! Sono Nemesis, il tuo assistente personale di fitness. Come posso aiutarti oggi?"
        
        elif any(word in msg for word in ["esercizi", "allenamento", "workout", "scheda"]):
            return "Posso aiutarti a trovare gli esercizi giusti per te. Che tipo di allenamento ti interessa? Cardio, forza, flessibilità o un mix? Dimmi quali sono i tuoi obiettivi e posso suggerirti una scheda adatta al tuo livello."
        
        elif any(word in msg for word in ["dieta", "nutrizione", "mangiare", "cibo", "calorie"]):
            return "L'alimentazione è fondamentale per raggiungere i tuoi obiettivi di fitness. Una buona regola generale è consumare proteine di qualità, carboidrati complessi, grassi sani e molte verdure. Ti consiglio comunque di consultare un nutrizionista per un piano personalizzato."
        
        elif any(word in msg for word in ["peso", "dimagrire", "bruciare", "grasso"]):
            return "Per perdere peso in modo sano ed efficace, è importante combinare un deficit calorico moderato con attività fisica regolare. Ti consiglio un mix di cardio, esercizi di forza e una dieta equilibrata. Ricorda che la costanza è più importante dei risultati immediati."
        
        elif any(word in msg for word in ["muscoli", "massa", "forza", "tonificare"]):
            return "Per aumentare la massa muscolare, concentrati su allenamenti di forza progressivi, un adeguato apporto proteico e riposo sufficiente. Gli esercizi composti come squat, stacchi da terra e panca piana sono particolarmente efficaci."
        
        elif any(word in msg for word in ["grazie", "thank", "aiuto"]):
            return "Sono felice di poterti aiutare! Se hai altre domande, non esitare a chiedere. Sono qui per supportarti nel tuo percorso fitness."
        
        else:
            return "Sono Nemesis, il tuo assistente AI di NemFit. Posso aiutarti con consigli su allenamento, nutrizione, e rispondere a domande sul fitness. Come posso esserti utile oggi?"
    
    def clear_conversation(self):
        """
        Cancella la cronologia della conversazione
        """
        st.session_state.nemesis_history = []
        return "Ho cancellato la nostra conversazione precedente. Possiamo iniziare di nuovo. Come posso aiutarti?"

def show_nemesis_chat():
    """
    Mostra l'interfaccia di chat dell'assistente Nemesis
    """
    st.title("Nemesis - Il Tuo Assistente AI")
    
    # Inizializza l'assistente
    nemesis = NemesisAI()
    
    # Pulsante per cancellare la conversazione
    if st.button("Nuova Conversazione"):
        response = nemesis.clear_conversation()
        st.info(response)
    
    # Area di input per il messaggio dell'utente
    user_message = st.text_input("Chiedi qualcosa a Nemesis", placeholder="Es: Quali esercizi sono migliori per la schiena?")
    
    # Invia il messaggio
    if user_message:
        # Ottieni la risposta dall'assistente
        response = nemesis.generate_response(user_message, st.session_state.user)
        
        # Mostra la risposta
        st.write("### Nemesis:")
        st.write(response)
        
    # Mostra la cronologia della conversazione
    if st.session_state.nemesis_history:
        st.divider()
        st.subheader("Cronologia della Conversazione")
        
        for i, message in enumerate(st.session_state.nemesis_history):
            if message["role"] == "user":
                st.write(f"**Tu:** {message['content']}")
            else:
                st.write(f"**Nemesis:** {message['content']}")
            
            if i < len(st.session_state.nemesis_history) - 1:
                st.write("---")
    
    # Suggerimenti di domande
    st.sidebar.subheader("Esempi di Domande")
    suggestions = [
        "Come posso migliorare la mia resistenza?",
        "Quali sono i migliori esercizi per le braccia?",
        "Quanta proteina dovrei assumere?",
        "Come posso evitare infortuni durante l'allenamento?",
        "Puoi consigliarmi una scheda per principianti?"
    ]
    
    for suggestion in suggestions:
        if st.sidebar.button(suggestion, key=f"suggest_{suggestion}"):
            # Simula l'invio del suggerimento come messaggio dell'utente
            response = nemesis.generate_response(suggestion, st.session_state.user)
            st.write(f"**Tu:** {suggestion}")
            st.write("### Nemesis:")
            st.write(response)
            st.rerun()