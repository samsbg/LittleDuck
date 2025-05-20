# Este es un código para calcular celcius a fahrenheit y viceversa
program convert_cf;
var celcius, fahrenheit : int;
main {
  celsius = 0;
  # Calcula los fahrenheit de los celcius
  fahrenheit = celsius * 9 / 5 + 32;
  print(fahrenheit);

  fahrenheit = 0;
  # Calcula los celcius de los fahrenheit
  celsius = (fahrenheit - 32) * 5 / 9;
  print(celcius);
}
end