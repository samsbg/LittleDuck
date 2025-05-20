from TokenDef import Estructura_Impresion

class CustomParser:

  def analisis(self, tokens):
    self.estructura = Estructura_Impresion()
    self.Programa(tokens)

  def checar_token(self, token_esperado, valor_esperado, tokens, estructura, keywords):
    token = tokens.current().token
    if (not token in token_esperado):
      self.set_error(token_esperado, valor_esperado, tokens, estructura, keywords)
    else:
      tokens.avanza()

  def set_error(self, tokenEsperado, valorEsperado, tokens, estructura, keywords):
    tokenObj = tokens.current()

    self.estructura.marcar_error()
    error_string = f"ERROR SINTACTICO en linea {tokenObj.lineaPos} index {tokenObj.lexpos}: esperaba {valorEsperado}, recibio {tokenObj.content} dentro de la estructura {estructura}"
    tokens.lista_errores.append(error_string)

    while (not tokenObj.token in keywords and not tokenObj.token in tokenEsperado):
      tokens.avanza()
      tokenObj = tokens.current()

    if (tokenObj.token in tokenEsperado):
      tokens.avanza()

  # Programa -> program id ; VAR? FUNCS* main Body end
  def Programa(self, tokens):
    self.estructura.empezar_estructura('Programa')

    keywords = ['EOD', 'PR_END', 'PR_MAIN', 'PR_VOID', 'PR_VAR', 'DEL_PUYCO', 'PR_PROGRAM']

    self.checar_token(['PR_PROGRAM'], 'program', tokens, 'Programa', keywords)

    keywords.pop()

    self.checar_token(['IDENTIFICADOR'], 'id', tokens, 'Programa', keywords)
    self.checar_token(['DEL_PUYCO'], ';', tokens, 'Programa', keywords)

    keywords.pop()

    token = tokens.current().token

    if (token == 'PR_VAR'):
      self.VARS(tokens)
    
    keywords.pop()
    token = tokens.current().token

    while (token == 'PR_VOID'):
      self.FUNCS(tokens)
      token = tokens.current().token

    keywords.pop()

    self.checar_token(['PR_MAIN'], 'main', tokens, 'Programa', keywords)

    keywords.pop()

    self.Body(tokens)
    self.checar_token(['PR_END'], 'end', tokens, 'Programa', keywords)
    self.estructura.termina_estructura()

  # Body -> { STATEMENT* }
  def Body(self, tokens):
    self.estructura.empezar_estructura('Body')

    keywords = ['EOD', 'PR_END']

    self.checar_token(['DEL_CORABI'], '{', tokens, 'Body', keywords)
    token = tokens.current().token

    while (token != 'DEL_CORCER' and not token in keywords):
      self.STATEMENT(tokens)
      token = tokens.current().token

    self.checar_token(['DEL_CORCER'], '}', tokens, 'Body', keywords)
    self.estructura.termina_estructura()

  # STATEMENT -> ASSIGN | CONDITION | CYCLE | F_Call | Print
  def STATEMENT(self, tokens):
    self.estructura.empezar_estructura('STATEMENT')
    token = tokens.current().token
    
    if (token == 'IDENTIFICADOR' and tokens.peek().token == 'OA_IGUAL'):
      self.ASSIGN(tokens)
    elif (token == 'PR_IF'):
      self.CONDITION(tokens)
    elif (token == 'PR_DO'):
      self.CYCLE(tokens)
    elif (token == 'IDENTIFICADOR' and tokens.peek().token == 'DEL_PARABI'):
      self.F_Call(tokens)
    elif (token == 'PR_PRINT'):
      self.Print(tokens)
    else:
      tokenObj = tokens.current()
      error_string = f"ERROR SINTACTICO en linea {tokenObj.lineaPos} index {tokenObj.lexpos}: recibio {tokenObj.content} dentro de la estructura STATEMENT y no se pudo identificar"
      tokens.lista_errores.append(error_string)
      tokens.avanza()

    self.estructura.termina_estructura()

  # Print -> print ( E ( , E )* ) ;
  def Print(self, tokens):
    self.estructura.empezar_estructura('Print')

    keywords = ['EOD', 'PR_END', 'DEL_CORCER', 'PR_DO', 'PR_IF', 'PR_PRINT', 'DEL_PUYCO']
    
    tokens.avanza() # print
    self.checar_token(['DEL_PARABI'], '(', tokens, 'Print', keywords)
    token = tokens.current().token

    if (token == 'CA_STRING'):
      tokens.avanza()
    else:
      self.expresion(tokens)

    token = tokens.current().token

    while (token == 'DEL_COMA'):
      tokens.avanza()
      token = tokens.current().token
      
      if (token == 'PR_STRING'):
        tokens.avanza()
      else:
        self.expresion(tokens)
      
      token = tokens.current().token

    self.checar_token(['DEL_PARCER'], ')', tokens, 'Print', keywords)
    self.checar_token(['DEL_PUYCO'], ';', tokens, 'Print', keywords)
    self.estructura.termina_estructura()

  # CYCLE -> do Body while ( E ) ;
  def CYCLE(self, tokens):
    self.estructura.empezar_estructura('CYCLE')
    
    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'PR_WHILE']
    
    tokens.avanza() # do
    self.Body(tokens)
    self.checar_token(['PR_WHILE'], 'while', tokens, 'CYCLE', keywords)
    keywords.pop()

    self.checar_token(['DEL_PARABI'], '(', tokens, 'CYCLE', keywords)
    self.expresion(tokens)
    self.checar_token(['DEL_PARCER'], ')', tokens, 'CYCLE', keywords)
    self.checar_token(['DEL_PUYCO'], ';', tokens, 'CYCLE', keywords)
    
    self.estructura.termina_estructura()

  # CONDITION -> if ( E ) Body [ else Body ] ;
  def CONDITION(self, tokens):
    self.estructura.empezar_estructura('CONDITION')

    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_PUYCO', 'PR_ELSE']

    tokens.avanza() # if
    self.checar_token(['DEL_PARABI'], '(', tokens, 'CONDITION', keywords)
    self.expresion(tokens)
    self.checar_token(['DEL_PARCER'], ')', tokens, 'CONDITION', keywords)
    self.Body(tokens)
    token = tokens.current().token

    if (token == 'PR_ELSE'):
      tokens.avanza()
      self.Body(tokens)

    self.checar_token(['DEL_PUYCO'], ';', tokens, 'CONDITION', keywords)
    self.estructura.termina_estructura()

  # F_Call -> id ( E ( , E )* ) ;
  def F_Call(self, tokens):
    self.estructura.empezar_estructura('F_Call')

    keywords = ['EOD', 'PR_END', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_CORCER', 'DEL_PUYCO']

    tokens.avanza() # ID
    tokens.avanza() # '('
    token = tokens.current().token

    # TODO: Cambiar el if gigante con un F_CALL prime
    if (token == 'DEL_PARABI' or token == 'OA_SUMA' or token == 'OA_RESTA' or token == 'IDENTIFICADOR' or token == 'CA_NUMBER' or token == 'CA_FLOAT'):
      self.expresion(tokens)
      token = tokens.current().token

      while (token == 'DEL_COMA'):
        tokens.avanza()
        self.expresion(tokens)
        token = tokens.current().token

    self.checar_token(['DEL_PARCER'], ')', tokens, 'F_Call', keywords)
    self.checar_token(['DEL_PUYCO'], ';', tokens, 'F_Call', keywords)
    self.estructura.termina_estructura()

  # F -> ( E ) | const_int
  def FACTOR(self, tokens):
    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_PUYCO']
    token = tokens.current().token

    if (token == 'DEL_PARABI'):
      tokens.avanza()
      self.exp(tokens)
      self.checar_token(['DEL_PARCER'], ')', tokens, 'FACTOR', keywords)

    elif (token == 'OA_SUMA' or token == 'OA_RESTA' or token == 'CA_NUMBER' or token == 'CA_FLOAT' or token == 'IDENTIFICADOR'):

      if (token == 'OA_SUMA' or token == 'OA_RESTA'):
        tokens.avanza()

      token = tokens.current().token

      if (token == 'IDENTIFICADOR'):
        tokens.avanza()
      elif (token == 'CA_NUMBER' or token == 'CA_FLOAT'):
        self.CTE(tokens)
      else:
        self.set_error(['IDENTIFICADOR', 'CA_NUMBER', 'CA_FLOAT'], 'id o numero', tokens, 'FACTOR', keywords)
        return
  
    else:
        self.set_error(['OA_SUMA', 'OA_RESTA', 'CA_NUMBER', 'CA_FLOAT', 'IDENTIFICADOR'], 'Numero o variable', tokens, 'FACTOR', keywords)

  # VARS -> var ( id ( , id )* : TYPE ;)+
  def VARS(self, tokens):
    self.estructura.empezar_estructura('VARS')

    keywords = ['EOD', 'PR_END', 'PR_VOID', 'PR_MAIN', 'DEL_CORABI', 'DEL_PUYCO', 'DEL_DOSPU']
    
    tokens.avanza() # var

    token = tokens.current().token

    if (token != 'IDENTIFICADOR'):
      self.set_error(['IDENTIFICADOR'], 'id', tokens, 'VARS', keywords)

    while (token == 'IDENTIFICADOR'):
      tokens.avanza()
      token = tokens.current().token
  
      while (token == 'DEL_COMA'):
        tokens.avanza()
        self.checar_token(['IDENTIFICADOR'], 'id', tokens, 'VARS', keywords)
        token = tokens.current().token

      self.checar_token(['DEL_DOSPU'], ':', tokens, 'VARS', keywords)
      self.TYPE(tokens)
      self.checar_token(['DEL_PUYCO'], ';', tokens, 'VARS', keywords)
      token = tokens.current().token

    self.estructura.termina_estructura()

  # TYPE -> int | float
  def TYPE(self, tokens):
    keywords = ['EOD', 'PR_END', 'DEL_PUYCO', 'PR_VOID', 'PR_MAIN', 'DEL_COMA', 'DEL_PARCER', 'PR_INT', 'PR_FLOAT']
    self.checar_token(['PR_INT', 'PR_FLOAT'], 'int o float', tokens, 'TYPE', keywords)

  # FUNCS -> void id ( id : TYPE ( , id : TYPE )* ) [ VARS? Body ] ;
  def FUNCS(self, tokens):
    self.estructura.empezar_estructura('FUNCS')

    keywords = ['PR_VOID', 'PR_MAIN', 'PR_END', 'EOD', 'PR_VAR', 'DEL_BRAABI', 'DEL_BRACER', 'DEL_PARCER', 'DEL_PARABI']

    tokens.avanza() # void

    self.checar_token(['IDENTIFICADOR'], 'id', tokens, 'FUNCS', keywords)
    self.checar_token(['DEL_PARABI'], '(', tokens, 'FUNCS', keywords)
    keywords.pop()
    
    token = tokens.current().token

    if (token == 'IDENTIFICADOR'):
      tokens.avanza()
      self.checar_token(['DEL_DOSPU'], ':', tokens, 'FUNCS', keywords)
      self.TYPE(tokens)
      token = tokens.current().token

      while (token == 'DEL_COMA'):
        tokens.avanza()
        self.checar_token(['IDENTIFICADOR'], 'id', tokens, 'FUNCS', keywords)
        self.checar_token(['DEL_DOSPU'], ':', tokens, 'FUNCS', keywords)
        self.TYPE(tokens)

        token = tokens.current().token
  
    self.checar_token(['DEL_PARCER'], ')', tokens, 'FUNCS', keywords)
    keywords.pop()
    self.checar_token(['DEL_BRAABI'], '[', tokens, 'FUNCS', keywords)

    token = tokens.current().token

    if (token == 'PR_VAR'):
      self.VARS(tokens)

    self.Body(tokens)

    self.checar_token(['DEL_BRACER'], ']', tokens, 'FUNCS', keywords)
    self.checar_token(['DEL_PUYCO'], ';', tokens, 'FUNCS', keywords)

    self.estructura.termina_estructura()

  # CTE -> CA_NUMBER | CA_FLOAT
  def CTE(self, tokens):
    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_PUYCO']
    self.checar_token(['CA_NUMBER', 'CA_FLOAT'], 'numero', tokens, 'CTE', keywords)

  # T' -> * F T' | epsilon
  def termino_prime(self, tokens):
    token = tokens.current().token
  
    # Si el token actual es un '*'
    if (token == 'OA_MULTI' or token == 'OA_DIVI'):
      tokens.avanza()
      self.FACTOR(tokens)
      self.termino_prime(tokens)
  
  # T -> F T'
  def termino(self, tokens):
    self.FACTOR(tokens)
    self.termino_prime(tokens)
  
  # E' -> + T E' | epsilon
  def exp_prime(self, tokens):
    token = tokens.current().token
  
    if (token == 'OA_SUMA' or token == 'OA_RESTA'):
      tokens.avanza()
      self.termino(tokens)
      self.exp_prime(tokens)
  
  # E -> T E'
  def exp(self, tokens):
    self.termino(tokens)
    self.exp_prime(tokens)
  
  # EX' -> E EX' | epsilon
  def expresion_prime(self, tokens):
    token = tokens.current().token
  
    if (token == "DEL_FLEIZQ" or token == "DEL_FLEDER" or token == 'OL_IGUIGU' or token ==  'OL_NOIGU' or token ==  'OL_MEIGU' or token ==  'OL_MAIGU'):
      tokens.avanza()
      self.exp(tokens)
      self.expresion_prime(tokens)
  
  # EX -> E EX'
  def expresion(self, tokens):
    self.exp(tokens)
    self.expresion_prime(tokens)
  
  # A -> id = EX ;
  def ASSIGN(self, tokens):
    self.estructura.empezar_estructura('ASSIGN')

    keywords = ['PR_END', 'EOD', 'PR_IF', 'PR_DO', 'PR_PRINT', 'DEL_CORCER', 'DEL_PUYCO']

    tokens.avanza() # ID
    tokens.avanza() # '='

    self.expresion(tokens)
    self.checar_token(['DEL_PUYCO'], ';', tokens, 'ASSIGN', keywords)

    self.estructura.termina_estructura()

