import os
from datetime import datetime
from reportlab.pdfgen import canvas

def generar_pdf_ventas(ventas, ruta_salida="reporte_ventas.pdf"):
    """
    Genera un PDF con el listado de ventas.
    'ventas' debe ser una lista de diccionarios o de objetos de tu base de datos.
    """
    # Aseguramos que el directorio de salida exista si deciden guardarlo en otra carpeta
    os.makedirs(os.path.dirname(ruta_salida) if os.path.dirname(ruta_salida) else '.', exist_ok=True)
    
    c = canvas.Canvas(ruta_salida)
    fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, f"Reporte de Ventas - {fecha_actual}")
    
    c.setFont("Helvetica", 12)
    y = 750
    total_general = 0
    #ajustar correttamente
    for venta in ventas:
        # Ajustá estas claves ('producto', 'cantidad', etc.) según los modelos de tu backend
       # texto = f"Producto: {venta['producto']} | Cant: {venta['cantidad']} | Total: ${venta['total']}"
        #c.drawString(100, y, texto)
        #total_general += float(venta['total'])
        #y -= 20
        
        if y < 50:
            c.showPage()
            y = 800
            
    c.line(100, y, 500, y)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y - 20, f"TOTAL RECAUDADO: ${total_general}")
    
    c.save()
    return ruta_salida