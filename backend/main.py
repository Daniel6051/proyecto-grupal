from base_datos.conexion import crear_base_datos
import modelos.producto
import modelos.usuario
import modelos.venta
import modelos.proveedor

from base_datos.repositorios import (
    crear_producto,
    listar_productos,
    buscar_producto_por_id,
    actualizar_stock,
    eliminar_producto
)


if __name__ == "__main__":
    print("Creando base de datos...")
    crear_base_datos()

    print("\nCreando producto...")
    producto = crear_producto("Yerba Mate", "Alimentos", 2500, 15)

    print("Producto creado:")
    print(producto)

    print("\nBuscando producto por ID...")
    encontrado = buscar_producto_por_id(producto.id)
    print(encontrado)

    print("\nActualizando stock...")
    actualizado = actualizar_stock(producto.id, 30)
    print(actualizado)

    print("\nListado de productos:")
    productos = listar_productos()
    for p in productos:
        print(p)

    print("\nEliminando producto...")
    eliminado = eliminar_producto(producto.id)
    print("Eliminado:", eliminado)

    print("\nTodo funcionando correctamente")

    from base_datos.repositorios import crear_usuario, buscar_usuario

    print("\nCreando usuario...")
    user = crear_usuario("admin", "1234", "administrador")
    print(user)

    print("\nBuscando usuario...")
    encontrado = buscar_usuario("admin")
    print(encontrado)

    from base_datos.repositorios import crear_venta

    print("\nCreando venta...")
    venta = crear_venta(1, 5000)
    print(venta)