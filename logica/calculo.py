import itertools

print ("Inicio")


class Calculo:
    def __init__( self ):

        self.implicante_tmp = ''
        self.implicantes_elem = []
        self.implicados_elem = []
        self.implicantes_L2 = []
        self.implicados_L2 = []
        self.implicantes_L3 = []
        self.implicados_L3 = []
        self.extranos = []
        self.redundantes = []

        # Se hallan los elementos extraños de las dependencias funcionales

    def obtener_extranos( self ):

        return '\n'.join (self.extranos)

        # Se obtiene L1

    def obtener_l1( self ):

        result = ''
        for i, res in enumerate (self.implicantes_L2):
            result = result + self.implicantes_L2[i] + "->" + self.implicados_L2[i] + ", "

        print (result)
        return result

    # Se obtienen los elementales del conjunto
    def obtener_elementales( self ):
        result = ''
        for i, res in enumerate (self.implicantes_elem):
            result = result + self.implicantes_elem[i] + "->" + self.implicados_elem[i] + ", "

        print (result)
        return result

    def obtener_redundantes( self ):
        return '\n'.join (self.redundantes)

    # Se obtiene L2 luego de quitar las redundantes
    def obtener_l2( self ):
        result = ''
        for i, res in enumerate (self.implicantes_L3):
            result = result + self.implicantes_L3[i] + "->" + self.implicados_L3[i] + ", "

        print (result)
        return result

    def obtener_l2_dependences( self ):
        return self.implicantes_L3, self.implicados_L3

    def encontrar_dependencias_elementales( self, conjunto_dependencias, implicantes, implicados ):
        # Se quitan los espacios de los conjuntos de implicates e implicados Luego se guardan en arreglos

        if conjunto_dependencias is not None:
            self.L = conjunto_dependencias
            L = self.L.replace (" ", "")
            dependence_arr = L.split (",")
            implicantes = []
            implicados = []
            for dependence in dependence_arr:
                depend = dependence.split ("->")
                implicantes.append (depend[0])
                implicados.append (depend[1])

        # Se hallan todas dependencias elementales
        for i, elemental in enumerate (implicados):
            if len (elemental) > 1:
                for j in elemental:
                    self.implicantes_elem.append (implicantes[i])
                    self.implicados_elem.append (j)
            else:
                self.implicantes_elem.append (implicantes[i])
                self.implicados_elem.append (implicados[i])

    # En este metodo se calcula el recubrimiento minimo
    def calcular_cubrimiento( self, conjunto_dependencias=None, implicantes=None, implicados=None ):

        self.encontrar_dependencias_elementales (conjunto_dependencias, implicantes, implicados)
        print ("L1: implicantes: ", self.implicantes_elem)
        print ("L1: implicados: ", self.implicados_elem)

        # encontrar atributos extranos en el arreglo de implicantes
        self.encontrar_extranos (self.implicantes_elem, 0, True)
        print ("Los elementos extraños son:", self.extranos)
        print ("L2: implicantes: ", self.implicantes_L2)
        print ("L2: implicados: ", self.implicados_L2)

        # encontrar dependencias redundantes
        self.encontrar_redundantes (self.implicantes_L2, self.implicados_L2)
        print ("L3: implicantes: ", self.implicantes_L3)
        print ("L3: implicantes:", self.implicados_L3)

    # Metodo para encontrar si el descriptor recibido tiene un equivalente en el arreglo de implicantes_elem
    def encontrar_extranos( self, descriptores, pos, flag_pi ):

        __implicantes_temporales = []
        __implicados_temporales = []

        flag_ex = False

        for i, implicante in enumerate (descriptores):

            if len (implicante) > 1:
                self.implicante_tmp = implicante
                combinaciones = self.encontrar_combinaciones (implicante, [len (implicante) - 1])
                print ("combinaciones: ", combinaciones)
                for j, descriptor in enumerate (combinaciones):
                    if flag_ex is False:
                        cierre = self.calcular_algoritmo_cierre (descriptor,
                                                                 self.implicantes_elem, self.implicados_elem)
                        print ("descriptor", descriptor, "cierre", cierre)
                        if flag_pi:
                            implicado = self.implicados_elem[i]
                        else:
                            implicado = self.implicados_elem[pos]

                        if implicado in cierre:
                            print ("extrano encontrado:", implicado, cierre)
                            flag_ex = True
                            self.implicante_tmp = descriptor
                            print ("impltemp", self.implicante_tmp)
                            if len (self.implicante_tmp) > 1:
                                self.encontrar_extranos ([descriptor], i, False)

                if len (descriptores) == len (self.implicados_elem):
                    if flag_ex:
                        print ("extrano", implicante, "reduccion: ", self.implicante_tmp, implicado)
                        self.extranos.append (
                            "Extraño: " + implicante + "->" + implicado + ", Reducción: " + self.implicante_tmp + "->" + implicado)
                        if self.comparador (self.implicante_tmp, implicado):
                            __implicantes_temporales.append (self.implicante_tmp)
                            __implicados_temporales.append (implicado)
                        flag_ex = False

                    else:
                        __implicantes_temporales.append (self.implicante_tmp)
                        __implicados_temporales.append (implicado)
            else:
                __implicantes_temporales.append (self.implicantes_elem[i])
                __implicados_temporales.append (self.implicados_elem[i])

        self.implicantes_L2 = __implicantes_temporales
        self.implicados_L2 = __implicados_temporales

    def calcular_algoritmo_cierre( self, descriptor, implicante_p, implicado_p ):

        # Metodo para encontrar el cierre
        cierre = descriptor
        flag = True
        result_arr = []
        while flag:
            combinaciones = self.encontrar_combinaciones (list (descriptor), range (1, len (list (descriptor)) + 1))
            for combinacion in combinaciones:
                cierre = cierre + self.encontrar (combinacion, implicante_p, implicado_p)

            cierr_arr = list (set (cierre))
            cierr_arr.sort ()
            cierre = ''.join (cierr_arr)
            result_arr.append ((descriptor, cierre))
            if descriptor != cierre:
                descriptor = cierre
            else:
                flag = False

        return cierre

    def encontrar( self, implicante, implicante_p, implicado_p ):

        result = ''
        for i, implic in enumerate (implicante_p):
            if implic == implicante:
                result = result + implicado_p[i]

        return result

    def comparador( self, implicante, implicado ):

        # Retorna una bandera por si encontro la misma combinacion implicado,implicante

        result = True
        for j, valor in enumerate (self.implicantes_elem):
            if implicante == valor:
                if implicado == self.implicados_elem[j]:
                    result = False
                    break

        return result

    def encontrar_combinaciones( self, lista, numero ):
        # Metodo para encontrar las  combinaciones de implicantes.
        # cse ingresa una lista y el numero de caracteres por cada combinación.

        list_password = []
        for r in numero:
            res = itertools.combinations (lista, r)
            for e in res:
                list_password.append (''.join (e))
        return list_password

    def encontrar_redundantes( self, implicantes, implicados ):
        for i, implicante in enumerate (implicantes):
            __implicantes_temporales = []
            __implicados_temporales = []
            for j, implicante2 in enumerate (implicantes):
                if j != i:
                    __implicantes_temporales.append (implicante2)
                    __implicados_temporales.append (implicados[j])

            cierre = self.calcular_algoritmo_cierre (implicante,
                                                     __implicantes_temporales, __implicados_temporales)

            implicado = implicados[i]
            if implicado in cierre:
                print (">>>", implicante, "-", implicado, "-", cierre)
                self.redundantes.append ("Redundante: " + implicante + "->" + implicado + ", cierre: " + cierre)

                self.encontrar_redundantes (__implicantes_temporales, __implicados_temporales)
                break

            self.implicantes_L3 = implicantes
            self.implicados_L3 = implicados

    def calcular_llaves( self, conjunto_t, conjunto_l2_implicantes, conjunto_l2_implicados ):
        self.T = conjunto_t
        arr_T = self.T.replace (" ", "")
        arr_conjunto_t = arr_T.split (",")
        Z = []

        for i in arr_conjunto_t:
            flag = False

            if i in "".join (conjunto_l2_implicados):
                flag = True

            if flag == False:
                Z.append (i)

        self.z = Z
        arr_conjunto_t.sort ()
        Z_str = "".join (Z)
        T_str = "".join (arr_conjunto_t)

        cierreZ = self.calcular_algoritmo_cierre (Z_str, conjunto_l2_implicantes, conjunto_l2_implicados)

        is_superkey = (cierreZ == T_str)

        W = []

        for i in arr_conjunto_t:
            flag = False

            if i in "".join (conjunto_l2_implicantes):
                flag = True

            if flag == False:
                W.append (i)
        self.w = W
        W_str = "".join (W)
        union = list (W_str + cierreZ)
        union_res = list (set (union))
        V = []
        for i in arr_conjunto_t:
            flag = False

            if i in "".join (union_res):
                flag = True

            if flag is False:
                V.append (i)
        return Z, is_superkey, W, V, cierreZ

    def CalcularBCForma( self ):
        return True

    def Calcular2Forma( self ):
        return True

    def Calcular3Forma( self ):
        return True
