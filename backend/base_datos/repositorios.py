from backend.base_datos.conexion import SessionLocal
from backend.modelos.producto import Producto

def crear_producto(nombre, categoria, precio, stock, stock_minimo=5):
    session = SessionLocal()

    producto = Producto(
        nombre=nombre,
        categoria=categoria,
        precio=precio,
        stock=stock,
        stock_minimo=stock_minimo
    )

    session.add(producto)
    session.commit()
    session.refresh(producto)
    session.close()

    return producto


def listar_productos():
    session = SessionLocal()
    productos = session.query(Producto).all()
    session.close()

    return productos


def buscar_producto_por_id(id_producto):
    session = SessionLocal()

    producto = session.query(Producto).filter(Producto.id == id_producto).first()

    session.close()

    return producto



def actualizar_stock(id_producto, nuevo_stock):
    session = SessionLocal()

    producto = session.query(Producto).filter(Producto.id == id_producto).first()

    if producto is None:
        session.close()
        return None

    producto.stock = nuevo_stock
    session.commit()
    session.refresh(producto)
    session.close()

    return producto



def eliminar_producto(id_producto):
    session = SessionLocal()

    producto = session.query(Producto).filter(Producto.id == id_producto).first()

    if producto is None:
        session.close()
        return False

    session.delete(producto)
    session.commit()
    session.close()

    return True

from backend.modelos.usuario import Usuario


def crear_usuario(nombre_usuario, password, rol):
    session = SessionLocal()

    usuario = Usuario(
        nombre_usuario=nombre_usuario,
        password=password,
        rol=rol
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    session.close()

    return usuario



def buscar_usuario(nombre_usuario):
    session = SessionLocal()

    usuario = session.query(Usuario).filter(
        Usuario.nombre_usuario == nombre_usuario
    ).first()

    session.close()

    return usuario

from backend.modelos.venta import Venta


def crear_venta(usuario_id, total):
    session = SessionLocal()

    venta = Venta(
        usuario_id=usuario_id,
        total=total
    )

    session.add(venta)
    session.commit()
    session.refresh(venta)
    session.close()

    return venta


def listar_ventas():
    session = SessionLocal()
    ventas = session.query(Venta).all()
    session.close()
    return ventas


from backend.modelos.proveedor import Proveedor


def crear_proveedor(nombre, telefono, email, direccion):
    session = SessionLocal()

    proveedor = Proveedor(
        nombre=nombre,
        telefono=telefono,
        email=email,
        direccion=direccion
    )

    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    session.close()

    return proveedor


def listar_proveedores():
    session = SessionLocal()
    proveedores = session.query(Proveedor).all()
    session.close()
    return proveedores
