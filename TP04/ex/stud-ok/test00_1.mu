var u:int;
var f:float;
var f2:float;
var z:bool;

log(3^2+45*(-2/-1));
log( (false || 3 != 77 ) && (42<=1515) );
log(true || false && true);
f=10/3;
log(f);
f2=3.14;
log(f2*f);
z=f2!=f;
log(z);

# EXPECTED
# 99.0
# 1
# 1
# 3.3333333333333335
# 10.466666666666667
# 1
