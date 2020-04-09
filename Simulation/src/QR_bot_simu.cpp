#include "QR_bot_simu.h"
#include "leg_simu.h"
#include <math.h>
#include <string>


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
// Right side - positive limit
coord[0] = INIT_X + (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) + L_MAX*sin(this->_newDir-this->_direction))/2;
// Right side - negative limit
coord[1] = INIT_X - (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) + L_MAX*sin(this->_newDir-this->_direction))/2;
// Left side - positive limit
coord[2] = INIT_X + (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) - L_MAX*sin(this->_newDir-this->_direction))/2;
// left side - negative limit
coord[3] = INIT_X - (2*L_MAX*this->_newSpd*sin(ANGLE_MAX) - L_MAX*sin(this->_newDir-this->_direction))/2;


return coord;
}

void QR_bot_simu::moveLeg(leg_simu leg, float newX, float newY){



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

}

void QR_bot_simu::updatePos(){
	string step = 0;

	float *newCoord = this->traj2leg();

	switch(this->_sequence)
	case 0:

		if (this->_orientation == 1){ // If crawling forward:

			// Front left leg moving
			float loadingCoord[3]={*(newCoord+2), INIT_Y, INIT_Z};
			this->_legs[0].coordBuff_write(loadingCoord);

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			/*this->_legs[3]._coord_buff[0] = *newCoord;
			this->_legs[3]._coord_buff[1] = INIT_Y;
			this->_legs[3]._coord_buff[2] = INIT_Z;



			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT
			loadingCoord[1]=INIT_X;
			loadingCoord[2]=INIT_Y;
			loadingCoord[3]=INIT_Z;
			this->legs[0].coordBuff_write(loadingCoord);

			this->_legs[1]._coord_buff[0] = *(newCoord+1);
			this->_legs[1]._coord_buff[1] = INIT_Y;
			this->_legs[1]._coord_buff[2] = INIT_Z;

			this->_legs[2]._coord_buff[0] = *(newCoord+3);
			this->_legs[2]._coord_buff[1] = INIT_Y;
			this->_legs[2]._coord_buff[2] = INIT_Z;

			this->_legs[3]._coord_buff[0] = INIT_X;
			this->_legs[3]._coord_buff[1] = INIT_Y;
			this->_legs[3]._coord_buff[2] = INIT_Z;

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			this->_legs[1]._coord_buff[0] = *newCoord;
			this->_legs[1]._coord_buff[1] = INIT_Y;
			this->_legs[1]._coord_buff[2] = INIT_Z;

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			this->_legs[2]._coord_buff[0] = *(newCoord+2);
			this->_legs[2]._coord_buff[1] = INIT_Y;
			this->_legs[2]._coord_buff[2] = INIT_Z;

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			this->_legs[0]._coord_buff[0] = *(newCoord+3);
			this->_legs[0]._coord_buff[1] = INIT_Y;
			this->_legs[0]._coord_buff[2] = INIT_Z;

			this->_legs[1]._coord_buff[0] = INIT_X;
			this->_legs[1]._coord_buff[1] = INIT_Y;
			this->_legs[1]._coord_buff[2] = INIT_Z;

			this->_legs[2]._coord_buff[0] = INIT_X;
			this->_legs[2]._coord_buff[1] = INIT_Y;
			this->_legs[2]._coord_buff[2] = INIT_Z;

			this->_legs[3]._coord_buff[0] = *(newCoord+1);
			this->_legs[3]._coord_buff[1] = INIT_Y;
			this->_legs[3]._coord_buff[2] = INIT_Z;
		}
		else{ // If crawling backwards

			this->_legs[0]._coord_buff[0] = *(newCoord+3);
			this->_legs[0]._coord_buff[1] = INIT_Y;
			this->_legs[0]._coord_buff[2] = INIT_Z;

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			this->_legs[3]._coord_buff[0] = *(newCoord+1);
			this->_legs[3]._coord_buff[1] = INIT_Y;
			this->_legs[3]._coord_buff[2] = INIT_Z;

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			this->_legs[0]._coord_buff[0] = INIT_X;
			this->_legs[0]._coord_buff[1] = INIT_Y;
			this->_legs[0]._coord_buff[2] = INIT_Z;

			this->_legs[1]._coord_buff[0] = *newCoord;
			this->_legs[1]._coord_buff[1] = INIT_Y;
			this->_legs[1]._coord_buff[2] = INIT_Z;

			this->_legs[2]._coord_buff[0] = *(newCoord+2);
			this->_legs[2]._coord_buff[1] = INIT_Y;
			this->_legs[2]._coord_buff[2] = INIT_Z;

			this->_legs[3]._coord_buff[0] = INIT_X;
			this->_legs[3]._coord_buff[1] = INIT_Y;
			this->_legs[3]._coord_buff[2] = INIT_Z;

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			this->_legs[1]._coord_buff[0] = *(newCoord+1);
			this->_legs[1]._coord_buff[1] = INIT_Y;
			this->_legs[1]._coord_buff[2] = INIT_Z;

			this->_legs[2]._coord_buff[0] = *(newCoord+3);
			this->_legs[2]._coord_buff[1] = INIT_Y;
			this->_legs[2]._coord_buff[2] = INIT_Z;

			// AJOUTER UN DELAI QUI ATTEND QUE LA JAMBE AIT TERMINE SON DEPLACEMENT

			this->_legs[0]._coord_buff[0] = *(newCoord+2);
			this->_legs[0]._coord_buff[1] = INIT_Y;
			this->_legs[0]._coord_buff[2] = INIT_Z;

			this->_legs[1]._coord_buff[0] = INIT_X;
			this->_legs[1]._coord_buff[1] = INIT_Y;
			this->_legs[1]._coord_buff[2] = INIT_Z;

			this->_legs[2]._coord_buff[0] = INIT_X;
			this->_legs[2]._coord_buff[1] = INIT_Y;
			this->_legs[2]._coord_buff[2] = INIT_Z;

			this->_legs[3]._coord_buff[0] = *newCoord;
			this->_legs[3]._coord_buff[1] = INIT_Y;
			this->_legs[3]._coord_buff[2] = INIT_Z;*/
		}
	}
