# Test d'integration - Algorithme d'Euclide.
var a : int;
var b : int;
var t : int;

a = 35;
b = 20;
while b != 0 {
	t = b;
	b = a % b;
	a = t;
}

log(a);

# EXPECTED
# 5