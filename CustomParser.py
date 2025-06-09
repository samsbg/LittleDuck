from TokenDef import Estructura_Impresion
from CustomSemantics import Lista_Cuadruples, Tabla_Funciones

class CustomParser:

  def analisis(self, tokens):
    self.estructura = Estructura_Impresion()
    self.tokens = tokens
    tablaFunciones = Tabla_Funciones()
    self.listaCuadruples = Lista_Cuadruples(tablaFunciones)

    self.Programa()

  def checar_token(self, token_esperado, valor_esperado, estructura, keywords):
    token = self.tokens.current().token
    if (not token in token_esperado):
      self.set_error(token_esperado, valor_esperado, estructura, keywords)
    else:
      self.tokens.avanza()

  def set_error(self, tokenEsperado, valorEsperado, estructura, keywords):
    tokenObj = self.tokens.current()

    self.estructura.marcar_error()
    error_string = f"ERROR SINTACTICO en linea {tokenObj.lineaPos} index {tokenObj.lexpos}: esperaba {valorEsperado}, recibio {tokenObj.content} dentro de la estructura {estructura}"
    self.tokens.lista_errores.append(error_string)

    while (not tokenObj.token in keywords and not tokenObj.token in tokenEsperado):
      self.tokens.avanza()
      tokenObj = self.tokens.current()

    if (tokenObj.token in tokenEsperado):
      self.tokens.avanza()

  # Programa -> program id ; VAR? FUNCS* main Body end
  def Programa(self):
    self.estructura.empezar_estructura('Programa')

    keywords = ['EOD', 'PR_END', 'PR_MAIN', 'PR_VOID', 'PR_VAR', 'DEL_PUYCO', 'PR_PROGRAM']

    self.checar_token(['PR_PROGRAM'], 'program', 'Programa', keywords)

    keywords.pop()

    nombrePrograma = self.tokens.current().content
    funPrograma = self.listaCuadruples.empezarPrograma(nombrePrograma)

    self.checar_token(['IDENTIFICADOR'], 'id', 'Programa', keywords)
    self.checar_token(['DEL_PUYCO'], ';', 'Programa', keywords)

    keywords.pop()

    token = self.tokens.current().token

    if (token == 'PR_VAR'):
      self.VARS(funPrograma.tabla_simbolos)
    
    keywords.pop()
    token = self.tokens.current().token

    while (token == 'PR_VOID'):
      self.FUNCS()
      token = self.tokens.current().token

    keywords.pop()

    self.checar_token(['PR_MAIN'], 'main', 'Programa', keywords)
    self.listaCuadruples.agregarResultadoMain(nombrePrograma)

    keywords.pop()

    self.Body()
    self.checar_token(['PR_END'], 'end', 'Programa', keywords)
    self.estructura.termina_estructura()

  # Body -> { STATEMENT* }
  def Body(self):
    self.estructura.empezar_estructura('Body')

    keywords = ['EOD', 'PR_END']

    self.checar_token(['DEL_CORABI'], '{', 'Body', keywords)
    token = self.tokens.current().token

    while (token != 'DEL_CORCER' and not token in keywords):
      self.STATEMENT()
      token = self.tokens.current().token

    self.checar_token(['DEL_CORCER'], '}', 'Body', keywords)
    self.estructura.termina_estructura()

  # STATEMENT -> ASSIGN | CONDITION | CYCLE | F_Call | Print
  def STATEMENT(self):
    self.estructura.empezar_estructura('STATEMENT')
    token = self.tokens.current().token
    
    if (token == 'IDENTIFICADOR' and self.tokens.peek().token == 'OA_IGUAL'):
      self.ASSIGN()
    elif (token == 'PR_IF'):
      self.CONDITION()
    elif (token == 'PR_DO'):
      self.CYCLE()
    elif (token == 'IDENTIFICADOR' and self.tokens.peek().token == 'DEL_PARABI'):
      self.F_Call()
    elif (token == 'PR_PRINT'):
      self.Print()
    else:
      tokenObj = self.tokens.current()
      error_string = f"ERROR SINTACTICO en linea {tokenObj.lineaPos} index {tokenObj.lexpos}: recibio {tokenObj.content} dentro de la estructura STATEMENT y no se pudo identificar"
      self.tokens.lista_errores.append(error_string)
      self.tokens.avanza()

    self.estructura.termina_estructura()

  # Print -> print ( E ( , E )* ) ;
  def Print(self):
    self.estructura.empezar_estructura('Print')

    keywords = ['EOD', 'PR_END', 'DEL_CORCER', 'PR_DO', 'PR_IF', 'PR_PRINT', 'DEL_PUYCO']
    
    self.tokens.avanza() # print
    self.checar_token(['DEL_PARABI'], '(', 'Print', keywords)
    token = self.tokens.current().token

    argI = self.expresion()

    self.listaCuadruples.agregarImpresion(contenido=argI['dir'])

    token = self.tokens.current().token

    while (token == 'DEL_COMA'):
      self.tokens.avanza()
      token = self.tokens.current().token
      
      argI = self.expresion()

      self.listaCuadruples.agregarImpresion(contenido=argI['dir'])
      
      token = self.tokens.current().token

    self.listaCuadruples.agregarSaltoLinea()

    self.checar_token(['DEL_PARCER'], ')', 'Print', keywords)
    self.checar_token(['DEL_PUYCO'], ';', 'Print', keywords)
    self.estructura.termina_estructura()

  # CYCLE -> do Body while ( E ) ;
  def CYCLE(self):
    self.estructura.empezar_estructura('CYCLE')
    index = self.listaCuadruples.empezarCiclo()
    
    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'PR_WHILE']
    
    self.tokens.avanza() # do
    self.Body()
    self.checar_token(['PR_WHILE'], 'while', 'CYCLE', keywords)
    keywords.pop()

    self.checar_token(['DEL_PARABI'], '(', 'CYCLE', keywords)
    linea = self.tokens.current().lineaPos
    argI = self.expresion()
    self.checar_token(['DEL_PARCER'], ')', 'CYCLE', keywords)
    self.checar_token(['DEL_PUYCO'], ';', 'CYCLE', keywords)

    self.listaCuadruples.condicionCiclo(argI['dir'], argI['tipo'], linea, index)
    
    self.estructura.termina_estructura()

  # CONDITION -> if ( E ) Body [ else Body ] ;
  def CONDITION(self):
    self.estructura.empezar_estructura('CONDITION')

    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_PUYCO', 'PR_ELSE']

    self.tokens.avanza() # if
    self.checar_token(['DEL_PARABI'], '(', 'CONDITION', keywords)
    linea = self.tokens.current().lineaPos
    argI = self.expresion()
    indexC = self.listaCuadruples.agregarCondicion(argI['dir'], argI['tipo'], linea)
    self.checar_token(['DEL_PARCER'], ')', 'CONDITION', keywords)
    self.Body()
    token = self.tokens.current().token

    if (token == 'PR_ELSE'):
      indexE = self.listaCuadruples.empezarElse()
      self.listaCuadruples.terminarCondicion(indexC)
      self.tokens.avanza()
      self.Body()
      self.listaCuadruples.terminarElse(indexE)
    else:
      self.listaCuadruples.terminarCondicion(indexC)

    self.checar_token(['DEL_PUYCO'], ';', 'CONDITION', keywords)
    self.estructura.termina_estructura()

  # F_Call -> id ( E ( , E )* ) ;
  def F_Call(self):
    self.estructura.empezar_estructura('F_Call')

    keywords = ['EOD', 'PR_END', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_CORCER', 'DEL_PUYCO']

    nombre = self.tokens.current().content
    linea = self.tokens.current().lineaPos

    self.listaCuadruples.empezarLlamadaFuncion(nombre, linea)

    self.tokens.avanza() # ID
    self.tokens.avanza() # '('
    token = self.tokens.current().token

    if (token == 'DEL_PARABI' or token == 'OA_SUMA' or token == 'OA_RESTA' or token == 'IDENTIFICADOR' or token == 'CA_NUMBER' or token == 'CA_FLOAT' or token == 'CA_STRING'):
      argI = self.expresion()
      params = [argI['dir']]
      tipos = [argI['tipo']]
      token = self.tokens.current().token

      while (token == 'DEL_COMA'):
        self.tokens.avanza()
        argI = self.expresion()
        params.append(argI['dir'])
        tipos.append(argI['tipo'])
        token = self.tokens.current().token

      self.listaCuadruples.agregarParams(nombre, params, tipos, linea)

    self.listaCuadruples.llamarFuncion(nombre)

    self.checar_token(['DEL_PARCER'], ')', 'F_Call', keywords)
    self.checar_token(['DEL_PUYCO'], ';', 'F_Call', keywords)
    self.estructura.termina_estructura()

  # F -> ( E ) | const_int
  def FACTOR(self):
    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_PUYCO']
    token = self.tokens.current().token

    if (token == 'DEL_PARABI'):
      self.tokens.avanza()
      arg = self.exp()
      self.checar_token(['DEL_PARCER'], ')', 'FACTOR', keywords)
      return arg

    elif (token == 'OA_SUMA' or token == 'OA_RESTA' or token == 'CA_NUMBER' or token == 'CA_FLOAT' or token == 'CA_STRING' or token == 'IDENTIFICADOR'):
      negativo = False
      
      if (token == 'OA_SUMA' or token == 'OA_RESTA'):
        if (token == 'OA_RESTA'):
          negativo = True
        self.tokens.avanza()

      token = self.tokens.current().token
      content = self.tokens.current().content
      linea = self.tokens.current().lineaPos

      if (token == 'IDENTIFICADOR'):
        self.tokens.avanza()
        var = self.listaCuadruples.buscarVariable(content, linea)
        arg = {'tipo': var['tipo'], 'dir': var['dir']}
      elif (token == 'CA_NUMBER'):
        self.CTE()
        dir = self.listaCuadruples.nuevaConstante(tipo='int', valor=content)['dir']
        arg = {'tipo': 'int', 'dir': dir}
      elif (token == 'CA_FLOAT'):
        self.CTE()
        dir = self.listaCuadruples.nuevaConstante(tipo='float', valor=content)['dir']
        arg = {'tipo': 'float', 'dir': dir}
      elif (token == 'CA_STRING'):
        self.CTE()
        dir = self.listaCuadruples.nuevaConstante(tipo='string', valor=content)['dir']
        arg = {'tipo': 'string', 'dir': dir}
      else:
        self.set_error(['IDENTIFICADOR', 'CA_NUMBER', 'CA_FLOAT'], 'id o numero', 'FACTOR', keywords)
        return
      
      if (negativo):
        arg = self.listaCuadruples.agregarNegativo('-', arg, None)
      
      return arg
  
    else:
        self.set_error(['OA_SUMA', 'OA_RESTA', 'CA_NUMBER', 'CA_FLOAT', 'IDENTIFICADOR'], 'Numero o variable', 'FACTOR', keywords)

  # VARS -> var ( id ( , id )* : TYPE ;)+
  def VARS(self, tabla_simbolos):
    self.estructura.empezar_estructura('VARS')

    keywords = ['EOD', 'PR_END', 'PR_VOID', 'PR_MAIN', 'DEL_CORABI', 'DEL_PUYCO', 'DEL_DOSPU']
    
    self.tokens.avanza() # var

    token = self.tokens.current().token

    if (token != 'IDENTIFICADOR'):
      self.set_error(['IDENTIFICADOR'], 'id', 'VARS', keywords)

    while (token == 'IDENTIFICADOR'):
      content = self.tokens.current().content
      variables = [content]
      self.tokens.avanza()
      token = self.tokens.current().token
  
      while (token == 'DEL_COMA'):
        self.tokens.avanza()
        content = self.tokens.current().content
        variables.append(content)
        self.checar_token(['IDENTIFICADOR'], 'id', 'VARS', keywords)
        token = self.tokens.current().token

      self.checar_token(['DEL_DOSPU'], ':', 'VARS', keywords)
      tipo = self.tokens.current().token
      linea = self.tokens.current().lineaPos
      if (tipo in ['PR_STRING', 'PR_INT', 'PR_FLOAT']):
        self.listaCuadruples.agregar_variables(tabla_simbolos, variables, tipo, linea)
      self.TYPE()
      self.checar_token(['DEL_PUYCO'], ';', 'VARS', keywords)
      token = self.tokens.current().token

    self.estructura.termina_estructura()

  # TYPE -> int | float
  def TYPE(self):
    keywords = ['EOD', 'PR_END', 'DEL_PUYCO', 'PR_VOID', 'PR_MAIN', 'DEL_COMA', 'DEL_PARCER', 'PR_INT', 'PR_FLOAT']
    self.checar_token(['PR_INT', 'PR_FLOAT', 'PR_STRING'], 'int, float o string', 'TYPE', keywords)

  # FUNCS -> void id ( id : TYPE ( , id : TYPE )* ) [ VARS? Body ] ;
  def FUNCS(self):
    self.estructura.empezar_estructura('FUNCS')

    keywords = ['PR_VOID', 'PR_MAIN', 'PR_END', 'EOD', 'PR_VAR', 'DEL_BRAABI', 'DEL_BRACER', 'DEL_PARCER', 'DEL_PARABI']

    self.tokens.avanza() # void

    content = self.tokens.current().content
    linea = self.tokens.current().lineaPos
    fun = self.listaCuadruples.agregarFuncion(content)
    tabla_simbolos = fun.tabla_simbolos

    self.checar_token(['IDENTIFICADOR'], 'id', 'FUNCS', keywords)
    self.checar_token(['DEL_PARABI'], '(', 'FUNCS', keywords)
    keywords.pop()
    
    token = self.tokens.current().token
    variable = self.tokens.current().content
    paramCount = 0

    if (token == 'IDENTIFICADOR'):
      paramCount += 1
      self.tokens.avanza()
      self.checar_token(['DEL_DOSPU'], ':', 'FUNCS', keywords)
      tipo = self.tokens.current().token
      self.TYPE()
      self.listaCuadruples.agregar_variables(tabla_simbolos, [variable], tipo, linea, True)
      token = self.tokens.current().token

      while (token == 'DEL_COMA'):
        paramCount += 1
        self.tokens.avanza()
        variable = self.tokens.current().content
        token = self.tokens.current().token
        self.checar_token(['IDENTIFICADOR'], 'id', 'FUNCS', keywords)
        self.checar_token(['DEL_DOSPU'], ':', 'FUNCS', keywords)
        tipo = self.tokens.current().token
        self.TYPE()
        if (token == 'IDENTIFICADOR'):
          self.listaCuadruples.agregar_variables(tabla_simbolos, [variable], tipo, linea, True)
        token = self.tokens.current().token

    fun.params = paramCount
  
    self.checar_token(['DEL_PARCER'], ')', 'FUNCS', keywords)
    keywords.pop()
    self.checar_token(['DEL_BRAABI'], '[', 'FUNCS', keywords)

    token = self.tokens.current().token

    if (token == 'PR_VAR'):
      self.VARS(tabla_simbolos)

    self.Body()

    self.listaCuadruples.terminarFuncion()

    self.checar_token(['DEL_BRACER'], ']', 'FUNCS', keywords)
    self.checar_token(['DEL_PUYCO'], ';', 'FUNCS', keywords)

    self.estructura.termina_estructura()

  # CTE -> CA_NUMBER | CA_FLOAT | CA_STRING
  def CTE(self):
    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_PUYCO']
    self.checar_token(['CA_NUMBER', 'CA_FLOAT', 'CA_STRING'], 'numero', 'CTE', keywords)

  # T' -> * F T' | epsilon
  def termino_prime(self, argI):
    token = self.tokens.current().token
    content = self.tokens.current().content
  
    # Si el token actual es un '*'
    if (token == 'OA_MULTI' or token == 'OA_DIVI'):
      linea = self.tokens.current().lineaPos
      self.tokens.avanza()
      argD = self.FACTOR()
      temp = self.termino_prime(argD)
      if (temp):
        argD = temp
      return self.listaCuadruples.agregarTemporal(operador=content, argIzquierdaT=argI['tipo'], argIzquierdaD=argI['dir'], argDerechaT=argD['tipo'], argDerechaD=argD['dir'], linea=linea)
  
  # T -> F T'
  def termino(self):
    argI = self.FACTOR()
    temp = self.termino_prime(argI)

    if (temp):
      argI = temp
    return argI
  
  # E' -> + T E' | epsilon
  def exp_prime(self, argI):
    token = self.tokens.current().token
    content = self.tokens.current().content
    linea = self.tokens.current().lineaPos
  
    if (token == 'OA_SUMA' or token == 'OA_RESTA'):
      self.tokens.avanza()
      argD = self.termino()
      temp = self.exp_prime(argI)
      if (temp):
        argD = temp
      return self.listaCuadruples.agregarTemporal(operador=content, argIzquierdaT=argI['tipo'], argIzquierdaD=argI['dir'], argDerechaT=argD['tipo'], argDerechaD=argD['dir'], linea=linea)
  
  # E -> T E'
  def exp(self):
    argI = self.termino()
    temp = self.exp_prime(argI)

    if (temp):
      argI = temp
    return argI
  
  # EX' -> E EX' | epsilon
  def expresion_prime(self, argI):
    token = self.tokens.current().token
    content = self.tokens.current().content
    linea = self.tokens.current().lineaPos
  
    if (token == "DEL_FLEIZQ" or token == "DEL_FLEDER" or token == 'OL_IGUIGU' or token ==  'OL_NOIGU' or token ==  'OL_MEIGU' or token ==  'OL_MAIGU'):
      self.tokens.avanza()
      argD = self.exp()
      temp = self.expresion_prime(argD)

      if (temp):
        argD = temp
      return self.listaCuadruples.agregarTemporal(operador=content, argIzquierdaT=argI['tipo'], argIzquierdaD=argI['dir'], argDerechaT=argD['tipo'], argDerechaD=argD['dir'], linea=linea)
  
  # EX -> E EX'
  def expresion(self):
    argI = self.exp()
    temp = self.expresion_prime(argI)

    if (temp):
      argI = temp
    return argI
  
  # A -> id = EX ;
  def ASSIGN(self):
    self.estructura.empezar_estructura('ASSIGN')

    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_CORCER', 'DEL_PUYCO']

    token = self.tokens.current()

    self.tokens.avanza() # ID
    self.tokens.avanza() # '='

    result = self.expresion()

    self.listaCuadruples.agregarAsignacion(variableC=token.content, valorD=result['dir'], valorT=result['tipo'], linea=token.lineaPos)

    self.checar_token(['DEL_PUYCO'], ';', 'ASSIGN', keywords)

    self.estructura.termina_estructura()

