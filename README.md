# Sistema de Gestión de Inventario

Este proyecto fue desarrollado como trabajo final para Talento Tech. Consiste en una aplicación de consola en Python que permite administrar el stock de productos de manera eficiente, utilizando una base de datos relacional para la persistencia.

Características principales
- Persistencia de Datos: Uso de SQLite3 para almacenar productos de forma local.
- Operaciones CRUD: 
  - `Crear`: Registro de nuevos productos con validación.
  - `Leer`: Consulta general de stock o búsqueda específica por ID.
  - `Actualizar`: Modificación dinámica de precios, cantidades y detalles.
  - `Eliminar`: Borrado de registros con confirmación de seguridad.
- Reportes Inteligentes: Función integrada para detectar productos con bajo stock.
- Validación: Control de errores para entradas numéricas y campos obligatorios.

Tecnologías utilizadas
- Lenguaje: Python 3.x
- Base de datos: SQLite3
- Librerías: `sqlite3` (estándar de Python)

