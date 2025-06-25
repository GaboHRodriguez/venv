# ui.py

class ConsoleUI:
    """
    Clase que gestiona la interfaz de usuario de la consola (menús y visualización de resultados).
    Aplica SRP: solo se ocupa de la presentación.
    """
    def __init__(self, job_manager):
        """
        Inicializa la UI con una instancia de JobManager (Inyección de Dependencias).
        """
        self.job_manager = job_manager

    def main_menu(self):
        """Muestra el menú principal de la aplicación."""
        print("\n--- GESTIÓN DE MANTENIMIENTO DE EDIFICIOS ---")
        print("1. Listar Trabajos")
        print("2. Añadir Trabajo")
        print("3. Actualizar Trabajo")
        print("4. Eliminar Trabajo")
        print("5. Salir")

    def run_app(self):
        """Ejecuta el bucle principal de la aplicación de consola."""
        while True:
            self.main_menu()
            choice = input("Seleccione una opción: ")

            if choice == '1':
                self.job_manager.display_jobs()
            elif choice == '2':
                self.job_manager.add_job()
            elif choice == '3':
                self.job_manager.update_job()
            elif choice == '4':
                self.job_manager.delete_job()
            elif choice == '5':
                print("Saliendo de la aplicación. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
