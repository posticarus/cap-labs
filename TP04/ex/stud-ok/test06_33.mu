var x:int;
var y:int;
var z:float;

x = 2;
y = 3;

if (x<42) {
    log("bonjour");
} else if (y>42) {
    log("au revoir");
} else {
    log("au revoir");
}


if (x>42) {
    log("au revoir");
} else if (y<42) {
    log("bonjour");
} else {
    log("au revoir");
}

# EXPECTED
# bonjour
# bonjour
