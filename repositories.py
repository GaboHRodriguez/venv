# repositories.py
import mysql.connector
from abc import ABC, abstractmethod
from db_manager import DatabaseManager

# --- INTERFACES (OPCIONAL, PERO BUENA PRÁCTICA PARA OCP/DIP) ---
# En Python, las interfaces se implementan a menudo con ABCs (Abstract Base Classes)
# o simplemente por "duck typing" (si camina como un pato y grazna como un pato...).
# Para este ejemplo, usaremos ABCs para claridad y para reforzar los principios.

class ConsorcioRepositoryInterface(ABC):
    @abstractmethod
    def get_by_name(self, name):
        pass

    @abstractmethod
    def get_name_by_id(self, consorcio_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

class GremioRepositoryInterface(ABC):
    @abstractmethod
    def get_by_name(self, name):
        pass

    @abstractmethod
    def get_name_by_id(self, gremio_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

class EstadoRepositoryInterface(ABC):
    @abstractmethod
    def get_by_name(self, name):
        pass

    @abstractmethod
    def get_name_by_id(self, estado_id):
        pass

class DepartamentoRepositoryInterface(ABC):
    @abstractmethod
    def get_all_by_consorcio(self, consorcio_name=None):
        pass

class AvanceRepositoryInterface(ABC):
    @abstractmethod
    def get_all_jobs(self):
        pass

    @abstractmethod
    def add_job(self, job_data):
        pass

    @abstractmethod
    def get_job_by_id(self, job_id):
        pass

    @abstractmethod
    def update_job(self, job_id, job_data):
        pass

    @abstractmethod
    def delete_job(self, job_id):
        pass


# --- IMPLEMENTACIONES DE REPOSITORIOS ---

class ConsorcioRepository(ConsorcioRepositoryInterface):
    """
    Gestiona las operaciones de base de datos para la tabla Consorcios.
    Aplica SRP: solo se ocupa de Consorcios.
    Aplica DIP: depende de la abstracción DatabaseManager, no de una conexión directa.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_by_name(self, nombre_consorcio):
        conn = self.db_manager.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Codigo FROM Consorcios WHERE Nombre = %s", (nombre_consorcio,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error al obtener ID de consorcio: {err}")
            return None
        finally:
            cursor.close()

    def get_name_by_id(self, consorcio_id):
        conn = self.db_manager.get_connection()
        if not conn: return "Desconocido"
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Nombre FROM Consorcios WHERE Codigo = %s", (consorcio_id,))
            result = cursor.fetchone()
            return result[0] if result else "Desconocido"
        except mysql.connector.Error as err:
            print(f"Error al obtener nombre de consorcio: {err}")
            return "Desconocido"
        finally:
            cursor.close()

    def get_all(self):
        conn = self.db_manager.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Nombre FROM Consorcios ORDER BY Nombre")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Error al obtener consorcios: {err}")
            return []
        finally:
            cursor.close()


class GremioRepository(GremioRepositoryInterface):
    """
    Gestiona las operaciones de base de datos para la tabla Gremios.
    Aplica SRP y DIP.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_by_name(self, nombre_fantasia_gremio):
        conn = self.db_manager.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Id FROM Gremios WHERE Nombre_Fantasia = %s", (nombre_fantasia_gremio,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error al obtener ID de gremio: {err}")
            return None
        finally:
            cursor.close()

    def get_name_by_id(self, gremio_id):
        conn = self.db_manager.get_connection()
        if not conn: return "Desconocido"
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Nombre_Fantasia FROM Gremios WHERE Id = %s", (gremio_id,))
            result = cursor.fetchone()
            return result[0] if result else "Desconocido"
        except mysql.connector.Error as err:
            print(f"Error al obtener nombre de fantasía de gremio: {err}")
            return "Desconocido"
        finally:
            cursor.close()

    def get_all(self):
        conn = self.db_manager.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Nombre_Fantasia FROM Gremios ORDER BY Nombre_Fantasia")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Error al obtener gremios: {err}")
            return []
        finally:
            cursor.close()


class EstadoRepository(EstadoRepositoryInterface):
    """
    Gestiona las operaciones de base de datos para la tabla Estado.
    Aplica SRP y DIP.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_by_name(self, nombre_estado):
        conn = self.db_manager.get_connection()
        if not conn: return None
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM Estado WHERE Estado = %s", (nombre_estado,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error al obtener ID de estado: {err}")
            return None
        finally:
            cursor.close()

    def get_name_by_id(self, estado_id):
        conn = self.db_manager.get_connection()
        if not conn: return "Desconocido"
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Estado FROM Estado WHERE id = %s", (estado_id,))
            result = cursor.fetchone()
            return result[0] if result else "Desconocido"
        except mysql.connector.Error as err:
            print(f"Error al obtener nombre de estado: {err}")
            return "Desconocido"
        finally:
            cursor.close()


class DepartamentoRepository(DepartamentoRepositoryInterface):
    """
    Gestiona las operaciones de base de datos para la tabla Departamentos.
    Aplica SRP y DIP.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_all_by_consorcio(self, consorcio_nombre=None):
        conn = self.db_manager.get_connection()
        if not conn: return []
        cursor = conn.cursor()
        try:
            query = """
            SELECT
                D.ID, D.Codigo, D.Unidad, D.Orden, D.Nombre AS dept_nombre,
                C.Nombre AS consorcio_nombre, D.Consorcio_FK AS consorcioId
            FROM
                Departamentos D
            JOIN
                Consorcios C ON D.Consorcio_FK = C.Codigo
            """
            params = []
            if consorcio_nombre:
                query += " WHERE C.Nombre = %s"
                params.append(consorcio_nombre)
            query += " ORDER BY C.Nombre, D.Codigo"
            
            cursor.execute(query, tuple(params))
            
            columns = [col[0] for col in cursor.description]
            departments = []
            for row_data in cursor.fetchall():
                departments.append(dict(zip(columns, row_data)))
            return departments
        except mysql.connector.Error as err:
            print(f"Error al obtener departamentos: {err}")
            return []
        finally:
            cursor.close()


class AvanceRepository(AvanceRepositoryInterface):
    """
    Gestiona las operaciones de base de datos para la tabla Avance.
    Aplica SRP y DIP.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_all_jobs(self):
        conn = self.db_manager.get_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True) # Devuelve resultados como diccionarios
        try:
            sql = """
            SELECT
                A.ID,
                A.Titulo,
                A.Descripcion,
                A.DiaFin,
                A.MesFin,
                A.AnioFin,
                A.Prioridad AS priority,
                C.Nombre AS building,
                D.ID AS departmentId,
                D.Unidad AS departmentUnit,
                D.Orden AS departmentOrder,
                G.Nombre_Fantasia AS technician,
                E.Estado AS status
            FROM
                Avance A
            JOIN
                Consorcios C ON A.Consorcio_FK = C.Codigo
            LEFT JOIN
                Departamentos D ON A.Departamento_FK = D.ID
            JOIN
                Gremios G ON A.Gremio_FK = G.Id
            JOIN
                Estado E ON A.Estado_FK = E.id
            ORDER BY
                A.AnioFin DESC, A.MesFin DESC, A.DiaFin DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener trabajos: {err}")
            return []
        finally:
            cursor.close()

    def add_job(self, job_data):
        conn = self.db_manager.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            if job_data.get('Departamento_FK'):
                sql = """
                INSERT INTO Avance (DiaIni, MesIni, AnioIni, Consorcio_FK, Departamento_FK, Titulo, Descripcion, Gremio_FK, DiaFin, MesFin, AnioFin, Estado_FK, Prioridad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    job_data['DiaIni'], job_data['MesIni'], job_data['AnioIni'],
                    job_data['Consorcio_FK'], job_data['Departamento_FK'], job_data['Titulo'],
                    job_data['Descripcion'], job_data['Gremio_FK'], job_data['DiaFin'],
                    job_data['MesFin'], job_data['AnioFin'], job_data['Estado_FK'], job_data['Prioridad']
                )
            else:
                sql = """
                INSERT INTO Avance (DiaIni, MesIni, AnioIni, Consorcio_FK, Titulo, Descripcion, Gremio_FK, DiaFin, MesFin, AnioFin, Estado_FK, Prioridad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    job_data['DiaIni'], job_data['MesIni'], job_data['AnioIni'],
                    job_data['Consorcio_FK'], job_data['Titulo'], job_data['Descripcion'],
                    job_data['Gremio_FK'], job_data['DiaFin'], job_data['MesFin'],
                    job_data['AnioFin'], job_data['Estado_FK'], job_data['Prioridad']
                )
            
            cursor.execute(sql, params)
            self.db_manager.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al añadir trabajo: {err}")
            self.db_manager.rollback()
            return False
        finally:
            cursor.close()

    def get_job_by_id(self, job_id):
        conn = self.db_manager.get_connection()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Avance WHERE ID = %s", (job_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener trabajo por ID: {err}")
            return None
        finally:
            cursor.close()

    def update_job(self, job_id, job_data):
        conn = self.db_manager.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            if job_data.get('Departamento_FK') is None:
                sql = """
                UPDATE Avance
                SET Titulo = %s, Descripcion = %s, DiaFin = %s, MesFin = %s, AnioFin = %s,
                    Consorcio_FK = %s, Departamento_FK = NULL, Gremio_FK = %s, Estado_FK = %s, Prioridad = %s
                WHERE ID = %s
                """
                params = (
                    job_data['Titulo'], job_data['Descripcion'],
                    job_data['DiaFin'], job_data['MesFin'], job_data['AnioFin'],
                    job_data['Consorcio_FK'], job_data['Gremio_FK'], job_data['Estado_FK'],
                    job_data['Prioridad'], job_id
                )
            else:
                sql = """
                UPDATE Avance
                SET Titulo = %s, Descripcion = %s, DiaFin = %s, MesFin = %s, AnioFin = %s,
                    Consorcio_FK = %s, Departamento_FK = %s, Gremio_FK = %s, Estado_FK = %s, Prioridad = %s
                WHERE ID = %s
                """
                params = (
                    job_data['Titulo'], job_data['Descripcion'],
                    job_data['DiaFin'], job_data['MesFin'], job_data['AnioFin'],
                    job_data['Consorcio_FK'], job_data['Departamento_FK'], job_data['Gremio_FK'],
                    job_data['Estado_FK'], job_data['Prioridad'], job_id
                )
            
            cursor.execute(sql, params)
            self.db_manager.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error al actualizar trabajo: {err}")
            self.db_manager.rollback()
            return False
        finally:
            cursor.close()

    def delete_job(self, job_id):
        conn = self.db_manager.get_connection()
        if not conn: return False
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Avance WHERE ID = %s", (job_id,))
            self.db_manager.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error al eliminar trabajo: {err}")
            self.db_manager.rollback()
            return False
        finally:
            cursor.close()

