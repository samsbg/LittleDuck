program tabla_de_2;
var i, acumulador : int ; s : float;
void unaFun (k : float)[
    var x : float;
    { 
        x = 5;
        print("Entró a la fun");
        k = x + s;
    }
];
main {
  print("Empieza el programa");
  i = 1;
  acumulador = 0;
  print("Entral al while");
  do {
    i = i + 1;
    acumulador = acumulador + 2;
    print( acumulador );
  } while (i < 11);
  if (i > 15) {
    print("Entra al if");
  } else {
    print("Entra al else");
  };
  s = 5;
  unaFun(15.0);
}
end
# un patoprograma de ejemplo
# quack!