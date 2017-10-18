var n_max, i, flight:int;
var n: float;
n_max = 30;
i = 20;
while i < n_max {
n = i/1;
flight = 0;
while n != 1 {
if n%2 == 0 n = n/2; else n = 3*n+1;
flight = flight + 1;
}
log(i);
log(flight);
i = i + 1;
}

# EXPECTED
#20
#7
#21
#7
#22
#15
#23
#15
#24
#10
#25
#23
#26
#10
#27
#111
#28
#18
#29
#18
