var n:int;

n = 5;

if n > 2 {
  log(n);
}

if n < 4 {
  log("non");
}
else if n == 5 {
  log("ok");
}
else {
  log("oui");
}

# EXPECTED
# 5
# ok
