# -------------------------------
# Agenda de contactos con POO
# -------------------------------

# Decorador para convertir un listado de contactos en HTML
def formatear_html(funcion_original):
    """
    Decorador sencillo:
    - Llama a la función original (que devuelve una lista de contactos)
    - Convierte esa lista en un texto con formato HTML
    """
    def nueva_funcion(*args, **kwargs):
        contactos = funcion_original(*args, **kwargs)  # obtenemos la lista de contactos

        # Empezamos a construir el texto HTML en una variable
        html = "<html>\n"
        html += "<head><title>Agenda</title></head>\n"
        html += "<body>\n"
        html += "<h1>Agenda de contactos</h1>\n"

        if not contactos:
            # Si la lista está vacía
            html += "<p>No hay contactos en la agenda.</p>\n"
        else:
            # Creamos una tabla sencilla con los datos
            html += "<table border='1'>\n"
            html += "<tr><th>Nombre</th><th>Teléfono</th><th>Dirección</th><th>Email</th></tr>\n"

            for c in contactos:
                html += "<tr>"
                html += f"<td>{c.nombre}</td>"
                html += f"<td>{c.telefono}</td>"
                html += f"<td>{c.direccion}</td>"
                # El email puede estar vacío, por eso usamos "or ''"
                html += f"<td>{c.email or ''}</td>"
                html += "</tr>\n"

            html += "</table>\n"

        html += "</body>\n"
        html += "</html>"

        # Devolvemos el HTML final
        return html

    return nueva_funcion


class Persona:
    """
    Clase básica para una persona.
    Solo guarda nombre y email.
    """
    def __init__(self, nombre, email=None):
        self.nombre = nombre
        self.email = email

    def __str__(self):
        # Texto que se muestra cuando hacemos print(persona)
        if self.email:
            return f"{self.nombre} ({self.email})"
        else:
            return self.nombre


class Contacto(Persona):
    """
    Contacto hereda de Persona.
    Además del nombre y el email, tiene teléfono y dirección.
    """
    def __init__(self, nombre, telefono, direccion, email=None):
        # Llamamos al constructor de Persona
        super().__init__(nombre, email)
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        # Texto que se muestra cuando hacemos print(contacto)
        base = super().__str__()
        return f"{base} - Tel: {self.telefono}, Dir: {self.direccion}"


class Agenda:
    """
    Clase Agenda.
    Guarda una lista de contactos y permite:
    - alta
    - baja
    - modificación
    - listado
    - búsqueda
    """
    def __init__(self):
        # Usamos una lista simple para guardar los contactos
        self.contactos = []

    # ---------- ALTAS ----------

    def alta_contacto(self, contacto):
        """
        Añade un contacto a la agenda.
        No dejamos que se repita el mismo nombre.
        """
        # Comprobamos si ya existe un contacto con ese nombre
        for c in self.contactos:
            if c.nombre == contacto.nombre:
                print(f"Ya existe un contacto con el nombre: {contacto.nombre}")
                return

        self.contactos.append(contacto)
        print(f"Contacto '{contacto.nombre}' añadido correctamente.")

    # ---------- BAJAS ----------

    def baja_contacto(self, nombre):
        """
        Elimina un contacto de la agenda por su nombre.
        """
        for c in self.contactos:
            if c.nombre == nombre:
                self.contactos.remove(c)
                print(f"Contacto '{nombre}' eliminado.")
                return

        print(f"No se encontró un contacto con el nombre: {nombre}")

    # ---------- MODIFICACIÓN ----------

    def modificar_contacto(self, nombre, nuevo_telefono=None, nueva_direccion=None, nuevo_email=None):
        """
        Modifica los datos de un contacto.
        Solo cambia los campos que reciban un valor.
        """
        for c in self.contactos:
            if c.nombre == nombre:
                if nuevo_telefono is not None:
                    c.telefono = nuevo_telefono
                if nueva_direccion is not None:
                    c.direccion = nueva_direccion
                if nuevo_email is not None:
                    c.email = nuevo_email

                print(f"Contacto '{nombre}' modificado.")
                return

        print(f"No se encontró un contacto con el nombre: {nombre}")

    # ---------- BÚSQUEDA ----------

    def buscar_contactos(self, texto):
        """
        Busca contactos cuyo nombre contenga el texto.
        Devuelve una lista con los contactos encontrados.
        """
        texto = texto.lower()
        resultado = []

        for c in self.contactos:
            if texto in c.nombre.lower():
                resultado.append(c)

        return resultado

    # ---------- LISTADO (DECORADO) ----------

    @formatear_html
    def listado_contactos(self):
        """
        Devuelve la lista de contactos ordenada por nombre.
        El decorador la convertirá en HTML.
        """
        # Ordenamos por nombre para que el listado sea más claro
        return sorted(self.contactos, key=lambda c: c.nombre.lower())


# --------------------------------------------------
# Ejemplo de uso de la agenda (puedes cambiarlo)
# --------------------------------------------------
if __name__ == "__main__":
    # Creamos una agenda vacía
    agenda = Agenda()

    # Alta de algunos contactos
    c1 = Contacto("Ana", "600111111", "Calle Uno 1", "ana@example.com")
    c2 = Contacto("Luis", "600222222", "Calle Dos 2")
    c3 = Contacto("María", "600333333", "Calle Tres 3", "maria@example.com")

    agenda.alta_contacto(c1)
    agenda.alta_contacto(c2)
    agenda.alta_contacto(c3)

    # Modificamos un contacto
    agenda.modificar_contacto("Luis", nuevo_telefono="699999999")

    # Borramos un contacto
    agenda.baja_contacto("Ana")

    # Buscamos contactos que contengan "ar" en el nombre
    encontrados = agenda.buscar_contactos("ar")
    print("Resultados de la búsqueda 'ar':")
    for c in encontrados:
        print(" -", c)

    # Obtenemos el listado en HTML
    html = agenda.listado_contactos()
    print("\n--- Listado en HTML ---")
    print(html)

    # Si quieres, puedes guardar el HTML en un archivo:
    with open("listado_agenda.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nSe ha guardado el listado en 'listado_agenda.html'")
