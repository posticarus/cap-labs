var b : bool;

b = true;

while b {
  log("yes");
  b = false;
}

while b {
  log("no");
}

# EXPECTED
# yes
