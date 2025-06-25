# config.py

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# ¡¡¡AJUSTA ESTAS CREDENCIALES A LAS DE TU INSTANCIA DE GOOGLE CLOUD SQL!!!
DB_CONFIG = {
    'host': '173.230.153.11',  # La IP pública de tu instancia de Cloud SQL
    'user': 'Gabohrodriguez',
    'password': 'Loberia690',
    'database': 'AdministracionEdificios',
    'port': 3306              # Puerto estándar de MySQL
}

# --- ESTADOS POSIBLES ---
ESTADOS_POSIBLES = ["Pendiente", "En Progreso", "Completado", "Cancelado", "Revisión"]

# --- PRIORIDADES POSIBLES ---
PRIORIDADES_POSIBLES = ["Baja", "Media", "Alta"]
