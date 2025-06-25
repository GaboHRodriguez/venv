# job_manager.py
from datetime import datetime
from repositories import (
    ConsorcioRepository, GremioRepository, EstadoRepository,
    DepartamentoRepository, AvanceRepository
)
from input_handler import InputHandler
from config import ESTADOS_POSIBLES, PRIORIDADES_POSIBLES

class JobManager:
    """
    Clase que contiene la lógica de negocio para gestionar los trabajos de mantenimiento.
    Aplica SRP: solo se ocupa de la lógica de negocio de los trabajos.
    Aplica DIP: depende de las abstracciones de los repositorios y el input_handler,
    no de sus implementaciones concretas directamente.
    """
    def __init__(self,
                 avance_repo: AvanceRepository,
                 consorcio_repo: ConsorcioRepository,
                 gremio_repo: GremioRepository,
                 estado_repo: EstadoRepository,
                 departamento_repo: DepartamentoRepository,
                 input_handler: InputHandler):
        """
        Inicializa el JobManager con las dependencias necesarias (repositorios y input handler).
        Esto es Inyección de Dependencias.
        """
        self.avance_repo = avance_repo
        self.consorcio_repo = consorcio_repo
        self.gremio_repo = gremio_repo
        self.estado_repo = estado_repo
        self.departamento_repo = departamento_repo
        self.input_handler = input_handler

    def display_jobs(self):
        """Muestra todos los trabajos de mantenimiento."""
        jobs = self.avance_repo.get_all_jobs()

        if not jobs:
            print("\nNo hay trabajos de mantenimiento registrados.")
            return

        print("\n--- LISTA DE TRABAJOS DE MANTENIMIENTO ---")
        print("{:<5} {:<30} {:<20} {:<15} {:<15} {:<10} {:<15}".format(
            "ID", "Título", "Edificio/Depto.", "Técnico", "Fecha Límite", "Estado", "Prioridad"))
        print("-" * 120)

        for job in jobs:
            building_dept_info = job['building']
            if job['departmentUnit'] and job['departmentOrder']:
                building_dept_info += f" / {job['departmentUnit']} ({job['departmentOrder']})"
            
            # Reconstruir fecha límite
            dia_fin = job['DiaFin'] if job['DiaFin'] is not None else 'N/A'
            mes_fin = job['MesFin'] if job['MesFin'] is not None else 'N/A'
            anio_fin = job['AnioFin'] if job['AnioFin'] is not None else 'N/A'
            fecha_limite = f"{dia_fin}/{mes_fin}/{anio_fin}" if all(x != 'N/A' for x in [dia_fin, mes_fin, anio_fin]) else 'N/A'

            print("{:<5} {:<30} {:<20} {:<15} {:<15} {:<10} {:<15}".format(
                job['ID'],
                job['Titulo'][:28] + '...' if len(job['Titulo']) > 28 else job['Titulo'],
                building_dept_info[:18] + '...' if len(building_dept_info) > 18 else building_dept_info,
                job['technician'][:13] + '...' if len(job['technician']) > 13 else job['technician'],
                fecha_limite,
                job['status'],
                job['priority']
            ))
        print("-" * 120)

    def add_job(self):
        """Permite al usuario añadir un nuevo trabajo."""
        print("\n--- AÑADIR NUEVO TRABAJO ---")
        titulo = self.input_handler.get_string_input("Título del trabajo: ")
        descripcion = self.input_handler.get_string_input("Descripción: ")

        # --- SELECCIÓN DE EDIFICIO/DEPARTAMENTO ---
        consorcios_disp = self.consorcio_repo.get_all()
        if not consorcios_disp:
            print("No hay consorcios disponibles. Por favor, añada consorcios primero.")
            return

        selected_consorcio_nombre = self.input_handler.get_choice_from_list(
            "\nSeleccione el Edificio (Consorcio):", consorcios_disp
        )
        if not selected_consorcio_nombre:
            return # El input_handler ya maneja el mensaje de error o cancelación
        
        consorcio_id = self.consorcio_repo.get_by_name(selected_consorcio_nombre)
        if not consorcio_id:
            print("Error: No se pudo obtener el ID del consorcio seleccionado.")
            return

        department_id = None
        target_type = self.input_handler.get_string_input("¿Es para un (E)dificio completo o (D)epartamento específico? (E/D): ").upper()
        if target_type == 'D':
            deptos_disp = self.departamento_repo.get_all_by_consorcio(selected_consorcio_nombre)
            if not deptos_disp:
                print(f"No hay departamentos para {selected_consorcio_nombre}. Se asignará al edificio completo.")
            else:
                selected_depto_info = self.input_handler.get_choice_from_list(
                    f"\nDepartamentos en {selected_consorcio_nombre}:",
                    [f"Unidad: {d['Unidad']} (Orden: {d['Orden']}) - {d['dept_nombre']}" for d in deptos_disp]
                )
                if selected_depto_info:
                    # Encuentra el ID del departamento seleccionado
                    for d in deptos_disp:
                        if f"Unidad: {d['Unidad']} (Orden: {d['Orden']}) - {d['dept_nombre']}" == selected_depto_info:
                            department_id = d['ID']
                            break
        
        # --- SELECCIÓN DE TÉCNICO ---
        gremios_disp = self.gremio_repo.get_all()
        if not gremios_disp:
            print("No hay gremios disponibles. Por favor, añada gremios primero.")
            return

        selected_gremio_nombre = self.input_handler.get_choice_from_list(
            "\nSeleccione el Técnico Asignado:", gremios_disp
        )
        if not selected_gremio_nombre:
            return
        gremio_id = self.gremio_repo.get_by_name(selected_gremio_nombre)
        if not gremio_id:
            print("Error: No se pudo obtener el ID del gremio seleccionado.")
            return

        # --- FECHA LÍMITE ---
        dia_fin, mes_fin, anio_fin = self.input_handler.get_date_input("Fecha Límite")
        if dia_fin is None: # Si el usuario lo dejó vacío y allow_empty fuera True, pero aquí no lo es.
            print("Fecha límite es requerida.")
            return

        # --- ESTADO Y PRIORIDAD ---
        status = self.input_handler.get_choice_from_list("\nSeleccione el Estado:", ESTADOS_POSIBLES)
        if not status: return
        estado_id = self.estado_repo.get_by_name(status)
        if not estado_id:
            print("Error: No se pudo obtener el ID del estado seleccionado.")
            return

        priority = self.input_handler.get_choice_from_list("\nSeleccione la Prioridad:", PRIORIDADES_POSIBLES)
        if not priority: return

        # Fecha de inicio (actual)
        fecha_actual = datetime.now()
        dia_ini = fecha_actual.day
        mes_ini = fecha_actual.month
        anio_ini = fecha_actual.year

        job_data = {
            'DiaIni': dia_ini, 'MesIni': mes_ini, 'AnioIni': anio_ini,
            'Consorcio_FK': consorcio_id, 'Departamento_FK': department_id,
            'Titulo': titulo, 'Descripcion': descripcion, 'Gremio_FK': gremio_id,
            'DiaFin': dia_fin, 'MesFin': mes_fin, 'AnioFin': anio_fin,
            'Estado_FK': estado_id, 'Prioridad': priority
        }

        if self.avance_repo.add_job(job_data):
            print("\nTrabajo añadido exitosamente.")
        else:
            print("\nError: No se pudo añadir el trabajo.")

    def update_job(self):
        """Permite al usuario actualizar un trabajo existente."""
        job_id = self.input_handler.get_string_input("\nIngrese el ID del trabajo a actualizar: ")
        job_existente = self.avance_repo.get_job_by_id(job_id)

        if not job_existente:
            print(f"No se encontró ningún trabajo con ID {job_id}.")
            return
        
        print("\n--- ACTUALIZAR TRABAJO ---")
        print(f"Trabajo actual: Título '{job_existente['Titulo']}', Descripción '{job_existente['Descripcion']}'")

        # Recopilar datos actualizados
        titulo = self.input_handler.get_string_input(f"Nuevo título", default_value=job_existente['Titulo'])
        descripcion = self.input_handler.get_string_input(f"Nueva descripción", default_value=job_existente['Descripcion'])

        # --- SELECCIÓN DE EDIFICIO/DEPARTAMENTO ---
        current_consorcio_nombre = self.consorcio_repo.get_name_by_id(job_existente['Consorcio_FK'])
        consorcios_disp = self.consorcio_repo.get_all()
        selected_consorcio_nombre = self.input_handler.get_choice_from_list(
            "\nSeleccione el nuevo Edificio (Consorcio):", consorcios_disp,
            current_selection=current_consorcio_nombre, allow_empty=True
        )
        # Si el usuario no ingresa nada, se mantiene el actual
        if selected_consorcio_nombre is None:
            selected_consorcio_nombre = current_consorcio_nombre
            consorcio_id = job_existente['Consorcio_FK']
        else:
            consorcio_id = self.consorcio_repo.get_by_name(selected_consorcio_nombre)
            if not consorcio_id:
                print("Error: No se pudo obtener el ID del consorcio seleccionado para actualizar.")
                return

        department_id = job_existente['Departamento_FK'] # Mantener el actual por defecto
        
        current_target_type = 'D' if department_id else 'E'
        target_type_str = self.input_handler.get_string_input(
            f"¿Es para (E)dificio completo o (D)epartamento específico?",
            default_value=current_target_type
        ).upper()

        if target_type_str == 'E':
            department_id = None
        elif target_type_str == 'D':
            deptos_disp = self.departamento_repo.get_all_by_consorcio(selected_consorcio_nombre)
            if not deptos_disp:
                print(f"No hay departamentos para {selected_consorcio_nombre}. Se asignará al edificio completo.")
                department_id = None
            else:
                current_depto_info = None
                if job_existente['Departamento_FK']:
                    # Reconstruir la información del departamento actual para mostrarla
                    for d in deptos_disp:
                        if d['ID'] == job_existente['Departamento_FK']:
                            current_depto_info = f"Unidad: {d['Unidad']} (Orden: {d['Orden']}) - {d['dept_nombre']}"
                            break

                selected_depto_info = self.input_handler.get_choice_from_list(
                    f"\nDepartamentos en {selected_consorcio_nombre}:",
                    [f"Unidad: {d['Unidad']} (Orden: {d['Orden']}) - {d['dept_nombre']}" for d in deptos_disp],
                    current_selection=current_depto_info,
                    allow_empty=True
                )
                if selected_depto_info is None:
                    # Si el usuario no cambió, se mantiene el ID depto original
                    pass
                else:
                    for d in deptos_disp:
                        if f"Unidad: {d['Unidad']} (Orden: {d['Orden']}) - {d['dept_nombre']}" == selected_depto_info:
                            department_id = d['ID']
                            break
        else:
            print("Opción no válida. Se mantendrá el tipo de objetivo actual.")

        # --- SELECCIÓN DE TÉCNICO ---
        current_gremio_nombre = self.gremio_repo.get_name_by_id(job_existente['Gremio_FK'])
        gremios_disp = self.gremio_repo.get_all()
        selected_gremio_nombre = self.input_handler.get_choice_from_list(
            "\nSeleccione el nuevo Técnico Asignado:", gremios_disp,
            current_selection=current_gremio_nombre, allow_empty=True
        )
        if selected_gremio_nombre is None:
            selected_gremio_nombre = current_gremio_nombre
            gremio_id = job_existente['Gremio_FK']
        else:
            gremio_id = self.gremio_repo.get_by_name(selected_gremio_nombre)
            if not gremio_id:
                print("Error: No se pudo obtener el ID del gremio seleccionado para actualizar.")
                return

        # --- FECHA LÍMITE ---
        current_date_obj = None
        if job_existente['AnioFin'] and job_existente['MesFin'] and job_existente['DiaFin']:
            try:
                current_date_obj = datetime(job_existente['AnioFin'], job_existente['MesFin'], job_existente['DiaFin']).date()
            except ValueError:
                current_date_obj = None # En caso de fecha inválida en DB

        dia_fin, mes_fin, anio_fin = self.input_handler.get_date_input(
            "Nueva Fecha Límite",
            current_date=current_date_obj,
            allow_empty=True
        )
        if dia_fin is None: # Si el usuario dejó vacío, mantiene los valores existentes
            dia_fin = job_existente['DiaFin']
            mes_fin = job_existente['MesFin']
            anio_fin = job_existente['AnioFin']

        # --- ESTADO Y PRIORIDAD ---
        current_estado_nombre = self.estado_repo.get_name_by_id(job_existente['Estado_FK'])
        status = self.input_handler.get_choice_from_list(
            "\nSeleccione el nuevo Estado:", ESTADOS_POSIBLES,
            current_selection=current_estado_nombre, allow_empty=True
        )
        if status is None:
            status = current_estado_nombre
            estado_id = job_existente['Estado_FK']
        else:
            estado_id = self.estado_repo.get_by_name(status)
            if not estado_id:
                print("Error: No se pudo obtener el ID del estado seleccionado para actualizar.")
                return

        current_priority = job_existente['Prioridad']
        priority = self.input_handler.get_choice_from_list(
            "\nSeleccione la nueva Prioridad:", PRIORIDADES_POSIBLES,
            current_selection=current_priority, allow_empty=True
        )
        if priority is None:
            priority = current_priority


        job_data = {
            'Titulo': titulo, 'Descripcion': descripcion,
            'DiaFin': dia_fin, 'MesFin': mes_fin, 'AnioFin': anio_fin,
            'Consorcio_FK': consorcio_id, 'Departamento_FK': department_id,
            'Gremio_FK': gremio_id, 'Estado_FK': estado_id, 'Prioridad': priority
        }

        if self.avance_repo.update_job(job_id, job_data):
            print("\nTrabajo actualizado exitosamente.")
        else:
            print("\nNo se realizaron cambios o el trabajo no existe.")

    def delete_job(self):
        """Permite al usuario eliminar un trabajo."""
        job_id = self.input_handler.get_string_input("\nIngrese el ID del trabajo a eliminar: ")
        
        confirmacion = self.input_handler.get_yes_no_confirmation(f"¿Está seguro de eliminar el trabajo con ID {job_id}?")
        
        if confirmacion:
            if self.avance_repo.delete_job(job_id):
                print(f"Trabajo con ID {job_id} eliminado exitosamente.")
            else:
                print(f"No se encontró ningún trabajo con ID {job_id} o hubo un error al eliminar.")
        else:
            print("Eliminación cancelada.")
