if 1 == 1 {
  log("yes");
}

if 1 == 1 {
  log("yes");
}
else {
  log("no");
}

if 1 == 2 {
  log("no");
}
else {
  log("yes");
}

if 1 == 2 {
  log("no");
}
else if 1 == 1 {
  log("yes");
}
else {
  log("no");
}

# EXPECTED
# yes
# yes
# yes
# yes
