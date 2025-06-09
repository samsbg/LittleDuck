# Este es un código para calcular los primero 10 números fibonacci
program fibonacci;
void defFibonacci(numAnt1: int, numAnt2: int, iterador: int) [
  var acumulador : int;
  {if ( iterador > 0 ) {
    acumulador = numAnt1 + numAnt2;
    print(acumulador);
    iterador = iterador - 1;
    defFibonacci(numAnt2, acumulador, iterador);
  };}
];
main {
  print("Primeros 12 digitos de fibonacci");
  print(0);
  print(1);
  defFibonacci(0, 1, 10);
}
end