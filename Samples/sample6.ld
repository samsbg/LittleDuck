program quack;
var x : float;
void unaFun (k : float)[
    var x : float;
    { 
        print("fun");
        k = x + k;
    }
];
void dosFun (param1 : int, param2 : float, param3 : float)[
    var var1 : float;
    { 
        print("fun");
        k = x + k;
    }
];
main {
    print("hi");
    unaFun( 20.0 );
    print("bye");
}
end