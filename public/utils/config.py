import os
import configparser
import json

def load_config():
    """
    Carica la configurazione dell'applicazione dal file config.ini
    
    Returns:
        dict: Configurazione dell'applicazione
    """
    config = configparser.ConfigParser()
    
    # Percorso del file di configurazione
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini')
    
    # Carica la configurazione dal file
    if os.path.exists(config_path):
        config.read(config_path)
    else:
        # Configurazione di default se il file non esiste
        config['app'] = {
            'name': 'NemFit',
            'version': '1.0.0',
            'language': 'it',
            'default_theme': 'light'
        }
        config['features'] = {
            'enable_ai_assistant': 'true',
            'enable_notifications': 'true',
            'enable_avatar': 'true',
            'enable_body_scan': 'true',
            'enable_multilanguage': 'true'
        }
    
    # Converti la configurazione in un dizionario
    config_dict = {section: dict(config[section]) for section in config.sections()}
    
    # Converti valori booleani e liste
    for section in config_dict:
        for key, value in config_dict[section].items():
            if isinstance(value, str):
                if value.lower() in ['true', 'yes', '1']:
                    config_dict[section][key] = True
                elif value.lower() in ['false', 'no', '0']:
                    config_dict[section][key] = False
                elif key == 'motivation_phrases' and value.startswith('[') and value.endswith(']'):
                    try:
                        config_dict[section][key] = json.loads(value)
                    except json.JSONDecodeError:
                        # Fallback se non è un JSON valido
                        config_dict[section][key] = [value.strip('[]')]
    
    return config_dict

def get_supported_languages():
    """
    Restituisce le lingue supportate dall'applicazione
    
    Returns:
        dict: Dizionario delle lingue supportate (codice: nome)
    """
    return {
        'it': 'Italiano',
        'en': 'English',
        'es': 'Español',
        'fr': 'Français',
        'de': 'Deutsch'
    }

def get_random_motivation_phrase():
    """
    Restituisce una frase motivazionale casuale per le notifiche
    
    Returns:
        str: Frase motivazionale
    """
    import random
    config = load_config()
    
    phrases = config.get('notifications', {}).get('motivation_phrases', 
        "È ora di allenarti! I muscoli non crescono sul divano! | Hey! La tua scheda di allenamento si sente trascurata! | Niente scuse oggi, solo risultati!"
    )
    
    if isinstance(phrases, str):
        # Converti in lista se è una stringa con separatore |
        if '|' in phrases:
            phrases = [p.strip() for p in phrases.split('|')]
        else:
            phrases = [phrases]
    
    return random.choice(phrases)