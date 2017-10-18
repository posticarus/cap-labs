while false {
	log("This must not be printed.");
}

log("This must be printed.");

# EXPECTED
# This must be printed.