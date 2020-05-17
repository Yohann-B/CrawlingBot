CC = g++
OPTCPU = -Wall -O3


#.o FILES
MAIN = src/main.o
ROBOT = src/QR_bot_simu.o
LEG = src/leg_simu.o
INPUT = src/input.o
OFILES = $(MAIN) $(ROBOT) $(LEG) $(INPUT)

#data FILES
DATA_COORD = dataOut/coord/FL_coord.csv dataOut/coord/FR_coord.csv dataOut/coord/RL_coord.csv dataOut/coord/RR_coord.csv
DATA_ANGLE = dataOut/angle/FL_angle.csv dataOut/angle/FR_angle.csv dataOut/angle/RL_angle.csv dataOut/angle/RR_angle.csv
DATA = $(DATA_ANGLE) $(DATA_COORD)

#FINAL GOAL
EXEC = simu

#RULES
default : $(EXEC)
#RULE TO MAKE .o's FROM .cpp's
$(ROBOT) : src/QR_bot_simu.cpp
	$(CC) $(OPTCPU) -o $@ -c $<
$(LEG) : src/leg_simu.cpp
	$(CC) $(OPTCPU) -o $@ -c $<
$(INPUT) : src/input.cpp
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
