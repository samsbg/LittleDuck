from TokenDef import BOLD, GREEN, RED, RESET

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

tokens = {
    "PR_INT": "int",
    "PR_FLOAT": "float",
    "PR_STRING": "string",
    "PR_VOID": "void"
}

tipado = {
    'CA_NUMBER': 'int',
    'CA_FLOAT': 'float',
    'CA_STRING': 'string',
}

cubo_semantico = {
    'int': {
        'int': {
            '+': 'int',
            '-': 'int',
            '/': 'float',
            '*': 'int',
            '==': 'bool',
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '!=': 'bool',
            '=': 'bool'
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '/': 'float',
            '*': 'float',
            '==': 'bool',
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '!=': 'bool',
            '=': 'error'
        },
        'string': {
            '+': 'error',
            '-': 'error',
            '/': 'error',
            '*': 'error',
            '==': 'bool',
            '<': 'error',
            '>': 'error',
            '<=': 'error',
            '>=': 'error',
            '!=': 'bool',
            '=': 'error'
        },
    },
    'float': {
        'int': {
            '+': 'float',
            '-': 'float',
            '/': 'float',
            '*': 'float',
            '==': 'bool',
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '!=': 'bool',
            '=': 'bool'
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '/': 'float',
            '*': 'float',
            '==': 'bool',
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '!=': 'bool',
            '=': 'bool'
        },
        'string': {
            '+': 'error',
            '-': 'error',
            '/': 'error',
            '*': 'error',
            '==': 'bool',
            '<': 'error',
            '>': 'error',
            '<=': 'error',
            '>=': 'error',
            '!=': 'bool',
            '=': 'error'
        },
    },
    'string': {
        'int': {
            '+': 'error',
            '-': 'error',
            '/': 'error',
            '*': 'error',
            '==': 'bool',
            '<': 'error',
            '>': 'error',
            '<=': 'error',
            '>=': 'error',
            '!=': 'bool',
            '=': 'error'
        },
        'float': {
            '+': 'error',
            '-': 'error',
            '/': 'error',
            '*': 'error',
            '==': 'bool',
            '<': 'error',
            '>': 'error',
            '<=': 'error',
            '>=': 'error',
            '!=': 'bool',
            '=': 'error'
        },
        'string': {
            '+': 'string',
            '-': 'error',
            '/': 'error',
            '*': 'error',
            '==': 'bool',
            '<': 'error',
            '>': 'error',
            '<=': 'error',
            '>=': 'error',
            '!=': 'bool',
            '=': 'bool'
        },
    }
}

class Funcion:
    nombre = ''
    returnType = ''
    params = 0
    tabla_simbolos = {}
    quadPos = 0
    direccion = 0

    def __init__(self, nombre, returnType, params, scope, direccion=None, quadPos=0):
        self.nombre = nombre
        self.returnType = returnType
        self.params = params
        self.quadPos = quadPos
        self.direccion = direccion
        self.tabla_simbolos = Tabla_Simbolos(scope)

    def imprimir(self):
        direccion = self.direccion if self.direccion is not None else ''
        print(f"{self.nombre:<{15}} {tokens[self.returnType]:<{5}} {self.params:<{7}} {self.quadPos:<{10}} {direccion:<{10}}")

    def imprimir_archivo(self, file):
        count_int = sum(1 for var in self.tabla_simbolos.variables.values() if var.tipo == 'PR_INT')
        count_float = sum(1 for var in self.tabla_simbolos.variables.values() if var.tipo == 'PR_FLOAT')
        count_string = sum(1 for var in self.tabla_simbolos.variables.values() if var.tipo == 'PR_STRING')

        file.write(f"{self.direccion}\n")
        file.write(f"params\t{self.params}\n")
        file.write(f"local_int\t{count_int}\n")
        file.write(f"local_float\t{count_float}\n")
        file.write(f"local_string\t{count_string}\n")
        file.write("end\n")

        regions["local_int"] -= count_int
        regions["local_float"] -= count_float
        regions["local_str"] -= count_string

class Tabla_Funciones:
    funciones = {}

    def __init__(self,):
        self.funciones = {}

    def empezarFuncion(self, nombre, quadPos):
        fun = Funcion(nombre, 'PR_VOID', 0, "local", regions["global_void"], quadPos)
        self.funciones[nombre] = fun
        regions["global_void"] += 1
        return fun
    
    def set_params_funcion(self, nombre, params):
        self.funciones[nombre].params = params
    
    def agregarPrograma(self, nombre):
        fun = Funcion(nombre, 'PR_VOID', 0, "global")
        self.funciones[nombre] = fun
        return fun
    
    def agregarQuadPosPrograma(self, nombre, quadPos):
        self.funciones[nombre].quadPos = quadPos
    
    def imprimirFunciones(self):
        print(f"{BOLD}Tabla de Funciones:{RESET}")
        print(f"{BOLD}---------------------------------------------------{RESET}")
        print(f"{BOLD}{'Nombre':<{15}} {'Tipo':<{5}} {'Params':<{7}} {'CuadPos':<{10}} {'Dirección':<{10}}{RESET}")
        print('---------------------------------------------------')
        for nombre in self.funciones:
            fun = self.funciones[nombre]
            fun.imprimir()
        print(f"{BOLD}---------------------------------------------------{RESET}")

        print()
        print()

        for nombre in self.funciones:
            print(f"{BOLD}Tabla de simbolos de {self.funciones[nombre].nombre}:{RESET}")
            self.funciones[nombre].tabla_simbolos.imprimir_variables()
            print()

class Variable:
    def __init__(self, nombre, tipo, isParam, valor, direccion):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.direccion = direccion
        self.isParam = isParam

    def imprimir(self):
        nombre = f"{self.nombre:<{15}}"
        tipo = f"{tokens[self.tipo]:<{7}}"
        valor = f"{self.valor if self.valor is not None else '-':<{7}}"
        direccion = f"{self.direccion:<{15}}"
        print(f"{nombre} {tipo} {valor} {direccion}")

class Tabla_Simbolos:
    variables = {}

    def __init__(self, scope):
        self.variables = {}
        self.scope = scope

    def getCodigo(self, scope, tipo):
        region = self.getBaseRegion(scope, tipo)
        codigo = regions[region]
        regions[region] += 1
        return codigo
    
    def getBaseRegion(self, scope, tipo):
        if (tipo == "CA_NUMBER"):
            return regions["cte_int"]
        elif (tipo == "CA_FLOAT"):
            return regions["cte_float"]
        elif (tipo == "CA_STR"):
            return regions["cte_str"]
        
        match (scope, tipo):
            case ("global", "PR_INT"):
                return "global_int"
            case ("global", "PR_FLOAT"):
                return "global_float"
            case ("global", "PR_STRING"):
                return "global_str"
            case ("global", "PR_VOID"):
                return "global_void"
            case ("local", "PR_INT"):
                return "local_int"
            case ("local", "PR_FLOAT"):
                return "local_float"
            case ("local", "PR_STRING"):
                return "local_str"

    def agregar_variable(self, nombre, tipo, isParam=False, valor=None):
        codigo = self.getCodigo(self.scope, tipo)
        var = Variable(nombre, tipo, isParam, valor, codigo)
        self.variables[nombre] = var

    def imprimir_variables(self):
        print(f"{BOLD}------------------------------------------{RESET}")
        print(f"{BOLD}{'Nombre':<{15}} {'Tipo':<{7}} {'Valor':<{7}} {'Dirección':<{15}}{RESET}")
        print('------------------------------------------')
        for var in self.variables:
            self.variables[var].imprimir()
        print(f"{BOLD}------------------------------------------{RESET}")

class Cuadruple:
    index = -1
    operador = ''
    argIzquierda = ''
    argDerecha = ''
    resultado = None

    def __init__(self, index, operador, argIzquierda=None, argDerecha=None, resultado=None):
        self.index = index
        self.operador = operador
        self.argIzquierda = argIzquierda
        self.argDerecha = argDerecha
        self.resultado = resultado

    def marcarResultado(self, resultado):
        self.resultado = resultado

    def imprimir(self):
        index = f"{self.index:<{6}}"
        operador = f"{self.operador:<{10}}"
        argIzquierda = f"{self.argIzquierda if self.argIzquierda is not None else '':<{15}}"
        argDerecha = f"{self.argDerecha if self.argDerecha is not None else '':<{15}}"
        resultado = f"{self.resultado if self.resultado is not None else ''}"

        print(f"{index}|   {operador} {argIzquierda} {argDerecha}| {resultado}")

    def imprimir_archivo(self, file):
        argIzquierda = f"{self.argIzquierda if self.argIzquierda is not None else '-1':<{15}}"
        argDerecha = f"{self.argDerecha if self.argDerecha is not None else '-1':<{15}}"
        resultado = f"{self.resultado if self.resultado is not None else '-1'}"

        file.write(f"{self.index}\t{self.operador}\t{argIzquierda}\t{argDerecha}\t{resultado}\n")

class Lista_Cuadruples:
    def __init__(self, tablaFunciones):
        self.cuadruples = []
        self.tablaFunciones = tablaFunciones
        self.scope = []
        self.errors = []
        self.constantes = {
            1000: {},
            2000: {},
            3000: {},
            4000: {},
            7000: {},
            8000: {},
            9000: {},
            12000: {},
            13000: {},
            14000: {},
            17000: {},
            18000: {},
            19000: {}
        }

    def empezarPrograma(self, programa):
        self.scope.append(programa)
        cuad = Cuadruple(len(self.cuadruples) + 1, operador='gotomain')
        self.cuadruples.append(cuad)
        return self.tablaFunciones.agregarPrograma(programa)

    def agregarCuadruple(self, operador, argIzquierda, argDerecha, resultado=None):
        cuad = Cuadruple(len(self.cuadruples) + 1, operador, argIzquierda, argDerecha, resultado)
        self.cuadruples.append(cuad)

    def empezarLlamadaFuncion(self, nombre, linea):
        if (nombre in self.tablaFunciones.funciones):
            cuad = Cuadruple(len(self.cuadruples) + 1, operador='sub', argIzquierda=self.tablaFunciones.funciones[nombre].direccion)
            self.cuadruples.append(cuad)
        else: 
            self.errors.append(f"No se declaro funcion {nombre} en la linea {linea}")

    def agregarFuncion(self, nombre):
        self.scope.append(nombre)
        quadPos = len(self.cuadruples) + 1
        return self.tablaFunciones.empezarFuncion(nombre, quadPos)

    def agregarAsignacion(self, variableC, valorD, valorT, linea):
        variableC = self.buscarVariable(variableC, linea)
        variable = variableC['dir']
        if (self.getTipo('=', variableC['tipo'], valorT) == 'error'):
            self.errors.append(f"Asignación incorrecta de tipos de {variableC['tipo']} y {valorT} en linea {linea}")
        cuad = Cuadruple(len(self.cuadruples) + 1, operador='=', resultado=variable, argIzquierda=valorD)
        self.cuadruples.append(cuad)

    def agregarImpresion(self, contenido):
        cuad = Cuadruple(len(self.cuadruples) + 1, operador='print', argIzquierda=contenido)
        self.cuadruples.append(cuad)

    def agregarSaltoLinea(self):
        nuevalinea = self.nuevaConstante(tipo='CA_STRING', valor="/n")
        self.agregarImpresion(nuevalinea['dir'])

    def agregarResultadoMain(self, nombre):
        self.cuadruples[0].marcarResultado(len(self.cuadruples) + 1)
        quadPos = len(self.cuadruples) + 1
        self.tablaFunciones.agregarQuadPosPrograma(nombre, quadPos)
    
    def agregarParams(self, nombre, params, tipos, linea):
        if (len(params) != self.tablaFunciones.funciones[nombre].params):
            self.errors.append(f"Error en número de params. La funcion necesita {self.tablaFunciones.funciones[nombre].params} y se encontraron {len(params)} en la linea {linea}")
        paramFunciones = self.tablaFunciones.funciones[nombre].tabla_simbolos.variables.copy()
        for i in range(len(params)):
            param = paramFunciones.pop(next(iter(paramFunciones)))
            if (self.getTipo('=', tipos[i], tokens[param.tipo]) == 'error'):
                self.errors.append(f"Error en tipo de params con {tipos[i]} y {tokens[param.tipo]} en la linea {linea}")
            cuad = Cuadruple(len(self.cuadruples) + 1, operador='param', argIzquierda=params[i], resultado=i)
            self.cuadruples.append(cuad)

    def agregar_variables(self, tabla_simbolos, nombres, tipo, linea, isParam=False, valor=None):
        for nombre in nombres:
            if nombre in self.tablaFunciones.funciones[self.scope[-1]].tabla_simbolos.variables:
                self.errors.append(f"Variable {nombre} en linea {linea} ya existe en este contexto")
                return
            tabla_simbolos.agregar_variable(nombre, tipo, isParam, valor)

    def llamarFuncion(self, nombre):
        if (nombre in self.tablaFunciones.funciones):
            cuad = Cuadruple(len(self.cuadruples) + 1, operador='gosub', argIzquierda=self.tablaFunciones.funciones[nombre].direccion, resultado=self.tablaFunciones.funciones[nombre].quadPos)
            self.cuadruples.append(cuad)

    def terminarFuncion(self):
        self.scope.pop()
        cuad = Cuadruple(len(self.cuadruples) + 1, operador='endfun')
        self.cuadruples.append(cuad)

    def empezarCiclo(self):
        return len(self.cuadruples) + 1

    def condicionCiclo(self, argI, tipo, linea, index):
        if (tipo != 'bool'):
            self.errors.append(f"El valor no es boolean en la condicional de linea {linea}")
        cuad = Cuadruple(len(self.cuadruples) + 1, operador='gotoV', argIzquierda=argI, resultado=index)
        self.cuadruples.append(cuad)

    def agregarCondicion(self, content, tipo, linea):
        index = len(self.cuadruples) + 1
        if (tipo != 'bool'):
            self.errors.append(f"El valor no es boolean en la condicional de linea {linea}")
        cuad = Cuadruple(index, operador='gotoF', argIzquierda=content)
        self.cuadruples.append(cuad)
        return index

    def empezarElse(self):
        index = len(self.cuadruples) + 1
        cuad = Cuadruple(index, operador='goto')
        self.cuadruples.append(cuad)
        return index

    def terminarElse(self, index):
        self.cuadruples[index - 1].marcarResultado(len(self.cuadruples) + 1)

    def terminarCondicion(self, index):
        final = len(self.cuadruples) + 1
        self.cuadruples[index - 1].marcarResultado(final)

    def buscarVariable(self, nombre, linea):
        var = None
        if nombre in self.tablaFunciones.funciones[self.scope[-1]].tabla_simbolos.variables:
            var = self.tablaFunciones.funciones[self.scope[-1]].tabla_simbolos.variables[nombre]
        if (var):
            return {'dir': var.direccion, 'tipo': tokens[var.tipo]}
        else:
            self.errors.append(f"Variable '{nombre}' en la linea {linea} no encontrada en el ámbito actual.")
            return {'dir': -1, 'tipo': 'error'}
        
    def agregarNegativo(self, argIzquierdaC, argIzquierdaT):
        argIzquierda = self.getInfo(argIzquierdaC, argIzquierdaT)
        tipo = argIzquierda.tipo

        temporal = self.nuevoTemporal(tipo)
        cuad = Cuadruple(len(self.cuadruples) + 1, operador='-', argIzquierda=argIzquierda.dir, resultado=temporal)
        self.cuadruples.append(cuad)
        return {'dir': temporal, 'tipo': tipo}
    
    def agregarTemporal(self, operador, argIzquierdaD, argIzquierdaT, argDerechaD, argDerechaT, linea):
        
        tipo = self.getTipo(operador, argIzquierdaT, argDerechaT)

        if (tipo == 'error'):
            self.errors.append(f"No se puede utilizar el operador {operador} con los tipos {argIzquierdaT} y {argDerechaT} en la linea {linea}")
            return {'dir': -1, 'tipo': 'error'}

        temporal = self.nuevoTemporal(tipo, linea)
        cuad = Cuadruple(len(self.cuadruples) + 1, operador, argIzquierdaD, argDerechaD, resultado=temporal)
        self.cuadruples.append(cuad)
        return {'dir': temporal, 'tipo': tipo}
    
    def getTipo(self, operador, tipoIzq, tipoDer):
        if (tipoIzq == 'error' or tipoDer == 'error'):
            return 'error'
        if (tipoIzq not in cubo_semantico or tipoDer not in cubo_semantico[tipoIzq]):
            # Espero que no llegue aqui?
            print(f"Operador '{operador}' no válido para tipos '{tipoIzq}' y '{tipoDer}' en cuadruplo {len(self.cuadruples) + 1}.")
            return 'error'
        return cubo_semantico[tipoIzq][tipoDer][operador]
    
    def nuevaConstante(self, tipo, valor):
        if (tipo == 'CA_NUMBER' or tipo == 'int'):
            tipo = 'int'
            dir = regions['cte_int']
            regions['cte_int'] += 1
        elif (tipo == 'CA_FLOAT' or tipo == 'float'):
            tipo = 'float'
            dir = regions['cte_float']
            regions['cte_float'] += 1
        elif (tipo == 'CA_STRING' or tipo == 'string'):
            tipo = 'string'
            dir = regions['cte_str']
            regions['cte_str'] += 1
        else:
            print(f"Tipo de constante '{tipo}' no reconocido en cuadruple {len(self.cuadruples) + 1}.")
            return {'dir': -1, 'tipo': 'error'}

        self.constantes[(dir // 1000) * 1000][dir] = valor
        return {'dir': dir, 'tipo': tipo}

    def nuevoTemporal(self, tipo, linea):
        if (tipo == 'error'):
            self.errors.append(f"No se puede crear un temporal de tipo 'error' en la linea {linea}.")
            return -1
        if (tipo == 'int'):
            tipo = 'temp_int'
        elif (tipo == 'float'):
            tipo = 'temp_float'
        elif (tipo == 'string'):
            tipo = 'temp_str'
        elif (tipo == 'bool'):
            tipo = 'temp_bool'
        dir = regions[tipo]
        regions[tipo] += 1
        return dir

    def imprimir(self):

        print('Regiones:')
        for region in regions:
            print(f"{region}: {regions[region]}")

        print(f"{BOLD}Lista de Cuadruples:{RESET}")
        print(f"{BOLD}----------------------------------------------------------------{RESET}")
        print(f"{BOLD}{'Index':<6}|   {'Operador':<10} {'Arg Izq':<15} {'Arg Der':<15}| {'Resultado'}{RESET}")
        print('----------------------------------------------------------------')

        for i in self.cuadruples:
            i.imprimir()

        print(f"{BOLD}----------------------------------------------------------------{RESET}")
        print()
        print()

    def getNumeroVariables(self, tipo):
        num = regions[tipo]
        num = num % 1000
        return num

    def imprimir_archivo(self):
        with open('output.txt', 'w') as file:
            conteo = False
            for con in self.constantes:
                for var in self.constantes[con]:
                    file.write(f"{self.constantes[con][var]}\t{var}\n")
                    conteo = True

            if (conteo):
                file.write("\n")

            for r in regions:
                file.write(f"{r}\t{self.getNumeroVariables(r)}\n")

            file.write("\n")

            if (len(self.tablaFunciones.funciones) > 1):
                for nombre in self.tablaFunciones.funciones:
                    if (self.tablaFunciones.funciones[nombre].direccion != None):
                        fun = self.tablaFunciones.funciones[nombre]
                        fun.imprimir_archivo(file)

                file.write("\n")

            for cuad in self.cuadruples:
                cuad.imprimir_archivo(file)

    def programaValido(self):
        if (len(self.errors) == 0):
            print(f"{GREEN}PRE-SEMANTICA OKS - Programa válido{RESET}\n\n")
            return True

        print(f"{RED}PRE-SEMANTICA NOPE - Programa no válido{RESET}\n\n")
        for e in self.errors:
            print(e)
        return False
   