#include "leg_simu.h"
#include <string>
#include <math.h>
#include <iostream>

using namespace std;
leg_simu::leg_simu(){

}


leg_simu::leg_simu(int *pin, bool orientation){

	_orientation = orientation;
	_h_speed = H_SPEED;
	_v_speed = V_SPEED;

	for (int i=0; i<3; i++){
		_servoPin[i]= *pin;
		pin++;
	}

	// Buffer initialization with initiation position:
	_coord_buff[0] = INIT_X;
	_coord_buff[1] = INIT_Y;
	_coord_buff[2] = INIT_Z;

	float R = sqrt(_coord_buff[0]*_coord_buff[0]+_coord_buff[1]*_coord_buff[1]);

	_angle_buff[0] = acos((LENGTH_A*LENGTH_A+LENGTH_B*LENGTH_B-LENGTH_C*LENGTH_C)/(2*LENGTH_A*LENGTH_B));	//// AJOUTER LA CONVERSION
	_angle_buff[1] = atan(_coord_buff[2]/(R-LENGTH_A))+acos((LENGTH_B*LENGTH_B+_coord_buff[2]*_coord_buff[2]+(R-LENGTH_A)*(R-LENGTH_A)-LENGTH_C*LENGTH_C)/(2*LENGTH_B*sqrt(_coord_buff[2]*_coord_buff[2]+(R-LENGTH_A)*(R-LENGTH_A))));
	_angle_buff[2] = acos((LENGTH_B+LENGTH_C-_coord_buff[2]*_coord_buff[2]-(R-LENGTH_A)*(R-LENGTH_A))/(2*LENGTH_B*LENGTH_C));

	_register_buff[0] = MIN_REG+_angle_buff[0]/180*(MAX_REG-MIN_REG);	//// AJOUTER LA CONVERSION
	_register_buff[1] = MIN_REG+_angle_buff[1]/180*(MAX_REG-MIN_REG);
	_register_buff[2] = MIN_REG+_angle_buff[2]/180*(MAX_REG-MIN_REG);

	// It would be good to make sure that the position is the one used by the model
	// by calling moveServo() during the initiation process->
}

leg_simu::~leg_simu(){}

// Readers:
float* leg_simu::coordBuff_read(){
	return this->_coord_buff;
}

float* leg_simu::initCoordBuff_read(){
	return this->_init_coord_buff;
}


float* leg_simu::angleBuff_read(){
	return this->_angle_buff;
}

int* leg_simu::registerBuff_read(){
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

float *leg_simu::ytraj_read(){
	return this->_ytraj;
}

float *leg_simu::ztraj_read(){
	return this->_ztraj;
}

// Writers:
void leg_simu::coordBuff_write(float *coordinates){
	for(int i=0; i<3; i++){
		_coord_buff[i] = *coordinates;
		coordinates++;
	}
}

void leg_simu::initCoordBuff_write(float *initCoord){
	for(int i=0; i<3; i++){
		_init_coord_buff[i] = *initCoord;
		initCoord++;
	}
}

void leg_simu::angleBuff_write(float *angles){
	for(int i=0; i<3; i++){
		_coord_buff[i] = *angles;
		angles++;
	}
}

void leg_simu::registerBuff_write(int *regval){
	for(int i=0; i<3; i++){
		_coord_buff[i] = *regval;
		regval++;
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

void leg_simu::ytraj_write(float *ytraj){
	_ytraj = ytraj;
}

void leg_simu::ztraj_write(float *ztraj){
	_ztraj = ztraj;
}
// Methods
/* conv2angle:
// This function is used to convert the Cartesian coordinates to angles in the leg coordinates->
// The leg coordinates are given by the 3 servo-motors of the leg->
// First coordinate is the body-hip link, 2nd is the hip-femur link, third is femur-tibia link->
*/
float *leg_simu::conv2angle(float *cartesian){
	float angle[3]={90, 90, 90};
	float R = sqrt(_coord_buff[0]*_coord_buff[0]+_coord_buff[1]*_coord_buff[1]);

	angle[0] = acos((LENGTH_A*LENGTH_A+LENGTH_B*LENGTH_B-LENGTH_C*LENGTH_C)/(2*LENGTH_A*LENGTH_B));
	angle[1] = atan(this->_coord_buff[2]/(R-LENGTH_A))+acos((LENGTH_B*LENGTH_B+this->_coord_buff[2]*this->_coord_buff[2]+(R-LENGTH_A)*(R-LENGTH_A)-LENGTH_C*LENGTH_C)/(2*LENGTH_B*sqrt(this->_coord_buff[2]*this->_coord_buff[2]+(R-LENGTH_A)*(R-LENGTH_A))));
	angle[2] = acos((LENGTH_B+LENGTH_C-this->_coord_buff[2]*this->_coord_buff[2]-(R-LENGTH_A)*(R-LENGTH_A))/(2*LENGTH_B*LENGTH_C));

	float *a = angle;
	return a;
}

int *leg_simu::conv2reg(float *angle){
	int regVal[3];
	for(int i=0; i<3; i++){
		regVal[i] = MIN_REG+ *angle /180*(MAX_REG-MIN_REG); ;//// COMPLETER AVEC LA VALEUR DE REGISTRE CORRESPONDANTE
		angle++;
	}
	int *r = regVal;
	return r;
}

void leg_simu::saveCoord(string file, int iter){
/*
	string titreReg = "regData_";
	titreReg += to_string(this->_servoPin[0]);
	titreReg += ".txt";

  ofstream saveReg;
  saveReg.open(titreReg);

	int *regData = this->registerBuff_read();
	for (int i=0; i<3; i++){
    if (i==0)
      save << to_string(iter) << "  ";
    save << *regData <<"  ";
    regData++;
    if (i==2)
      save << "\n";
  }
	saveReg.close;

  string titreAng = "angData_";
  titreAng += to_string(this->_servoPin[0]);
  titreAng += ".txt";

	ofstream saveAng;
  saveAng.open(titreAng);

  float *angData = this->angleBuff_read();
  for (int i=0; i<3; i++){
    if (i==0)
      save << to_string(iter) << "  ";
    save << *angData << " ";
    angData++;
    if (i==2)
      save << "\n";
  }
	saveAng.close;

  string titreCoo = "cooData_";
  titreCoo += to_string(this->_servoPin[0]);
  titreCoo += ".txt";

	ofstream saveCoo;
  saveCoo.open(titreCoo);

  float *cooData = this->coordBuff_read();
  for (int i=0; i<3; i++){
    if (i==0)
      save << to_string(iter) << "  ";
    save << *cooData << " ";
    cooData++;
    if (i==2)
      save << "\n";
  }
	saveCoo.close;*/
}

void leg_simu::calctraj(float Zmax, int samples){
	// We want this function to return an array of x and y coordinates of the traj to reach
	float y[samples];
	float z[samples];

	float l_gap = this->_init_coord_buff[2] - this->_coord_buff[2];
	if (l_gap < 0){l_gap=-l_gap;}

	float y_gap;
	if (_init_coord_buff[2]<_coord_buff[2])
		y_gap = _init_coord_buff[2] + l_gap/2;
	else
		y_gap = _init_coord_buff[2] - l_gap/2;

	if (y_gap < 0){y_gap=-y_gap;}

	float ytraj[samples];
	float ztraj[samples];

	for(int i = 0; i<samples; i++){
		ytraj[i] = -l_gap/2 + i*l_gap/(samples-1);
		ztraj[i] = Zmax-(2*Zmax/l_gap)*(2*Zmax/l_gap)*ytraj[i]*ytraj[i];
		ytraj[i] = ytraj[i] - y_gap;
	}

	this->_ytraj=ytraj;
	this->_ztraj=ztraj;
}
