#include "leg_simu.h"
#include <string>
#include <math.h>
#include <iostream>
#include <iomanip>

leg_simu::leg_simu(){

}


leg_simu::leg_simu(int *pin, bool orientation, input &param){
	param.find_key("LENGTH_A", _length_A, 49.5);
	param.find_key("LENGTH_B", _length_B, 60);
	param.find_key("LENGTH_C", _length_C, 99);
	param.find_key("INIT_X", _init_X, 0);
	param.find_key("INIT_Y", _init_Y, 100);
	param.find_key("INIT_Z", _init_Z, -50);
	param.find_key("MAX_Z", _max_Z, 10);
	param.find_key("TILT_ANGLE", _tilt_angle, 90);
	param.find_key("TRAJ_LEG_SAMPLES", _leg_traj_samples, 99);

	_orientation = orientation;
	_h_speed = H_SPEED;
	_v_speed = V_SPEED;

	for (int i=0; i<3; i++){
		_servoPin[i]= *pin;
		pin++;
	}

	// Buffer initialization with initiation position:
	_init_coord_buff[0] = this->_init_X;
	_init_coord_buff[1] = this->_init_Y;
	_init_coord_buff[2] = this->_init_Z;

	float R = sqrt(_coord_buff[0]*_coord_buff[0]+_coord_buff[1]*_coord_buff[1]);

	_angle_buff[0] = acos((this->_length_A*this->_length_A+this->_length_B*this->_length_B-this->_length_C*this->_length_C)/(2*this->_length_A*this->_length_B));	//// AJOUTER LA CONVERSION
	_angle_buff[1] = atan(_coord_buff[2]/(R-this->_length_A))+acos((this->_length_B*this->_length_B+_coord_buff[2]*_coord_buff[2]+(R-this->_length_A)*(R-this->_length_A)-this->_length_C*this->_length_C)/(2*this->_length_B*sqrt(_coord_buff[2]*_coord_buff[2]+(R-this->_length_A)*(R-this->_length_A))));
	_angle_buff[2] = acos((this->_length_B+this->_length_C-_coord_buff[2]*_coord_buff[2]-(R-this->_length_A)*(R-this->_length_A))/(2*this->_length_B*this->_length_C));

	_register_buff[0] = MIN_REG+_angle_buff[0]/180*(MAX_REG-MIN_REG);	//// AJOUTER LA CONVERSION
	_register_buff[1] = MIN_REG+_angle_buff[1]/180*(MAX_REG-MIN_REG);
	_register_buff[2] = MIN_REG+_angle_buff[2]/180*(MAX_REG-MIN_REG);

	// It would be good to make sure that the position is the one used by the model
	// by calling moveServo() during the initiation process->
}

leg_simu::~leg_simu(){}

// Readers:
std::array <float, 3> leg_simu::coordBuff_read(){
	return this->_coord_buff;
}

std::array <float, 3> leg_simu::initCoordBuff_read(){
	return this->_init_coord_buff;
}


std::array <float, 3> leg_simu::angleBuff_read(){
	return this->_angle_buff;
}

std::array <int, 3> leg_simu::registerBuff_read(){
	return this->_register_buff;
}

int* leg_simu::servoPin_read(){
	return this->_servoPin;
}

int leg_simu::hSpeed_read(){
	return this->_h_speed;
}

int leg_simu::vSpeed_read(){
	return this->_v_speed;
}

std::vector <float> leg_simu::ytraj_read(){
	return this->_ytraj;
}

std::vector <float> leg_simu::ztraj_read(){
	return this->_ztraj;
}

float leg_simu::init_X_read(){
	return this->_init_X;
}

float leg_simu::init_Y_read(){
	return this->_init_Y;
}

float leg_simu::init_Z_read(){
	return this->_init_Z;
}

// Writers:
void leg_simu::coordBuff_write(std::array <float, 3> coordinates){
	for(int i=0; i<3; i++){
		_coord_buff[i] = coordinates[i];
	}
}

void leg_simu::initCoordBuff_write(std::array <float, 3> initCoord){
	for(int i=0; i<3; i++){
		_init_coord_buff[i] = initCoord[i];
	}
}

void leg_simu::angleBuff_write(std::array <float, 3> angles){
	for(int i=0; i<3; i++){
		_coord_buff[i] = angles[i];
	}
}

void leg_simu::registerBuff_write(std::array <int, 3> regval){
	for(int i=0; i<3; i++){
		_coord_buff[i] = regval[i];
	}
}

void leg_simu::servoPin_write(int *pin){
	for(int i=0; i<3; i++){
		_coord_buff[i] = *pin;
		pin++;
	}
}

void leg_simu::hSpeed_write(int hSpeed){
	_h_speed = hSpeed;
}

void leg_simu::vSpeed_write(int vSpeed){
	_v_speed = vSpeed;
}

void leg_simu::ytraj_write(std::vector <float> ytraj){
	_ytraj = ytraj;
}

void leg_simu::ztraj_write(std::vector <float> ztraj){
	_ztraj = ztraj;
}


// cleaner

void leg_simu::xtraj_clear(){
	this->_xtraj.clear();
}

void leg_simu::ytraj_clear(){
	this->_ytraj.clear();
}

void leg_simu::ztraj_clear(){
	this->_ztraj.clear();
}

void leg_simu::angleA_clear(){
	this->_angleA.clear();
}

void leg_simu::angleB_clear(){
	this->_angleB.clear();
}

void leg_simu::angleC_clear(){
	this->_angleC.clear();
}

// Methods
/* conv2angle:
// This function is used to convert the Cartesian coordinates to angles in the leg coordinates->
// The leg coordinates are given by the 3 servo-motors of the leg->
// First coordinate is the body-hip link, 2nd is the hip-femur link, third is femur-tibia link->
*/

/*
std::array <float, 3> leg_simu::conv2angle(){
	std::array <float, 3> angle = {90, 90, 90};
	float R = sqrt(_coord_buff[0]*_coord_buff[0]+_coord_buff[1]*_coord_buff[1]);

	angle[0] = acos((this->_length_A*this->_length_A+this->_length_B*this->_length_B-this->_length_C*this->_length_C)/(2*this->_length_A*this->_length_B));
	angle[1] = atan(this->_coord_buff[2]/(R-this->_length_A))+acos((this->_length_B*this->_length_B+this->_coord_buff[2]*this->_coord_buff[2]+(R-this->_length_A)*(R-this->_length_A)-this->_length_C*this->_length_C)/(2*this->_length_B*sqrt(this->_coord_buff[2]*this->_coord_buff[2]+(R-this->_length_A)*(R-this->_length_A))));
	angle[2] = acos((this->_length_B+this->_length_C-this->_coord_buff[2]*this->_coord_buff[2]-(R-this->_length_A)*(R-this->_length_A))/(2*this->_length_B*this->_length_C));

	return angle;
}*/

void leg_simu::conv2angle(){

	int nbr_elem = this->_xtraj.size();
	for(int i=0; i<nbr_elem; i++){

		float R = sqrt(this->_xtraj[i]*this->_xtraj[i]+this->_ytraj[i]*this->_ytraj[i]);
		float l = sqrt(this->_ztraj[i]*this->_ztraj[i]+(R-this->_length_A)*(R-this->_length_A));


		_angleA.push_back(atan(this->_xtraj[i]/this->_ytraj[i])*180/M_PI);
		_angleB.push_back((acos(-this->_ztraj[i]/l)+acos((this->_length_C*this->_length_C-this->_length_B*this->_length_B-l*l)/(-2*this->_length_B*l)))*180/M_PI);
		_angleC.push_back(acos((l*l-this->_length_C*this->_length_C-this->_length_B*this->_length_B)/(-2*this->_length_C*this->_length_B))*180/M_PI);
	}

}

std::array <int, 3> leg_simu::conv2reg(float *angle){
	std::array <int, 3> regVal;
	for(int i=0; i<3; i++){
		regVal[i] = MIN_REG + *angle /180*(MAX_REG-MIN_REG); ;//// COMPLETER AVEC LA VALEUR DE REGISTRE CORRESPONDANTE
		angle++;
	}

	return regVal;
}

void leg_simu::saveCoord(std::fstream &file){
	int nbr_elem =this->_xtraj.size();
	for(int i=0; i<nbr_elem; i++){
			file<<std::setprecision(10)<<this->_xtraj.at(i)<<","<<std::setprecision(10)<<this->_ytraj.at(i)<<","<<std::setprecision(10)<<this->_ztraj.at(i)<<"\n";
	}
}

void leg_simu::saveAngle(std::fstream &file){
	int nbr_elem =this->_angleA.size();
	for(int i=0; i<nbr_elem; i++){
			file<<std::setprecision(10)<<this->_angleA.at(i)<<","<<std::setprecision(10)<<this->_angleB.at(i)<<","<<std::setprecision(10)<<this->_angleC.at(i)<<"\n";
	}
}


void leg_simu::calctraj(int choice){
	// We want this function to return an array of x and y coordinates of the traj to reach

	float l_gap = this->_init_coord_buff[0] - this->_coord_buff[0];
	// if the leg needs to reach a point forward, direction = 1, 0 otherwise.
	bool direction = 0;

	if (l_gap < 0){
		l_gap=-l_gap;
		direction = 1;
	}

	float x_gap;
	if (_init_coord_buff[0]<_coord_buff[0])
		x_gap = _init_coord_buff[0] + l_gap/2;
	else
		x_gap = _init_coord_buff[0] - l_gap/2;

	std::vector<float> xtraj;
	std::vector<float> ytraj;
	std::vector<float> ztraj;

	if(choice == PARABOLA){
		if (direction == 1){
			for(int i = 0; i<this->_leg_traj_samples; i++){
				xtraj.push_back(-l_gap/2 + i*l_gap/(this->_leg_traj_samples-1));
				ytraj.push_back(this->_init_Y);
				ztraj.push_back(this->_max_Z+(this->_init_Z-this->_max_Z)/(l_gap*l_gap/4)*xtraj[i]*xtraj[i]);

				xtraj[i] = xtraj[i] + x_gap;
			}
		}
		else{
			for(int i = this->_leg_traj_samples-1; i>=0; i--){
				xtraj.push_back(-l_gap/2 + i*l_gap/(this->_leg_traj_samples-1));
				ytraj.push_back(this->_init_Y);
				ztraj.push_back(this->_max_Z+(this->_init_Z-this->_max_Z)/(l_gap*l_gap/4)*xtraj[this->_leg_traj_samples-1-i]*xtraj[this->_leg_traj_samples-1-i]);

				xtraj[this->_leg_traj_samples-1-i] = xtraj[this->_leg_traj_samples-1-i] + x_gap;
			}
		}
	}

	if(choice == FREEZE_Z){
		if (direction == 1){
			for(int i = 0; i<this->_leg_traj_samples; i++){
				xtraj.push_back(-l_gap/2 + i*l_gap/(this->_leg_traj_samples-1) + x_gap);
				ytraj.push_back(this->_init_Y);
				ztraj.push_back(_init_coord_buff[2]);
			}
		}
		else{
			for(int i = this->_leg_traj_samples-1; i>=0; i--){
				xtraj.push_back(-l_gap/2 + i*l_gap/(this->_leg_traj_samples-1) + x_gap);
				ytraj.push_back(this->_init_Y);
				ztraj.push_back(_init_coord_buff[2]);
			}
		}
	}

	if(choice == TILTED_PARABOLA){
		if (direction == 1){
			for(int i = 0; i<this->_leg_traj_samples; i++){
				xtraj.push_back(-l_gap/2 + i*l_gap/(this->_leg_traj_samples-1));
				ztraj.push_back(this->_max_Z+(this->_init_Z-this->_max_Z)/(l_gap*l_gap/4)*xtraj[i]*xtraj[i]);
				ytraj.push_back(this->_init_Y + (ztraj[i]-this->_init_Z)/tan(this->_tilt_angle*M_PI/180));

				xtraj[i] = xtraj[i] + x_gap;
			}
		}
		else{
			for(int i = this->_leg_traj_samples-1; i>=0; i--){
				xtraj.push_back(-l_gap/2 + i*l_gap/(this->_leg_traj_samples-1));
				ztraj.push_back(this->_max_Z+(this->_init_Z-this->_max_Z)/(l_gap*l_gap/4)*xtraj[this->_leg_traj_samples-1-i]*xtraj[this->_leg_traj_samples-1-i]);
				ytraj.push_back(this->_init_Y + (ztraj[i]-this->_init_Z)/tan(this->_tilt_angle*M_PI/180));
				xtraj[this->_leg_traj_samples-1-i] = xtraj[this->_leg_traj_samples-1-i] + x_gap;
			}
		}
	}

	this->_xtraj.insert(_xtraj.end(), xtraj.begin(), xtraj.end());
	this->_ytraj.insert(_ytraj.end(), ytraj.begin(), ytraj.end());
	this->_ztraj.insert(_ztraj.end(), ztraj.begin(), ztraj.end());
}

void leg_simu::freeze(){
	for(int i=0; i<this->_leg_traj_samples; i++){
		this->_xtraj.push_back(this->_init_coord_buff[0]);
		this->_ytraj.push_back(this->_init_coord_buff[1]);
		this->_ztraj.push_back(this->_init_coord_buff[2]);
	}
}
