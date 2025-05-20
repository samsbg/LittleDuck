# Este es un código para calcular los primero 10 números fibonacci
program fibonacci;
var iterador, numActual, acumulador, numSiguiente : int;
main {
  numActual = 0;
  numSiguiente = 1;
  iterador = 1;
  do {
    print(numeroActual);
    # Va sumando el actual y el anterior
    acumulador = numActual + numSiguiente;
    numActual = numSiguiente;
    numSiguiente = acumulador;
    iterador = iterador + 1;
  } while (iterador <= 10);
}
end