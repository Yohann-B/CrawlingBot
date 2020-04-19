CC = g++
OPTCPU = -Wall -O3


#.o FILES
MAIN = src/main.o
ROBOT = src/QR_bot_simu.o
LEG = src/leg_simu.o
OFILES = $(MAIN) $(ROBOT) $(LEG)

#data FILES
DATA = dataOut/FL_coord.csv dataOut/FR_coord.csv dataOut/RL_coord.csv dataOut/RR_coord.csv

#FINAL GOAL
EXEC = simu

#RULES
default : $(EXEC)
#RULE TO MAKE .o's FROM .cpp's
$(ROBOT) : src/QR_bot_simu.cpp
	$(CC) $(OPTCPU) -o $@ -c $<
$(LEG) : src/leg_simu.cpp
	$(CC) $(OPTCPU) -o $@ -c $<


#RULES TO MAKE THE FINAL EXECUTABLES
$(EXEC) : $(OFILES)
	$(CC) $(OPTCPU) $^ -o $@

.PHONY : clean cleaner

#CLEANING RULES
clean :
	rm -f $(OFILES)

cleaner :
	rm -f $(OFILES) $(EXEC) $(DATA)
