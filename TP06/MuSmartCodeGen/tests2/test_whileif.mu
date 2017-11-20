var x,a,n:int;

x = 3;
n = 5;
a = 7;
while (n < 10) {
   if (x == 2) {
       log(a);
    }
    else {
        log(x);
     }   
   x = x-1;
   n = n+1;
}


# EXPECTED
# 3
# 7 
# 1
# 0
# -1