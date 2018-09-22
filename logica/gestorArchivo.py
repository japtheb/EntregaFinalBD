import json


class GestorArchivo:
    mensaje = ''
    datos = {}

    def LeerArchivo( self, ruta ):
        try:
            # lectura de la ruta con los datos
            datos = json.loads (open (ruta).read ())
            return datos

        except:

            print (self.mensaje)
            raiseimport
            json