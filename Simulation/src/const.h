#ifndef _CONST_H_
#define _CONST_H_

#define INIT_DIR        0
#define INIT_SPD        0.5
#define INIT_SEQ        1

#define ANGLE_MAX       100
#define L_MAX           asin(ANGLE_MAX)*49.5

#define H_SPEED         10
#define V_SPEED         10

#define MAX_REG			    480
#define MIN_REG			    120
#define MIDPOS_REG 		  MIN_REG+(MAX_REG-MIN_REG)/2

#define FL_OR           0
#define FR_OR           1
#define RL_OR           1
#define RR_OR           0

#define FREEZE_Z        0
#define PARABOLA        1
#define TILTED_PARABOLA 2

#define MOVE_SEQUENCE   2

#endif
