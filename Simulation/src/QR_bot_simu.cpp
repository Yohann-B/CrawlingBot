#include "QR_bot_simu.h"
#include "leg_simu.h"
#include <math.h>
#include <string>
#include <iostream>

using namespace std;

// Builders

QR_bot_simu::QR_bot_simu(leg_simu *legs) {

	for(int i = 0; i<4; i++){
		_legs[i]= *legs;
		legs++;
	}

	_direction = INIT_DIR;
	_speed = INIT_SPD;
	_sequence = INIT_SEQ;
}

QR_bot_simu::~QR_bot_simu(){
}

// Readers

leg_simu * QR_bot_simu::legs_read(){

	return this->_legs;
}

float QR_bot_simu::direction_read(){
	return this->_direction;
}

float QR_bot_simu::speed_read(){
	return this->_speed;
}

float QR_bot_simu::newDir_read(){
	return this->_newDir;
}

float QR_bot_simu::newSpd_read(){
	return this->_newSpd;
}

int QR_bot_simu::sequence_read(){
	return this->_sequence;
}

// Writers

void QR_bot_simu::legs_write(leg_simu *legs){
	for(int i = 0; i < 4; i++){
		this->_legs[i]= *legs;
		legs++;
	}
}

void QR_bot_simu::direction_write(float dir){
	this->_direction = dir;
}

void QR_bot_simu::speed_write(float spd){
	this->_speed = spd;
}

void QR_bot_simu::newDir_write(float newDir){
	this->_newDir = newDir;
}

void QR_bot_simu::newSpd_write(float newSpd){
	this->_newSpd = newSpd;
}

void QR_bot_simu::sequence_write(int seq){
	this->_sequence = seq;
}

// Methods

float *QR_bot_simu::traj2leg(){

	static float coord[4];
	// Left side - positive limit
	coord[0] = INIT_X + (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) - L_MAX*sin(this->_newDir-this->_direction))/2;
	// left side - negative limit
	coord[1] = INIT_X - (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) - L_MAX*sin(this->_newDir-this->_direction))/2;
	// Right side - positive limit
	coord[2] = INIT_X + (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) + L_MAX*sin(this->_newDir-this->_direction))/2;
	// Right side - negative limit
	coord[3] = INIT_X - (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) + L_MAX*sin(this->_newDir-this->_direction))/2;

return coord;
}

void QR_bot_simu::moveLeg(int leg, std::array <float, 3> coord){

	// We need to call functions that move legs to a new (x,y,z) position:

	this->_legs[leg].coordBuff_write(coord);
	this->_legs[leg].calctraj(PARABOLA);

	this->_legs[leg].initCoordBuff_write(coord);
/*

	//the movement is made in 3 steps:
	//Firstly we put the leg high to move it. We need to set the z coordinate of the leg to a new value.
	float *tempCoord = leg.coordBuff_read();
	*(tempCoord+2) = HIGH_Z;
	leg.coordBuff_write(tempCoord);

	//Secondly we set the final (x,y) pos the leg must be at.
	*tempCoord = newX;
	*(tempCoord+1) = newY;
	leg.coordBuff_write(tempCoord);

  //thirdly we put the leg on the ground by setting it to its previous location.
	*(tempCoord+3) = INIT_Z;
	leg.coordBuff_write(tempCoord);
*/
}


void QR_bot_simu::updatePos(float *newCoord){
	// We want a big _ytraj/_ztraj buffer wher all the sequence is written for
	// each legs.
	for(int i=0; i<4; i++){
		this->_legs[i].ytraj_clear();
		this->_legs[i].ztraj_clear();
	}
	// In case we're using "speed-direction" control, uncoment this and remove the
	// function argumetn:
	//float *newCoord = this->traj2leg();

	switch (this->_sequence){

		case 1:{
			// We will compute the trajectories that legs needs to follow to go forward.
			// Loading the coordinates legs will have to reach.

			// Computing to reach front position with left side:
			this->_legs[0].coordBuff_write({INIT_X, *(newCoord), INIT_Z});
			this->_legs[2].coordBuff_write({INIT_X, *(newCoord), INIT_Z});

			// Computing trajectories legs will have to follow at first:
			this->_legs[0].calctraj(PARABOLA);
			this->_legs[1].freeze();
			this->_legs[2].freeze();
			this->_legs[3].freeze();

			// Filling the buffer of the current position reached:
			this->_legs[0].initCoordBuff_write({INIT_X, *(newCoord), INIT_Z});

			this->_legs[0].freeze();
			this->_legs[1].freeze();
			this->_legs[2].calctraj(PARABOLA);
			this->_legs[3].freeze();

			// Filling the buffer of the current position with reached position:
			this->_legs[2].initCoordBuff_write({INIT_X, *(newCoord), INIT_Z});

			// Computing to back all legs:
			this->_legs[0].coordBuff_write({INIT_X, 0, INIT_Z});
			this->_legs[1].coordBuff_write({INIT_X, *(newCoord+3), INIT_Z});
			this->_legs[2].coordBuff_write({INIT_X, 0, INIT_Z});
			this->_legs[3].coordBuff_write({INIT_X, *(newCoord+3), INIT_Z});

			this->_legs[0].calctraj(FREEZE_Z);
			this->_legs[1].calctraj(FREEZE_Z);
			this->_legs[2].calctraj(FREEZE_Z);
			this->_legs[3].calctraj(FREEZE_Z);

			// Filling the buffer of the current position with reached position:
			this->_legs[0].initCoordBuff_write({INIT_X, 0, INIT_Z});
			this->_legs[1].initCoordBuff_write({INIT_X, *(newCoord+3), INIT_Z});
			this->_legs[2].initCoordBuff_write({INIT_X, 0, INIT_Z});
			this->_legs[3].initCoordBuff_write({INIT_X, *(newCoord+3), INIT_Z});

			// Computing to reach front position with
			this->_legs[1].coordBuff_write({INIT_X, *(newCoord+2), INIT_Z});
			this->_legs[3].coordBuff_write({INIT_X, *(newCoord+2), INIT_Z});

			this->_legs[0].freeze();
			this->_legs[1].calctraj(PARABOLA);
			this->_legs[2].freeze();
			this->_legs[3].freeze();

			// Filling the buffer of the current position with reached position:
			this->_legs[1].initCoordBuff_write({INIT_X, *(newCoord+2), INIT_Z});

			this->_legs[0].freeze();
			this->_legs[1].freeze();
			this->_legs[2].freeze();
			this->_legs[3].calctraj(PARABOLA);

			// Filling the buffer of the current position with reached position:
			this->_legs[3].initCoordBuff_write({INIT_X, *(newCoord+2), INIT_Z});


			this->_legs[0].coordBuff_write({INIT_X, *(newCoord+1), INIT_Z});
			this->_legs[1].coordBuff_write({INIT_X, 0, INIT_Z});
			this->_legs[2].coordBuff_write({INIT_X, *(newCoord+1), INIT_Z});
			this->_legs[3].coordBuff_write({INIT_X, 0, INIT_Z});

			this->_legs[0].calctraj(FREEZE_Z);
			this->_legs[1].calctraj(FREEZE_Z);
			this->_legs[2].calctraj(FREEZE_Z);
			this->_legs[3].calctraj(FREEZE_Z);

			// Filling the buffer of the current position with reached position:
			this->_legs[0].initCoordBuff_write({INIT_X, *(newCoord+1), INIT_Z});
			this->_legs[1].initCoordBuff_write({INIT_X, 0, INIT_Z});
			this->_legs[2].initCoordBuff_write({INIT_X, *(newCoord+1), INIT_Z});
			this->_legs[3].initCoordBuff_write({INIT_X, 0, INIT_Z});
		}break;

		case 2:{
			// Loading next point to reach for the Front left and rear right legs:
			this->_legs[0].coordBuff_write({INIT_X, *(newCoord), INIT_Z}); // (+) for left side
			this->_legs[3].coordBuff_write({INIT_X, *(newCoord+2), INIT_Z}); // (+) for right side

			// Loading next point to reach for the Front right and rear left legs:
			this->_legs[1].coordBuff_write({INIT_X, *(newCoord+3), INIT_Z}); // (-) for right side
			this->_legs[2].coordBuff_write({INIT_X, *(newCoord+1), INIT_Z}); // (-) for left side

			// Moving the two first forward while moving the two seconds backwards with
			// contact with the ground:
			this->_legs[0].calctraj(PARABOLA);
			this->_legs[1].calctraj(FREEZE_Z);
			this->_legs[2].calctraj(FREEZE_Z);
			this->_legs[3].calctraj(PARABOLA);

			// Filling the buffer of the current position with reached position:
			this->_legs[0].initCoordBuff_write({INIT_X, *(newCoord), INIT_Z});
			this->_legs[1].initCoordBuff_write({INIT_X, *(newCoord+3), INIT_Z});
			this->_legs[2].initCoordBuff_write({INIT_X, *(newCoord+1), INIT_Z});
			this->_legs[3].initCoordBuff_write({INIT_X, *(newCoord+2), INIT_Z});

			// Redoing the same in the opposite direction.

			// Loading next point to reach for the Front left and rear right legs:
			this->_legs[1].coordBuff_write({INIT_X, *(newCoord+2), INIT_Z}); // (+) for right side
			this->_legs[2].coordBuff_write({INIT_X, *(newCoord), INIT_Z}); // (+) for left side

			// Loading next point to reach for the Front right and rear left legs:
			this->_legs[0].coordBuff_write({INIT_X, *(newCoord+1), INIT_Z}); // (-) for left side
			this->_legs[3].coordBuff_write({INIT_X, *(newCoord+3), INIT_Z}); // (-) for right side

			// Moving the two first forward while moving the two seconds backwards with
			// contact with the ground:
			this->_legs[0].calctraj(FREEZE_Z);
			this->_legs[1].calctraj(PARABOLA);
			this->_legs[2].calctraj(PARABOLA);
			this->_legs[3].calctraj(FREEZE_Z);

			// Filling the buffer of the current position with reached position:
			this->_legs[0].initCoordBuff_write({INIT_X, *(newCoord+1), INIT_Z});
			this->_legs[1].initCoordBuff_write({INIT_X, *(newCoord+2), INIT_Z});
			this->_legs[2].initCoordBuff_write({INIT_X, *(newCoord), INIT_Z});
			this->_legs[3].initCoordBuff_write({INIT_X, *(newCoord+3), INIT_Z});

		}break;
}
	// UNE BOUCLE VIENT D'ETRE TERMINEE. FIN DE LA FONCTION.
}
