# main.py
from config import DB_CONFIG
from db_manager import DatabaseManager
from repositories import (
    ConsorcioRepository, GremioRepository, EstadoRepository,
    DepartamentoRepository, AvanceRepository
)
from input_handler import InputHandler
from job_manager import JobManager
from ui import ConsoleUI

if __name__ == "__main__":
    # --- COMPOSICIÓN DE OBJETOS (Dependency Injection Container simple) ---
    # Aquí es donde se instancian las clases y se inyectan las dependencias.
    # Esto sigue el Principio de Inversión de Dependencias (DIP).

    db_manager = DatabaseManager(DB_CONFIG)

    consorcio_repo = ConsorcioRepository(db_manager)
    gremio_repo = GremioRepository(db_manager)
    estado_repo = EstadoRepository(db_manager)
    departamento_repo = DepartamentoRepository(db_manager)
    avance_repo = AvanceRepository(db_manager)

    input_handler = InputHandler()

    job_manager = JobManager(
        avance_repo=avance_repo,
        consorcio_repo=consorcio_repo,
        gremio_repo=gremio_repo,
        estado_repo=estado_repo,
        departamento_repo=departamento_repo,
        input_handler=input_handler
    )

    console_ui = ConsoleUI(job_manager=job_manager)

    # --- INICIO DE LA APLICACIÓN ---
    try:
        console_ui.run_app()
    finally:
        # Asegurarse de cerrar la conexión a la base de datos al finalizar
        db_manager.close_connection()

