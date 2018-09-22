from logica.calculo import Calculo


def calcular():
    calculo = Calculo()
    conjunto_l = "AB->C, D->EF, C->A, BE->C, BC->D, CF->BD, ACD->B, CE->AF"
    conjunto_t = "A,B,C,D,E,F"

    calculo.calcular_cubrimiento(conjunto_l)
    Z, is_superkey, W, V = calculo.calculo_llaves(conjunto_t, calculo.implicantes_L3, calculo.implicados_L3)

    if is_superkey:
        is_superllave = "Z es superllave"
    else:
        is_superllave = ""

    print("Z: ", Z)
    print("is_superkey: ", is_superllave)
    print("W: ", W)
    print("V: ", V)
