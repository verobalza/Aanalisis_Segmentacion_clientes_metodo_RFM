import pandas as pd

#calculamos con el metodo RFM (RECENCIA, FRECUENCIA, MONEDA) la segmentacion de nuestros clientes

#cargamos el archivo
archivo = pd.read_csv('ventas_limpio.csv')

#como utilizaremos el id_fecha y es un objeto convertimos a fecha 
archivo['fecha_venta'] = pd.to_datetime(archivo['fecha_venta'], format='%d/%m/%Y')

#Recencia
fecha_referencia = archivo['fecha_venta'].max()

#Agrupar por cliente 
rfm = archivo.groupby(['id_cliente','nombre_cliente']).agg({
    'id_venta': 'count',
    'fecha_venta': lambda x:(fecha_referencia - x.max()).days,
    'importe_total':'sum',
  
}).reset_index()

rfm.columns = ['id_cliente', 'nombre_cliente','frecuencia','recencia','moneda']
def segmentacion_cliente(fila):
    if fila['frecuencia']> 30 and fila['recencia']<= 30 and fila['moneda']>100000:
        return "Cliente Leal"
    elif fila['frecuencia']> 20 and fila['recencia']<= 60 and fila['moneda']>50000:
        return 'Cliente de alto Valor'
    elif fila['frecuencia']> 20 and fila['recencia']<= 90 and fila['moneda']>30000:
        return 'Cliente frecuente'
    elif fila['frecuencia']> 10 and fila['recencia']<= 30 and fila['moneda']>20000:
        return 'Cliente potencial'
    elif fila['frecuencia']<= 10 and fila['recencia']> 90 and fila['moneda']<= 20000:
        return ' Cliente con riesgo a abandonar'
    elif fila['frecuencia']<= 10 and fila['recencia']> 180 and fila['moneda']<=10000:
        return 'Cliente perdido'
    else:
        return 'Otro'

#agregamos una columna y aplicamos la funcion y le decimos con axis=1 que trabaje en las columnas 

rfm['segmentacion'] =rfm.apply(segmentacion_cliente, axis=1)

#convertimos en csv y le decimos que queremos 2 decimales
rfm.to_csv('clientes_segmentados.csv', index=False, float_format='%.2f')