if 1 + 1 == 3 {
	log("This must not be displayed.");
} else if 1 + 1 == 2 {
	log("This must be displayed.");
} else {
	log("This must not be displayed.");
}
# EXPECTED
# This must be displayed.