# Este es un código para calcular celcius a fahrenheit y viceversa
program convert_cf;
var celsius, fahrenheit : int;
main {
  print("0 celcius -> ");
  celsius = 0;
  # Calcula los fahrenheit de los celcius
  fahrenheit = celsius * 9 / 5 + 32;
  print("Fahrenheit: ", fahrenheit);

  print("");

  print("0 fahrenheit -> ");
  fahrenheit = 0;
  # Calcula los celcius de los fahrenheit
  celsius = (fahrenheit - 32) * 5 / 9;
  print("Celcius: ", celsius);
}
end