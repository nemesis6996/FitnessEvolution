import streamlit as st
import datetime
import random
from utils.config import get_random_motivation_phrase

def setup_notification_system():
    """
    Inizializza il sistema di notifiche nell'app
    """
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    
    if 'notification_settings' not in st.session_state:
        st.session_state.notification_settings = {
            'enabled': True,
            'workout_reminders': True,
            'progress_updates': True,
            'motivation_messages': True,
            'frequency': 'daily'
        }

def add_notification(message, type="info", expiry_minutes=5):
    """
    Aggiunge una notifica al sistema
    
    Args:
        message (str): Messaggio della notifica
        type (str): Tipo di notifica (info, success, warning, error)
        expiry_minutes (int): Minuti dopo i quali la notifica scade
    """
    if 'notifications' not in st.session_state:
        setup_notification_system()
    
    # Crea una nuova notifica
    notification = {
        'id': random.randint(10000, 99999),
        'message': message,
        'type': type,
        'created': datetime.datetime.now(),
        'expiry': datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes),
        'read': False
    }
    
    # Aggiungi la notifica all'elenco
    st.session_state.notifications.append(notification)

def get_notifications(include_read=False):
    """
    Ottiene le notifiche attive
    
    Args:
        include_read (bool): Includere le notifiche già lette
        
    Returns:
        list: Lista di notifiche attive
    """
    if 'notifications' not in st.session_state:
        setup_notification_system()
        return []
    
    # Filtra le notifiche scadute e lette
    now = datetime.datetime.now()
    notifications = []
    
    for notification in st.session_state.notifications:
        if notification['expiry'] > now and (include_read or not notification['read']):
            notifications.append(notification)
    
    # Aggiorna la lista delle notifiche rimuovendo quelle scadute
    st.session_state.notifications = [n for n in st.session_state.notifications if n['expiry'] > now]
    
    return notifications

def mark_notification_read(notification_id):
    """
    Marca una notifica come letta
    
    Args:
        notification_id (int): ID della notifica
    """
    if 'notifications' not in st.session_state:
        return
    
    for notification in st.session_state.notifications:
        if notification['id'] == notification_id:
            notification['read'] = True
            break

def generate_workout_reminder():
    """
    Genera un promemoria di allenamento casuale
    """
    phrase = get_random_motivation_phrase()
    add_notification(f"🏋️‍♂️ {phrase}", "info", 60 * 24)  # Scade dopo 24 ore

def show_notifications():
    """
    Mostra le notifiche nell'interfaccia
    """
    notifications = get_notifications()
    
    if not notifications:
        return
    
    with st.sidebar.expander(f"📬 Notifiche ({len(notifications)})", expanded=len(notifications) > 0):
        for notification in notifications:
            col1, col2 = st.columns([5, 1])
            
            with col1:
                if notification['type'] == 'info':
                    st.info(notification['message'])
                elif notification['type'] == 'success':
                    st.success(notification['message'])
                elif notification['type'] == 'warning':
                    st.warning(notification['message'])
                elif notification['type'] == 'error':
                    st.error(notification['message'])
            
            with col2:
                if st.button("✓", key=f"notif_{notification['id']}"):
                    mark_notification_read(notification['id'])
                    st.rerun()
        
        if st.button("🧹 Pulisci Tutto"):
            for notification in notifications:
                mark_notification_read(notification['id'])
            st.rerun()