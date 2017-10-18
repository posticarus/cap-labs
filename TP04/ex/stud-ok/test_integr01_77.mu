# Test d'integration - Simulation de boucle for.
var left : int;
var right : int;
var step : int;
var i : int;

left = 10;
right = 30;
step = 5;

i = left;
while i <= right {
	log(i);
	i = i + step;
}

# EXPECTED
# 10
# 15
# 20
# 25
# 30
