import os
from datetime import datetime

def get_timestamp():
    """Retourne l'heure actuelle au format 'YYYYMMDD_HHmmss'."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def get_video_path(base_dir):
    """Retourne le chemin complet du fichier vidéo à enregistrer."""
    timestamp = get_timestamp()
    filename = f'video_{timestamp}.mp4'
    return os.path.join(base_dir, filename)
