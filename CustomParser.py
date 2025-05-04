
class CustomParser:

  def analisis(self, tokens):
    self.ASSIGN(tokens)

  def set_error(self, linea, valorEsperado, valorRecibido, posicion, tokens, estructura):
    error_string = f"ERROR SINTACTICO en linea {linea} index {posicion}: esperaba {valorEsperado}, recibio {valorRecibido} dentro de la estructura {estructura}"
    tokens.lista_errores.append(error_string)

  def getToken(self, tokens):
    token = tokens.current().token
    content = tokens.current().content
    return token, content

  def avanza(self, tokens):
    tokens.avanza()
    return self.getToken(tokens)

  # Programa -> program id ; VAR? FUNCS* main Body end
  def Programa(self, tokens):
    token, content = self.getToken(tokens)
    
    if (token != 'PR_PROGRAM'):
      self.set_error(tokens.current().lineaPos, 'program', content, tokens.pos, tokens, 'Programa')
      return
      
    token, content = self.avanza(tokens)

    if (token != 'IDENTIFICADOR'):
      self.set_error(tokens.current().lineaPos, 'id', content, tokens.pos, tokens, 'Programa')
      return
      
    token, content = self.avanza(tokens)

    if (token != 'DEL_PUYCO'):
      self.set_error(tokens.current().lineaPos, ';', content, tokens.pos, tokens, 'Programa')
      return
      
    token, content = self.avanza(tokens)

    if (token == 'PR_VAR'):
      self.VARS(tokens)

    token, content = self.getToken(tokens)

    while (token == 'PR_VOID'):
      self.FUNCS(tokens)
      token, content = self.getToken(tokens)

    if (token != 'PR_MAIN'):
      self.set_error(tokens.current().lineaPos, 'main', content, tokens.current().lexpos, tokens, 'Programa')
      return
      
    token, content = self.avanza(tokens)

    self.Body(tokens)

    token, content = self.getToken(tokens)

    if (token != 'PR_END'):
      
      self.set_error(tokens.current().lineaPos, 'end', content, tokens.current().lexpos, tokens, 'Programa')
      return

    tokens.avanza()

  # VARS -> var ( id ( , id )* : TYPE ;)+
  def VARS(self, tokens):
    token, content = self.getToken(tokens)

    if (token != 'PR_VAR'):
      self.set_error(tokens.current().lineaPos, 'var', content, tokens.current().lexpos, tokens, 'VARS')
      return

    token, content = self.avanza(tokens)

    if (token != 'IDENTIFICADOR'):
      self.set_error(tokens.current().lineaPos, 'id', content, tokens.current().lexpos, tokens, 'VARS')
      return

    while (token == 'IDENTIFICADOR'):
      token, content = self.avanza(tokens)
  
      while (token == 'DEL_COMA'):
        token, content = self.avanza(tokens)
  
        if (token != 'IDENTIFICADOR'):
          self.set_error(tokens.current().lineaPos, 'id', content, tokens.current().lexpos, tokens, 'VARS')
          return
      
        token, content = self.avanza(tokens)

      if (token != 'DEL_DOSPU'):
        self.set_error(tokens.current().lineaPos, ':', content, tokens.current().lexpos, tokens, 'VARS')
        return

      token, content = self.avanza(tokens)

      self.TYPE(tokens)

      token, content = self.getToken(tokens)

      if (token != 'DEL_PUYCO'):
        self.set_error(tokens.current().lineaPos, ';', content, tokens.current().lexpos, tokens, 'VARS')
        return

      token, content = self.avanza(tokens)

  # TYPE -> int | float
  def TYPE(self, tokens):
    token, content = self.getToken(tokens)

    if (token != 'PR_INT' and token != 'PR_FLOAT'):
      self.set_error(tokens.current().lineaPos, 'int o float', content, tokens.current().lexpos, tokens, 'TYPE')
      return

    tokens.avanza()

  def Body(self, tokens):
    token, content = self.getToken(tokens)

    if (token != 'DEL_CORABI'):
      self.set_error(tokens.current().lineaPos, '{', content, tokens.current().lexpos, tokens, 'Body')
      return

    token, content = self.avanza(tokens)

    while (token == 'IDENTIFICADOR' or token == 'PR_IF' or token == 'PR_PRINT' or token == 'PR_DO'):
      self.STATEMENT(tokens)
      token, content = self.getToken(tokens)
    
    if (token != 'DEL_CORCER'):
      self.set_error(tokens.current().lineaPos, '}', content, tokens.current().lexpos, tokens, 'Body')
      return

    token, content = self.avanza(tokens)

  def STATEMENT(self, tokens):
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

  def Print(self, tokens):
    token, content = self.getToken(tokens)

    if (token != 'PR_PRINT'):
      self.set_error(tokens.current().lineaPos, 'print', content, tokens.current().lexpos, tokens, 'Print')
      return

    token, content = self.avanza(tokens)

    if (token != 'DEL_PARABI'):
      self.set_error(tokens.current().lineaPos, '(', content, tokens.current().lexpos, tokens, 'Print')
      return

    token, content = self.avanza(tokens)

    if (token == 'PR_STRING'):
      token, content = self.avanza(tokens)
    else:
      self.expresion(tokens)
      token, content = self.getToken(tokens)

    while (token == 'DEL_COMA'):
      token, content = self.avanza(tokens)
      
      if (token == 'PR_STRING'):
        token, content = self.avanza(tokens)
      else:
        self.expresion(tokens)
        token, content = self.getToken(tokens)

    if (token != 'DEL_PARCER'):
      self.set_error(tokens.current().lineaPos, ')', content, tokens.current().lexpos, tokens, 'Print')
      return
  
    token, content = self.avanza(tokens)

    if (token != 'DEL_PUYCO'):
      self.set_error(tokens.current().lineaPos, ')', content, tokens.current().lexpos, tokens, 'Print')
      return
  
    token, content = self.avanza(tokens)
  
  def CYCLE(self, tokens):
    token, content = self.getToken(tokens)
    
    if (token != 'PR_DO'):
      self.set_error(tokens.current().lineaPos, 'do', content, tokens.current().lexpos, tokens, 'CYCLE')
      return

    token, content = self.avanza(tokens)

    self.Body(tokens)

    token, content = self.getToken(tokens)

    if (token != 'PR_WHILE'):
      self.set_error(tokens.current().lineaPos, 'while', content, tokens.current().lexpos, tokens, 'CYCLE')
      return

    token, content = self.avanza(tokens)

    if (token != 'DEL_PARABI'):
      self.set_error(tokens.current().lineaPos, '(', content, tokens.current().lexpos, tokens, 'CYCLE')
      return
  
    token, content = self.avanza(tokens)

    self.expresion(tokens)
    token, content = self.getToken(tokens)

    if (token != 'DEL_PARCER'):
      self.set_error(tokens.current().lineaPos, ')', content, tokens.current().lexpos, tokens, 'CYCLE')
      return
  
    token, content = self.avanza(tokens)

    if (token != 'DEL_PUYCO'):
      self.set_error(tokens.current().lineaPos, ';', content, tokens.current().lexpos, tokens, 'CYCLE')
      return
  
    token, content = self.avanza(tokens)

  def CONDITION(self, tokens):
    token, content = self.getToken(tokens)
    
    if (token != 'PR_IF'):
      self.set_error(tokens.current().lineaPos, 'if', content, tokens.current().lexpos, tokens, 'CONDITION')
      return

    token, content = self.avanza(tokens)

    if (token != 'DEL_PARABI'):
      self.set_error(tokens.current().lineaPos, '(', content, tokens.current().lexpos, tokens, 'CONDITION')
      return
  
    tokens.avanza()

    self.expresion(tokens)

    token, content = self.getToken(tokens)

    if (token != 'DEL_PARCER'):
      self.set_error(tokens.current().lineaPos, ')', content, tokens.current().lexpos, tokens, 'CONDITION')
      return
  
    token, content = self.avanza(tokens)

    self.Body(tokens)

    token, content = self.getToken(tokens)

    if (token == 'PR_ELSE'):
      tokens.avanza()
      self.Body(tokens)

    token, content = self.getToken(tokens)
  
    if (token != 'DEL_PUYCO'):
      self.set_error(tokens.current().lineaPos, ';', content, tokens.current().lexpos, tokens, 'CONDITION')
      return

    tokens.avanza()

  def CTE(self, tokens):
    token, content = self.getToken(tokens)
    
    if (token != 'CA_NUMBER' and token != 'CA_FLOAT'):
      self.set_error(tokens.current().lineaPos, '(', content, tokens.current().lexpos, tokens, 'CTE')
      return

    tokens.avanza()    

  def FUNCS(self, tokens):
    token, content = self.getToken(tokens)

    if (token != 'VOID'):
      self.set_error(tokens.lineaPos, 'void', content, tokens.current().lexpos, tokens, 'FUNCS')
      return

    token, content = self.avanza(tokens)

    if (token != 'IDENTIFICADOR'):
      self.set_error(tokens.lineaPos, 'id', content, tokens.current().lexpos, tokens, 'FUNCS')
      return
  
    token, content = self.avanza(tokens)

    if (token != 'DEL_PARABI'):
      self.set_error(tokens.lineaPos, '(', content, tokens.current().lexpos, tokens, 'FUNCS')
      return
  
    token, content = self.avanza(tokens)

    if (token == 'IDENTIFICADOR'):
      token, content = self.avanza(tokens)

      if (token != 'DEL_DOSPU'):
        self.set_error(tokens.lineaPos, ')', content, tokens.current().lexpos, tokens, 'FUNCS')
        return
  
      token, content = self.avanza(tokens)

      self.TYPE(tokens)

      while (token == 'DEL_COMA'):
        token, content = self.avanza(tokens)

        if (token != 'DEL_DOSPU'):
          self.set_error(tokens.lineaPos, ')', content, tokens.current().lexpos, tokens, 'FUNCS')
          return

        token, content = self.avanza(tokens)

        self.TYPE(tokens)

    if (token != 'DEL_PARCER'):
      self.set_error(tokens.lineaPos, ')', content, tokens.current().lexpos, tokens, 'FUNCS')
      return
  
    token, content = self.avanza(tokens)

    if (token != 'DEL_BRAABI'):
      self.set_error(tokens.lineaPos, '[', content, tokens.current().lexpos, tokens, 'FUNCS')
      return

    token, content = self.avanza(tokens)

    if (token == 'VAR'):
      self.VARS(tokens)

    self.Body(tokens)

    token, content = self.getToken(tokens)

    if (token != 'DEL_BRACER'):
      self.set_error(tokens.lineaPos, ']', content, tokens.current().lexpos, tokens, 'FUNCS')
      return
    
    token, content = self.avanza(tokens)

    if (token != 'DEL_PUYCO'):
      self.set_error(tokens.lineaPos, ';', content, tokens.current().lexpos, tokens, 'FUNCS')
      return
  
    tokens.avanza()

  def F_Call(self, tokens):
    token, content = self.getToken(tokens)

    if (token != 'IDENTIFICADOR'):
      self.set_error(tokens.current().lineaPos, 'id', content, tokens.current().lexpos, tokens, 'F_Call')
      return

    token, content = self.avanza(tokens)

    if (token != 'DEL_PARABI'):
      self.set_error(tokens.current().lineaPos, '(', content, tokens.current().lexpos, tokens, 'F_Call')
      return
  
    token, content = self.avanza(tokens)

    if (token == 'DEL_PARABI' or token == 'OA_SUMA' or token == 'OA_RESTA' or token == 'IDENTIFICADOR' or token == 'CA_NUMBER' or token == 'CA_FLOAT'):
      self.expresion(tokens)
      token, content = self.getToken(tokens)

      while (token == 'DEL_COMA'):
        tokens.avanza()
        self.expresion(tokens)
        token, content = self.getToken(tokens)

    if (token != 'DEL_PARCER'):
      self.set_error(tokens.current().lineaPos, ')', content, tokens.current().lexpos, tokens, 'F_Call')
      return

    token, content = self.avanza(tokens)

    if (token != 'DEL_PUYCO'):
      self.set_error(tokens.current().lineaPos, ';', content, tokens.current().lexpos, tokens, 'F_Call')
      return
  
    token, content = self.avanza(tokens)

  # F -> ( E ) | const_int
  def FACTOR(self, tokens):
    token, content = self.getToken(tokens)
  
    if (token == 'DEL_PARABI'):
      tokens.avanza()
      
      self.exp(tokens)
  
      token, content = self.getToken(tokens)
  
      if (token != 'DEL_PARCER'):
        self.set_error(tokens.current().lineaPos, ")", content, tokens.current().lexpos, tokens, 'FACTOR')
        return
  
      tokens.avanza()
  
    elif (token == 'OA_SUMA' or token == 'OA_RESTA' or token == 'CA_NUMBER' or token == 'CA_FLOAT' or token == 'IDENTIFICADOR'):

      if (token == 'OA_SUMA' or token == 'OA_RESTA'):
        token, content = self.avanza(tokens)

      if (token == 'IDENTIFICADOR'):
        tokens.avanza()
      elif (token == 'CA_NUMBER' or token == 'CA_FLOAT'):
        self.CTE(tokens)
      else:
        self.set_error(tokens.current().lineaPos, "Numero entero o id", content, tokens.current().lexpos, tokens, 'FACTOR')
        return
  
    else:
      self.set_error(tokens.current().lineaPos, "Numero entero, id o (", content, tokens.current().lexpos, tokens, 'FACTOR')

  # T' -> * F T' | epsilon
  def termino_prime(self, tokens):
    token, content = self.getToken(tokens)
  
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
    token, content = self.getToken(tokens)
  
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
    token, content = self.getToken(tokens)
  
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
    token, content = self.getToken(tokens)
  
    if (token != 'IDENTIFICADOR'):
      self.set_error(tokens.current().lineaPos, "id", content, tokens.current().lexpos, tokens, 'ASSIGN')
  
    token, content = self.avanza(tokens)

    if (token == 'OA_IGUAL'):
      self.set_error(tokens.current().lineaPos, "=", content, tokens.current().lexpos, tokens, 'ASSIGN')
      
    tokens.avanza()
    self.expresion(tokens)

    token, content = self.getToken(tokens)

    if (token != "DEL_PUYCO"):
      self.set_error(tokens.current().lineaPos, ";", content, tokens.current().lexpos, tokens, 'ASSIGN')

    tokens.avanza()

