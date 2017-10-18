var a, b, t : int;

a = 468;
b = 324;

while b > 0 {
  t = b;
  b = a % b;
  a = t;
}

log("gcd: " + a);

# EXPECTED
# gcd: 36
