from openpyxl import Workbook
import os

def exportar_excel_inventario(inventario, ruta_salida="inventario.xlsx"):
    """
    Exporta el estado actual del inventario a Excel.
    'inventario' debe ser una lista de diccionarios u objetos de tu BD.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Stock Actual"
    
    # Encabezados de las columnas
    ws.append(["ID", "Nombre del Producto", "Stock Actual", "Stock Mínimo", "Precio"])
    
    # Carga de datos
    for item in inventario:
        # ajustar correctamente con el modelo
        ws.append([
            item['id'], 
            item['nombre'], 
            item['stock'], 
            item['stock_minimo'], 
            item['precio']
        ])
        
    wb.save(ruta_salida)
    return ruta_salida