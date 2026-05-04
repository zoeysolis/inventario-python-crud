"""
Sistema de Gestión de Inventario (Talento Tech)
-----------------------------------------------
Autor: Zoe Solis
Descripción: CRUD completo para administración de stock utilizando Python y SQLite3.
Características: Validación de datos, reportes de bajo stock y persistencia en DB.
"""

import sqlite3

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA BASE DE DATOS
# ---------------------------------------------------------

def conectar():
    """Establece conexión con la base de datos."""
    return sqlite3.connect("inventario.db")

def crear_base_datos():
    """Crea la tabla de productos si no existe al iniciar el programa."""
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
        """)
        conexion.commit()

# ---------------------------------------------------------
# FUNCIONES DE LÓGICA DE NEGOCIO
# ---------------------------------------------------------

def agregar_producto():
    print("\n--- ➕ Agregar nuevo producto ---")
    nombre = input("Nombre: ").strip()
    while not nombre:
        print("❌ El nombre no puede estar vacío.")
        nombre = input("Nombre: ").strip()

    descripcion = input("Descripción: ").strip()

    while True:
        cant_in = input("Cantidad disponible: ").strip()
        if cant_in.isdigit():
            cantidad = int(cant_in)
            break
        print("❌ Ingresá un número entero válido.")

    while True:
        prec_in = input("Precio (ej: 250.75): ").strip()
        try:
            precio = float(prec_in)
            break
        except ValueError:
            print("❌ Ingresá un número decimal válido.")

    categoria = input("Categoría: ").strip()

    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) 
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, categoria))
    
    print(f"\n✅ Producto '{nombre}' agregado correctamente.")

def mostrar_productos():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

    if not productos:
        print("\n📭 No hay productos registrados.")
    else:
        print("\n--- 📋 Lista de productos ---")
        for p in productos:
            print(f"ID: {p[0]} | {p[1]} | Stock: {p[3]} | ${p[4]} | Cat: {p[5]}")

def buscar_por_id():
    print("\n--- 🔍 Buscar producto por ID ---")
    id_buscar = input("ID del producto: ").strip()
    if not id_buscar.isdigit():
        print("❌ ID inválido.")
        return

    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_buscar,))
        producto = cursor.fetchone()

    if producto:
        print(f"\n✅ Encontrado: {producto[1]} | Stock: {producto[3]} | Precio: ${producto[4]}")
    else:
        print("❌ No se encontró un producto con ese ID.")

def eliminar_producto():
    print("\n--- 🗑️ Eliminar producto ---")
    id_eliminar = input("ID del producto a eliminar: ").strip()
    if not id_eliminar.isdigit():
        print("❌ ID inválido.")
        return

    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_eliminar,))
        producto = cursor.fetchone()

        if producto:
            confirm = input(f"⚠️ ¿Eliminar '{producto[1]}'? (s/n): ").lower()
            if confirm == 's':
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_eliminar,))
                print("✅ Producto eliminado.")
        else:
            print("❌ No existe el ID.")

def actualizar_producto():
    print("\n--- 🔄 Actualizar producto ---")
    id_act = input("ID del producto: ").strip()
    if not id_act.isdigit(): return

    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_act,))
        p = cursor.fetchone()

        if p:
            nombre = input(f"Nuevo nombre [{p[1]}]: ").strip() or p[1]
            desc = input(f"Nueva desc [{p[2]}]: ").strip() or p[2]
            cant = input(f"Nueva cant [{p[3]}]: ").strip()
            cant = int(cant) if cant.isdigit() else p[3]
            prec = input(f"Nuevo precio [{p[4]}]: ").strip()
            try: prec = float(prec)
            except: prec = p[4]
            cat = input(f"Nueva cat [{p[5]}]: ").strip() or p[5]

            cursor.execute("""
                UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=?
                WHERE id=?
            """, (nombre, desc, cant, prec, cat, id_act))
            print("✅ Actualizado con éxito.")
        else:
            print("❌ ID no encontrado.")

def reporte_bajo_stock():
    print("\n--- 📉 Reporte de Stock Bajo ---")
    limite = input("Límite de alerta: ").strip()
    if not limite.isdigit(): return

    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        prods = cursor.fetchall()

    if prods:
        for p in prods:
            print(f"⚠️ ALERTA: {p[1]} - Quedan: {p[3]}")
    else:
        print("✅ Todo el stock está por encima del límite.")

# ---------------------------------------------------------
# INTERFAZ Y MENÚ
# ---------------------------------------------------------

def main():
    crear_base_datos()
    while True:
        print("\n" + "="*30)
        print("  GESTIÓN DE INVENTARIO - AFRODITA") # Un guiño a tu estética
        print("="*30)
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Buscar por ID")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Reporte bajo stock")
        print("7. Salir")
        
        op = input("\nElegí una opción: ").strip()

        if op == "1": agregar_producto()
        elif op == "2": mostrar_productos()
        elif op == "3": buscar_por_id()
        elif op == "4": actualizar_producto()
        elif op == "5": eliminar_producto()
        elif op == "6": reporte_bajo_stock()
        elif op == "7":
            print("¡Nos vemos, Zoe!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
