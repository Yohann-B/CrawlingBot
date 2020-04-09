#ifndef _CONST_H_
#define _CONST_H_

#define INIT_DIR      0
#define INIT_SPD      0.5
#define INIT_SEQ      1

#define INIT_X        3
#define INIT_Y        0
#define INIT_Z        -5
#define HIGH_Z        3

#define ANGLE_MAX     100
#define L_MAX         asin(ANGLE_MAX)*LENGTH_A

#define H_SPEED       10
#define V_SPEED       10

// Quad robot's leg characteristics (ATTENTION UNITES)
#define LENGTH_A      49.5
#define LENGTH_B      60
#define LENGTH_C      99

#define MAX_REG			  480
#define MIN_REG			  120
#define MIDPOS_REG 		MIN_REG+(MAX_REG-MIN_REG)/2

#endif
