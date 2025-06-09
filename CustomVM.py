
from TokenDef import BOLD, RED, RESET
from CustomSemantics import Funcion, Lista_Cuadruples, Tabla_Funciones

regions = {
    "global_int": 1000,
    "global_float": 2000,
    "global_str": 3000,
    "global_void": 4000,
    "local_int": 7000,
    "local_float": 8000,
    "local_str": 9000,
    "temp_int": 12000,
    "temp_float": 13000,
    "temp_bool": 14000,
    "cte_int": 17000,
    "cte_float": 18000,
    "cte_str": 19000
}

class VM:
    def __init__(self):
        self.tabla_funciones = Tabla_Funciones()
        self.lista_cuadruples = Lista_Cuadruples(self.tabla_funciones)
        self.variables = {}

    def analisis(self):
        self.leer_archivo()
        self.ejecutar()

    def leer_cuadruples(self, lineas):
        for linea in lineas:
            cuad = linea.split("\t")
            if len(cuad) == 5:
                cuad = [x.strip() for x in cuad if x.strip() != '']
                cuad = [cuad[1]] + [int(x) for x in cuad[2:]]
                cuad = [None if x == -1 else x for x in cuad]
                self.lista_cuadruples.agregarCuadruple(cuad[0], cuad[1], cuad[2], cuad[3])

    def leer_funciones(self, lineas):
        i = 0
        while (i < len(lineas)/6):
            direccion = int(lineas[0+i*6])
            params = int(lineas[1+i*6].split("\t")[1])
            count_int = int(lineas[2+i*6].split("\t")[1])
            count_float = int(lineas[3+i*6].split("\t")[1])
            count_str = int(lineas[4+i*6].split("\t")[1])

            fun = Funcion(direccion, 'void', params, 'local', direccion)

            for x in range(count_int):
                fun.tabla_simbolos.agregar_variable(regions['local_int'], 'PR_INT', True)
                regions["local_int"] = regions["local_int"] + 1
            regions["local_int"] -= count_int

            for x in range(count_float):
                fun.tabla_simbolos.agregar_variable(regions['local_float'], 'PR_FLOAT', True)
                regions["local_float"] = regions["local_float"] + 1
            regions["local_float"] -= count_float

            for x in range(count_str):
                fun.tabla_simbolos.agregar_variable('', 'PR_STRING', True)
                regions["local_str"] = regions["local_str"] + 1
            regions["local_str"] -= count_str

            self.tabla_funciones.funciones[direccion] = fun
            i += 1

    def leer_archivo(self):
        with open("output.txt", "r") as file:
            content = file.read()
            secciones = content.split("\n\n")

        seccion = secciones.pop()
        lineas = seccion.split("\n")

        self.leer_cuadruples(lineas)
        
        seccion = secciones.pop()
        lineas = seccion.split("\n")

        if (len(lineas[0].split("\t")) == 1 and lineas[0] != ""):
            self.leer_funciones(lineas)
            seccion = secciones.pop()
            lineas = seccion.split("\n")

        for region in regions:
            self.variables[regions[region]] = {}

        for linea in lineas:
            region = linea.split("\t")
            numVar = int(region[1].strip())
            for i in range(numVar):
                r = regions[region[0].strip()]
                self.variables[r][r+i] = None

        if (len(secciones)):
            seccion = secciones.pop()
            lineas = seccion.split("\n")
            for linea in lineas:
                constante = linea.split("\t")
                dir = int(constante[1].strip())
                valor  = constante[0]
                r = dir - dir % 1000
                if (r == 17000):
                    valor = int(valor)
                if (r == 18000):
                    valor = float(valor)
                self.variables[r][dir] = valor

    def getDirecciones(self, cuad):
        direcciones = {}

        dir_izq = cuad.argIzquierda
        if (dir_izq):
            r_izq = dir_izq - dir_izq % 1000
            direcciones['izq'] = self.variables[r_izq][dir_izq]
            if (direcciones['izq'] is None):
                print(f"{RED}Variable sin declarar en cuadruple {cuad.index}{RESET}")
                return 'error'

        dir_der = cuad.argDerecha
        if (dir_der):
            r_der = dir_der - dir_der % 1000
            direcciones['der'] = self.variables[r_der][dir_der]
            if (direcciones['der'] is None):
                print(f"{RED}Variable sin declarar en cuadruple {cuad.index}{RESET}")
                return 'error'

        return direcciones

    def ejecutar(self):
        cuads = self.lista_cuadruples.cuadruples
        index = int(cuads[0].resultado) - 1
        consola = ''
        returnIndex = []
        while (index < len(cuads)):
            operador = cuads[index].operador
            if (operador == 'print'):
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                if (direcciones['izq']  == "/n"):
                    consola += '\n'
                else:
                    consola += str(direcciones['izq'])
                index += 1

            elif (operador == '+'):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] + direcciones['der']
                index += 1

            elif (operador == '-'):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                self.variables[dir_r][dir_resultado] = direcciones['izq'] - direcciones['der']
                index += 1

            elif (operador == '/'):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones['der'] ==  0):
                    print(f"{RED}Division entre cero invalida en el cuadruple {index+1}{RESET}")
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] / direcciones['der']
                index += 1

            elif (operador == '*'):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                self.variables[dir_r][dir_resultado] = direcciones['izq'] * direcciones['der']
                index += 1

            elif (operador == '='):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq']
                index += 1

            elif (operador == '<'):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] < direcciones['der']
                index += 1

            elif (operador == '>'):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] > direcciones['der']
                index += 1

            elif (operador == '>='):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] >= direcciones['der']
                index += 1

            elif (operador == '<='):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] <= direcciones['der']
                index += 1
                
            elif (operador == '!='):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] != direcciones['der']
                index += 1
            
            elif (operador == '=='):
                dir_resultado = cuads[index].resultado
                dir_r = dir_resultado - dir_resultado % 1000
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return
                self.variables[dir_r][dir_resultado] = direcciones['izq'] == direcciones['der']
                index += 1

            elif (operador == 'gotoF'):
                resultado = cuads[index].resultado
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return

                if direcciones['izq']:
                    index += 1
                else:
                    index = resultado - 1

            elif (operador == 'goto'):
                resultado = int(cuads[index].resultado)
                index = resultado - 1

            elif (operador == 'gotoV'):
                resultado = cuads[index].resultado
                direcciones = self.getDirecciones(cuads[index])
                if (direcciones == 'error'):
                    return

                if direcciones['izq']:
                    index = resultado - 1
                else:
                    index += 1

            elif (operador == 'sub'):
                dir_func = int(cuads[index].argIzquierda) 
                funcion = self.tabla_funciones.funciones[dir_func]
                index += 1

                self.funParams = funcion.tabla_simbolos.variables.copy()

            elif(operador == 'param'):
                param = self.funParams.pop(next(iter(self.funParams)))
                dir_param = int(param.direccion)
                r_param = dir_param - dir_param % 1000
                dir_resultado = int(cuads[index].argIzquierda)
                r_resultado = dir_resultado - dir_resultado % 1000

                self.variables[r_param][dir_param] = self.variables[r_resultado][dir_resultado]
                index += 1

            elif(operador == 'gosub'):
                returnIndex.append(index+2)
                resultado = int(cuads[index].resultado)
                index = resultado - 1

            elif (operador == 'endfun'):
                index = returnIndex.pop() - 1

            else: 
                print(f"{BOLD}Operador desconocido {operador}{RESET}")
                index += 1

        print(f"\n{BOLD}Consola de salida: --------------------{RESET}")
        print(consola)
        print(f"{BOLD}Fin de programa: ----------------------{RESET}")

            