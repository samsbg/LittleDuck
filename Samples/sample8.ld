program quack;
var x : float;
void unaFun (k : float)[
    { 
        print("fun");
        k = x + 5 * 2;
    }
];
void dosFun (param1 : int, param2 : float, param3 : float)[
    var var1 : float;
    { 
        print( 5 );
        var1 = param1 + param2;
    }
];
main {
    print("hi");
    unaFun( 20.0 );
    print("bye");
}
end