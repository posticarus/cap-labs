var x:int;
var y:int;

x = 42;

while x>0 {
    x = x - 1;
}

log(x);
x=42;
y=30;

while (x!=y) {
    x = x-1;
}

log(x);

# EXPECTED
# 0
# 30
