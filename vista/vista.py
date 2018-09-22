from tkinter import *
from tkinter import ttk
from logica.calculo import Calculo
from logica.gestorArchivo import GestorArchivo

class Vista:

    Superllave = None
    llaveUnica = None
    es2Forma = None
    es3Forma = None
    objCalculo = None
    esArchivo = False
    conjuntoArchivoL=None
    conjuntoTArchivo=None
    conjuntoV=None

    def __init__(self):
        self.window = Tk()
        self.window.title ("Recubrimiento minimo y Calculo de llaves")
        self.window.geometry ('1300x500')

        # Declarar variables de control

        self.conjunto_in = StringVar(value='')
        self.t_elementales = StringVar(value='')
        self.t_extranos = StringVar(value='')
        self.total = StringVar(value='')
        self.extranos = StringVar(value='')
        self.redundantes = StringVar(value='')
        self.z = StringVar(value='')
        self.w = StringVar(value='')
        self.v = StringVar(value='')
        self.is_superllave = StringVar(value='')
        self.conjunto_T = StringVar(value='')

        self.label_T = ttk.Label(self.window, text="CONJUNTO T: ").grid(row=0,column=0)
        self.input_T = ttk.Entry(self.window, textvariable=self.conjunto_T).grid(row=0,column=1)

        self.label_T = ttk.Label (self.window, text="CONJUNTO T: ").grid (row=0, column=3)
        self.txtJSON = ttk.Entry (self.window, width=50)
        self.txtJSON.grid (row=1, column=3)

        self.l_label = ttk.Label(self.window, text="CONJUNTO L: ").grid(row=1,column=0)
        self.l_input = ttk.Entry(self.window, textvariable=self.conjunto_in).grid(row=1,column=1)

        self.l_label_elem = ttk.Label(self.window, text="CONJUNTO L1: ").grid(row=2,column=0)
        self.etiq_elem = ttk.Label(self.window,width=30,textvariable=self.t_elementales,foreground="black",
                                   borderwidth=5).grid(row=2,column=1)

        self.label_reducciones = ttk.Label(self.window, textvariable=self.extranos).grid(row=3,column=0)

        self.label_extranos = ttk.Label(self.window, text="CONJUNTO L2:").grid(row=4,column=0)

        self.etiq_extranos = ttk.Label(self.window,width=30, textvariable=self.t_extranos,foreground="black",
                                       borderwidth=5).grid(row=4,column=1)

        self.label_redundantes = ttk.Label(self.window,width=30, textvariable=self.redundantes).grid(row=5,column=0)

        self.etiq5 = ttk.Label(self.window, text="CONJUNTO L3: ").grid(row=6,column=0)
        self.etiq6 = ttk.Label(self.window,width=30, textvariable=self.total,foreground="black",
                               borderwidth=5).grid(row=6,column=1)

        self.separ1 = ttk.Separator(self.window, orient=VERTICAL).grid(row=7,column=0)
        self.separ2 = ttk.Separator(self.window, orient=VERTICAL).grid(row=8,column=0)
        self.separ3 = ttk.Separator(self.window, orient=VERTICAL).grid(row=9,column=0)

        self.label_llaves_z = ttk.Label(self.window, text="Cierre Z:").grid(row=10,column=0)
        self.label_llaves_z_1 = ttk.Label(self.window,width=30, textvariable=self.z,foreground="BLACK", borderwidth=5).grid(row=10,column=1)

        self.label_is_superllave = ttk.Label(self.window, textvariable=self.is_superllave).grid(row=11,column=0)

        self.label_llaves_v = ttk.Label(self.window, text="CONJUNTO V (Posibles):").grid(row=12,column=0)
        self.label_llaves_v_1 = ttk.Label(self.window,width=30, textvariable=self.v).grid(row=12,column=1)

        self.label_llaves_w = ttk.Label(self.window, text="CONJUNTO W (Nunca):").grid(row=13,column=0)
        self.label_llaves_w_1 = ttk.Label(self.window,width=30, textvariable=self.w).grid(row=13,column=1)


        self.cancelar = ttk.Button(self.window, text="SALIR",command=quit).grid(row=16,column=0)
        self.cargarArchivo = ttk.Button (self.window, text="LEER DESDE ARCHIVO", command=self.CargarArchivo).grid (row=3, column=2)
        self.Nocargar= ttk.Button (self.window, text="LEER DATOS INGRESADOS", command=self.NoCargarArchivo).grid (row=3,
                                                                                                          column=3)
        self.btn2Forma = ttk.Button (self.window,text="2f normal",command=self.verificar2Forma).grid (row=16,column=1)
        self.btn3Forma = ttk.Button (self.window, text="3forma normal", command=self.verificar3Forma).grid(row=16,column=2)
        self.btnBCForma = ttk.Button (self.window, text="BCforma normal", command=self.verificarBCForma).grid(row=16,column=3)
        self.calcular = ttk.Button(self.window,text="EJECUTAR",command=self.calcular).grid(row=16,column=4)

        self.window.mainloop()

    def NoCargarArchivo( self ):
        self.esArchivo = False
    def CargarArchivo( self):
        # lee el dato del archivo
        gestor = GestorArchivo()
        rutaJSON = self.txtJSON.get()
        datos = gestor.LeerArchivo (rutaJSON)
        print (datos)
        self.conjuntoTArchivo=datos['T']
        self.conjuntoArchivoL=datos['L']
        self.esArchivo=True
        print("L es ",self.conjunto_in)

    def verificarBCForma( self ):
        ##Si la relaci{on R desppues de la descomposici{on se halla una superllave se concluye que la relacion
        ##esta en forma Boyce Codd}}
        self.esbcForma = True
        if self.Superllave == False:
            self.esbcForma = False
            self.label_esbcForma = ttk.Label (text="El conjunto dado no se encuentra en BOYCE CODD forma Normal").grid(row=18,column=0)
        else:
            self.label_esbcForma = ttk.Label (text="El conjunto dado se encuentra en BOYCE CODD forma Normal").grid(row=18,column=0)


    def verificar3Forma( self ):
        # Si en la relacion R una vez se realiza el cierre de z no se obtiene la super llave pero si llaves candidatas ,
        self.es3Forma = True
        if self.Superllave == False:
            self.es3Forma = False
            self.label_es3Forma = ttk.Label (text="No se encuentra en tercera forma Normal").grid(row=19,column=0)
        else:
            self.label_es3Forma = ttk.Label (text="Se encuentra en tercera forma Normal").grid(row=19,column=0)

    def verificar2Forma( self ):
        if self.Superllave == True and len(self.conjuntoV)>=1:
            self.es2Forma = False
            self.label_es2Forma = ttk.Label(text="No se encuentra en segunda forma Normal").grid(row=20,column=0)
        else:
            self.es2Forma = True
            self.label_es2Forma = ttk.Label (text="La relacion R se encuentra en segunda forma Normal").grid(row=20,column=0)

    def calcular(self):
        print("t", self.conjunto_T)
        calculo = Calculo()
        self.objCalculo=calculo
        error_dato = False
        total = 0
        try:
            if self.esArchivo==True:
                conjunto_l= self.conjuntoArchivoL
            else:
                conjunto_l = str(self.conjunto_in.get())
        except Exception as e:
            error_dato = True
            print("error",str(e))

        if not error_dato:
            calculo.calcular_cubrimiento(conjunto_l)
            localT=None
            if self.esArchivo==True:
                localT= self.conjuntoTArchivo
            else:
                localT= self.conjunto_T.get()

            Z, is_superkey, W, V, cierreZ = calculo.calcular_llaves (localT, calculo.implicantes_L3,
                                                                     calculo.implicados_L3)
            self.conjuntoV=V
            self.Superllave=is_superkey
            self.llaveUnica=cierreZ
            self.t_elementales.set(calculo.obtener_elementales())
            self.extranos.set(calculo.obtener_extranos())
            self.t_extranos.set(calculo.obtener_l1())
            self.redundantes.set(calculo.obtener_redundantes())
            self.total.set(calculo.obtener_l2())

            self.z.set(Z)
            if is_superkey:
                self.is_superllave = "Z es superllave"
            else:
                self.is_superllave = ""

            self.v.set(V)
            self.w.set(W)
            print("calculo", calculo.obtener_l2())
        else:
            self.total.set("¡ERROR!")

def main():
    mi_app = Vista()
    return 0

if __name__ == '__main__':
    main()