# -*- coding: utf8 -*-
import json
import sys
sys.path.append('../')
from logica.calculo import Calculo


class ApiController:

    def __init__(self):
        self.__data_in = ''
        self.__data_out = ''
        self.__implicantes = []
        self.__implicados = []
        self.__json_arr = []
        self.__transform_arr = []

    def get_data_in(self):
        # Obtenemos el valor del archivo y validamos que tenga el formato correcto:
        try:
            print("Leer archivos")
            json_valor = json.loads(open('data_in.json').read())
            print(json_valor)
        except ValueError as e:
            print(f"El archivo no tiene un formato valido. Error: {e}")
        else:
            self.__data_in = json_valor

    def transform_data_in(self):
        # Transformamos la data para pasarla a la clase calculo con variables de un solo caracter ( codigo = A, nombre = B, etc...)

        print(self.__data_in['conjunto'])
        print(self.__data_in['dependencias_funcionales'])

        for i, value in enumerate(self.__data_in["conjunto"]):
            self.__json_arr.append(value["value"])

        print(self.__json_arr)

        for one in range(65, 65 + len(self.__data_in["conjunto"])):
            self.__transform_arr.append(chr(one))

        print(self.__transform_arr)

        implicantes = []
        implicados = []
        implicantes_transform = []
        implicados_transform = []
        # Cogemos los implicantes y los implicados y los transformamos a A,B,C,D,E,... Y LOS GUARDAMOS en dos arrays

        for i, dependencia in enumerate(self.__data_in["dependencias_funcionales"]):

            dep = dependencia["implicante"].split(" ")
            print(dep)
            dep_transfor = ''
            for i, value in enumerate(dep):
                if value in self.__json_arr:
                    iter = self.__json_arr.index(value)
                    dep_transfor = dep_transfor + self.__transform_arr[iter]



            print(">>", dep_transfor)
            implicantes_transform.append(dep_transfor)

            dep = dependencia["implicado"].split(" ")
            print(dep)
            dep_transfor = ''
            for i, value in enumerate(dep):
                if value in self.__json_arr:
                    iter = self.__json_arr.index(value)
                    dep_transfor = dep_transfor + self.__transform_arr[iter]

                    # print(dep_transfor)
            implicados_transform.append(dep_transfor)

        print(implicantes_transform)
        print(implicados_transform)

        self.__implicantes = implicantes_transform
        self.__implicados = implicados_transform

    def calculate_minimal_recubrimiento(self):
        """

        :return: el valor obtenido del recubrimiento minimo y su transformacion a los conjuntos originales.
        """
        self.get_data_in()
        self.transform_data_in()
        calculo = Calculo()
        calculo.calcular_cubrimiento(implicantes=self.__implicantes, implicados=self.__implicados)
        res_implicantes, res_implicados = calculo.get_l2_dependences()
        print("Response1: ", res_implicantes)
        print("Response1: ", res_implicados)

        resultado_implicantes, resultado_implicados = self.transform_to_data_out(res_implicantes, res_implicados)

        return resultado_implicantes, resultado_implicados

    def transform_to_data_out(self, implicantes, implicados):
        """

        :param implicantes:
        :param implicados:
        :return: Valor correspondiente de implicantes e implicador en los parametros originales (A = codigo, B = Nombre, etc)
        """
        # implicantes:
        arr_implicantes = []
        arr_implicados = []

        for implicante in implicantes:
            char_implicantes = list(implicante)
            print(">>", char_implicantes)

            impli_transform = ''
            for j, value in enumerate(char_implicantes):
                if value in self.__transform_arr:
                    iter = self.__transform_arr.index(value)
                    impli_transform = impli_transform + self.__json_arr[iter]

            arr_implicantes.append(impli_transform)

        for implicado in implicados:
            char_implicado = list(implicado)

            impli_transform = ''
            for j, value in enumerate(char_implicado):
                if value in self.__transform_arr:
                    iter = self.__transform_arr.index(value)
                    impli_transform = impli_transform + self.__json_arr[iter]

            arr_implicados.append(impli_transform)

        return arr_implicantes, arr_implicados

    def get_data_out(self):
        implicantes_res, implicados_res = self.calculate_minimal_recubrimiento()

        arr_result = []
        for i, value in enumerate(implicados_res):
            dependencias ={
                "implicante": implicantes_res[i],
                "implicado": implicados_res[i]
            }

            arr_result.append(dependencias)

        result = {
            "conjunto": self.__data_in['conjunto'],
            "dependencias": arr_result

        }

        # Writing JSON data
        with open('data_out.json', 'w') as f:
            json.dump(result, f)



ej = ApiController()
ej.get_data_out()

