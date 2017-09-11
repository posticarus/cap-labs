#include <iostream>
#include <algorithm>
#include <string>
#include <fstream>
#include <vector>
#include <cstdio>
#include <SDL2/SDL.h>
#include <stdint.h>
#include <thread>
#include <signal.h>

#include "structs.h"
#include "debug.h"
#include "screen.h"
#include "simulateur.h"




/* make sure we only read characters belonging to a hexadecimal chain */
std::string stripNonHex(const std::string source) {
	std::string output;
	for (auto c : source) {
		if (('0' <= c && c <= '9')
			|| ('a' <= c && c <= 'f')
			|| ('A' <= c && c <= 'F'))
		output.push_back(c);
	}
	return output;
}

/* convert an hex char to an int */
uword convHex(char c) {
	if ('0' <= c && c <= '9')
		return c - '0';
	if ('a' <= c && c <= 'f')
		return 10 + c - 'a';
	if ('A' <= c && c <= 'F')
		return 10 + c - 'A';
	return 0;
}


/* takes a source and convert it to an array of opcodes */
std::vector<uword> toOpCodes(std::string source) {
	if (source.size() % 4 != 0) {
		printf ("Oups, code incorrect\n");
		exit(1);
		return std::vector<uword>();
	}
	std::vector<uword> out;
	for (unsigned int i = 0; i < source.size(); i += 4) {
		uword temp = 0;
		temp |= (convHex(source[i]) << 12);
		temp |= (convHex(source[i+1]) << 8);
		temp |= (convHex(source[i+2]) << 4);
		temp |= (convHex(source[i+3]));
		out.push_back(temp);
	}
	return out;
}


/* read from binary file
 * deprecated but keep, we never know
 * */
bool readFromBin(std::string file_path, Machine &machine) {
	std::ifstream file(file_path, std::ios::binary | std::ios::ate);
	file.seekg(0, std::ios::end);
	auto file_size = file.tellg();
	if ((file_size & 1) == 1) {
		printf("[Erreur], le fichier n'est pas correct\n");
		return false;
	} else {
		file.seekg(0, std::ios::beg);
		unsigned short code[file_size>>1];
	    char current;
		int i = 0;
		while (file.get(current)) {
			code[i] = ((unsigned char) current) << 8;
			file.get(current);
			code[i] |=(unsigned char) current;
			machine.program.push_back(code[i]);
			i++;
		}
		return true;
	}
}

/* load the program from a path */
bool readFromStr(std::string file_path, Machine &machine) {
	std::ifstream file(file_path);
    if(file.fail()) {
        std::cout << "cannot read file: '" << file_path << "'\n";
        exit(1);
        //Note: returning false does not seem enough so we exit() ourselves
    }
	std::string code_str = std::string((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
	machine.program = toOpCodes(stripNonHex(code_str));
	return true;
}

/* transfer the code to the memory */
void loadCodeToMemory(Machine &machine) {
	for (unsigned int i = 0; i < machine.program.size(); ++i) {
		machine.memory[/*PROGRAM_BEGIN -*/ i] = machine.program[i];
	}
}


bool force_quit = false;
extern volatile bool refresh;
/* function to handle any forced exit */
void handleForceExit(int sig) {
	force_quit = true;
	exit(sig);
}

void tolowercase(std::string &data) {
    std::transform(data.begin(), data.end(), data.begin(), ::tolower);
}

void loadClockTicksRc(const std::string &dir, struct ClockTicks &ct) {
    std::ifstream file(dir + std::string("/config.rc"));
    if (!file.is_open() || file.fail()) {
        std::cout << "Exception reading config.rc\n";
        return; 
    } else {
        std::string keyword;
        unsigned int value;
        while (file >> keyword >> value) {
        tolowercase(keyword);
        if (keyword == "add")
            ct.add_t = value;
        else if (keyword == "sub")
            ct.sub_t = value;
        else if (keyword == "wmem")
            ct.wmem_t = value;
        else if (keyword == "snif")
            ct.snif_t = value;
        else if (keyword == "and")
            ct.and_t = value;
        else if (keyword == "or")
            ct.or_t = value;
        else if (keyword == "xor")
            ct.xor_t = value;
        else if (keyword == "lsl")
            ct.lsl_t = value;
        else if (keyword == "lsr")
            ct.lsr_t = value;
        else if (keyword == "asr")
            ct.asr_t = value;
        else if (keyword == "call")
            ct.call_t = value;
        else if (keyword == "jump")
            ct.jump_t = value;
        else if (keyword == "return")
            ct.return_t = value;
        else if (keyword == "letl")
            ct.letl_t = value;
        else if (keyword == "leth")
            ct.leth_t = value;
        else if (keyword == "copy")
            ct.copy_t = value;
        else if (keyword == "rmem")
            ct.rmem_t = value;
        else if (keyword == "ticks")
            ct.click_constant = value;

        }
        // std::cout<<keyword<<": "<<value<<"\n";
    
    }
    // std::cout<<"file opened";
    file.close();
}

int main(int argc, char* argv[]) {
	if (argc != 3) {
		printf("Syntax: %s {-s,-r,-fulldebug,-q} <file.obj>\n", argv[0]);
		return EXIT_FAILURE;
	}
    ClockTicks ct = clockticks_new();
	{
	using namespace std;
	string dir = argv[0];
	dir.resize(dir.rfind('/')); // dirname of argv[0], i.e. LEIA directory.
	loadClockTicksRc(dir, ct);
	}
	Param param;
	bool quiet = false;
	/* parse the params */
	if (std::string(argv[1]) == "-s") {
		param.step_by_step = true;
		param.debug_output = true;
		param.fast_mode = false;
		param.full_debug = false;
		param.skip_call = false;
    } else if (std::string(argv[1]) == "-skip") {
		param.step_by_step = true;
		param.debug_output = true;
		param.fast_mode = false;
		param.full_debug = false;
		param.skip_call = true;
	} else if (std::string(argv[1]) == "-q") {
		param.step_by_step = false;
		param.debug_output = false;
		param.fast_mode = true;
		param.full_debug = false;
		param.skip_call = false;
		quiet = true;
	} else if (std::string(argv[1]) == "-r") {
		param.step_by_step = false;
		param.debug_output = true;
		param.fast_mode = false;
		param.full_debug = false;
		param.skip_call = false;
	} else if (std::string(argv[1]) == "-fulldebug") {
		param.step_by_step = false;
		param.debug_output = false;
		param.fast_mode = false;
		param.full_debug = true;
		param.skip_call = false;
	}
	else {
		param.step_by_step = false;
		param.debug_output = false;
		param.fast_mode = true;
		param.full_debug = false;
		param.skip_call = false;
	}

	/* add interruptions for Ctrl+Z or Ctrl+C */
    /* bad way to deal with signals, but I learned the good way later in time. Shame on me*/
	signal(SIGINT, handleForceExit);
	signal(SIGTSTP, handleForceExit);


	Machine machine;
    machine.clock_ticks = ct;
	machine.in_call = false;
	/* launch the screen with the option to manually refresh the screen deactivated*/
	std::thread screen;
	if (!quiet) {
		screen = std::thread(simulate_screen, std::ref(machine), std::ref(force_quit), std::ref(refresh), true);
	}
	/* if we can read the program */
	if (readFromStr(argv[2], machine)) {
		loadCodeToMemory(machine);
		Uint32 time_exec = SDL_GetTicks();
		if (!param.full_debug) {
            simulate(machine, param);
		} else {
			fullDebug(machine, param);
		}
		if (!quiet) {
			printf("Simulation finished in %d ms\n", SDL_GetTicks() - time_exec);
			printf("Please press the ENTER key");
			getchar();
			force_quit = true;
			printf("\n");
        }
	}


	if (!quiet) {
		screen.join();
		printf("\n");
	}
	return EXIT_SUCCESS;
}
