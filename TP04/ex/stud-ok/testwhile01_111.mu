var x:int;
var y:float;

x = 4;
y = 0.0;

while x > 0 
{
	y = y + 0.5;
	x = x - 1; 
}
log(y);

# EXPECTED
# 2.0
