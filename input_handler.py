# input_handler.py
from datetime import datetime

class InputHandler:
    """
    Clase dedicada a manejar todas las entradas de usuario y su validación.
    Aplica SRP: solo se ocupa de la interacción de entrada.
    """
    def get_string_input(self, prompt, default_value=None):
        """Obtiene una cadena de texto del usuario."""
        if default_value is not None:
            return input(f"{prompt} (actual: {default_value}, dejar vacío para no cambiar): ") or default_value
        return input(prompt)

    def get_choice_from_list(self, prompt_list, available_options, current_selection=None, allow_empty=False):
        """
        Permite al usuario seleccionar una opción de una lista numerada.
        Args:
            prompt_list (str): El mensaje a mostrar antes de listar las opciones.
            available_options (list): Una lista de cadenas de texto con las opciones disponibles.
            current_selection (str, optional): La opción actualmente seleccionada para mostrar como "actual".
            allow_empty (bool, optional): Si se permite al usuario dejar la entrada vacía.
        Returns:
            str: La opción seleccionada o None si se permite vacío y el usuario lo deja así.
        """
        if not available_options:
            print("No hay opciones disponibles.")
            return None

        print(prompt_list)
        for i, opt in enumerate(available_options):
            print(f"{i+1}. {opt}")

        while True:
            try:
                input_prompt = f"Ingrese el número (1-{len(available_options)}"
                if current_selection:
                    input_prompt += f", actual: {current_selection}"
                if allow_empty:
                    input_prompt += ", dejar vacío para no cambiar"
                input_prompt += "): "

                choice_str = input(input_prompt)
                
                if allow_empty and not choice_str:
                    return None # Usuario eligió no cambiar
                
                choice_idx = int(choice_str) - 1
                if 0 <= choice_idx < len(available_options):
                    return available_options[choice_idx]
                else:
                    print("Opción no válida. Intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingrese un número.")

    def get_date_input(self, prompt, current_date=None, allow_empty=False):
        """
        Obtiene una fecha del usuario en formato YYYY-MM-DD.
        Args:
            prompt (str): El mensaje a mostrar al usuario.
            current_date (datetime.date, optional): La fecha actual para mostrar como "actual".
            allow_empty (bool, optional): Si se permite al usuario dejar la entrada vacía.
        Returns:
            tuple: (dia, mes, anio) o (None, None, None) si se permite vacío y el usuario lo deja así.
        """
        while True:
            try:
                display_current = current_date.strftime("%Y-%m-%d") if current_date else ""
                input_prompt = f"{prompt} (YYYY-MM-DD"
                if display_current:
                    input_prompt += f", actual: {display_current}"
                if allow_empty:
                    input_prompt += ", dejar vacío para no cambiar"
                input_prompt += "): "

                fecha_str = input(input_prompt)
                
                if allow_empty and not fecha_str:
                    return None, None, None # Usuario eligió no cambiar
                
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
                return fecha_obj.day, fecha_obj.month, fecha_obj.year
            except ValueError:
                print("Formato de fecha incorrecto. Use YYYY-MM-DD.")

    def get_yes_no_confirmation(self, prompt):
        """Obtiene una confirmación de sí/no del usuario."""
        while True:
            confirmacion = input(f"{prompt} (s/n): ").lower()
            if confirmacion in ('s', 'n'):
                return confirmacion == 's'
            else:
                print("Entrada inválida. Ingrese 's' para sí o 'n' para no.")
