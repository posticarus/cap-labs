var x:int;
var s:string;

s = "hi";
x=10;

while (x > 0){
      x = x - 1;
      s = s + "!";
}

log(s);
s = "bye";
log(s + " " + s)

# EXPECTED
# hi!!!!!!!!!!
# bye bye