var n:int;

n=2;
if 2!=2 {n=3;} else if 2==2 {n=5;} else {n=4;}
log(n);
while (n<10) {n=n+1;log(n);}

#EXPECTED
#5
#6
#7
#8
#9
#10