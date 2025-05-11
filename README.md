# NemFit - Applicazione Fitness con Intelligenza Artificiale

NemFit è un'applicazione fitness completa, potenziata dall'intelligenza artificiale, con un database di esercizi, schede di allenamento personalizzabili e un avatar 3D che si aggiorna con i tuoi progressi.

## Caratteristiche Principali

- **Database Esercizi Completo**: Centinaia di esercizi con istruzioni dettagliate e visualizzazioni
- **Schede di Allenamento Personalizzabili**: Crea e modifica schede adatte ai tuoi obiettivi
- **Avatar 3D Interattivo**: Visualizza il tuo progresso con un avatar 3D che si aggiorna
- **Body Scanning con IA**: Carica foto o video per creare un avatar personalizzato
- **Nemesis AI**: Assistente virtuale che ti guida e motiva durante l'allenamento
- **Multilingua**: Completamente in italiano con possibilità di cambiare lingua
- **Notifiche Motivazionali**: Promemoria divertenti e personalizzati

## Requisiti di Sistema

- Python 3.8+
- Streamlit
- Pandas, Plotly
- Connessione internet per le funzionalità AI

## Installazione

1. Clona il repository:
```
git clone https://github.com/tuonome/nemfit.git
cd nemfit
```

2. Installa le dipendenze:
```
pip install -r requirements.txt
```

3. Avvia l'applicazione:
```
streamlit run app.py
```

## Deployment

L'app è configurata per essere facilmente deployata su:

- **Streamlit Cloud**: Compatibile e pronta per il deployment
- **Heroku**: Incluso Procfile per deployment automatico
- **Vercel**: Configurazione inclusa in vercel.json
- **Netlify**: Configurazione inclusa in netlify.toml
- **Docker**: Dockerfile incluso per containerizzazione

## Configurazione

L'app utilizza file di configurazione specifici per ogni ambiente:

- `.streamlit/config.toml`: Configurazione Streamlit
- `vercel.json`: Configurazione per Vercel
- `netlify.toml`: Configurazione per Netlify
- `firebase.json`: Configurazione per Firebase

## Integrazione API

NemFit può integrarsi con diverse API esterne:

- **OpenAI**: Per l'assistente AI e raccomandazioni
- **Anthropic**: Alternativa per l'assistente AI
- **Twilio**: Per notifiche SMS personalizzate

## Personalizzazione

Puoi personalizzare l'app modificando:

- I colori del tema in `.streamlit/config.toml`
- Il database in `utils/database.py`
- Le risposte AI in `utils/nemesis_ai.py`
- L'avatar 3D in `utils/avatar.py`

## Supporto e Contatti

Per domande, suggerimenti o supporto, contattare il team di sviluppo all'indirizzo email: support@nemfit.com

---

© 2023 NemFit - Tutti i diritti riservati