var n:int;
n = 9;

while n > 0 {

  # expressions can be surrounded by parenthesis, of course
  if (n % 2  == 0) {
    log n + " -> even";
  }
  else {
    log n + " -> odd";
  }

  n = n - 1;
}

# EXPECTED
# 9 -> odd
# 8 -> even
# 7 -> odd
# 6 -> even
# 5 -> odd
# 4 -> even
# 3 -> odd
# 2 -> even
# 1 -> odd
