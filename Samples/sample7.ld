program proquacks;
var n : int ; j , i : float; s : string;
 
void fact (n : int, a : int)
[  var n : int;
 
   {  if (n > 1 )
      {  b = a * n;
         fact (n-1, b);  
      }
      else
      {  print(a);   }; 
   }
];
 
void some_other( n : int )
[  var n : float;
   {  n = "woooooooooo 5"; 
      print("hello "); 
      xf = 7;
 
      fact(3, 1);
   } 
];
 
 
main 
{  n = 5;
   fact(n, 1);
 
   fact(n+1, 1);
 
    do {
 
      print(3, "w", 4+5, 4.5);
    }while( 3 < 5 / 1.5  );
 
 
    if ( 3 >= 8)
    {
      print("texto ");
      n = 58 + 9 * 5;
    }
    else
    {   print("xsxsxs", (5) );
 
    };
}
end