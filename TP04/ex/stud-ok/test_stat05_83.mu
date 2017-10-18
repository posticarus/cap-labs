if 1 + 1 == 3 {
	log("This must not be displayed.");
} else if 1 + 1 == 1 {
	log("This must not be displayed.");
} else {
	log("This must be displayed.");
}
# EXPECTED
# This must be displayed.