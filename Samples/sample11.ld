program sample11;
var a : float;
void fun(b : string, c : float) [
  {
    c = 1;
  }
];
main {
    print(a);
    a = 1 / 0;
    fun( "1", 2.0 );
}
end