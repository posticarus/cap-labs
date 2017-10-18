var u, v, w, n : int;
u = 1;
v = 1;
n = 1;
while n <= 15 {
    w = v;
    v = u + v;
    u = w;
    log(u);
    n = n + 1;
}
# Fibonacci

# EXPECTED
# 1
# 2
# 3
# 5
# 8
# 13
# 21
# 34
# 55
# 89
# 144
# 233
# 377
# 610
# 987
