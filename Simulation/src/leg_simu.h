#ifndef _LEG_SIMU_H_
#define _LEG_SIMU_H_

#include <string>
#include "const.h"

using namespace std;


class leg_simu{
	private:
	float _coord_buff[3]; 	// Cartesian coordinates of the position for the servo to reach.
	float _init_coord_buff[3];
	float _angle_buff[3];	// Converted angle value of the position for the servo to reach.
	int _register_buff[3];	// Converted register value of the position for the servo to reach.
	int _servoPin[3];		/* Pin number on the PCA9685 the servo is associated to. Index 0 of the array is servo between the body and
							the hip, index 1 between the hip and the femur and index 2 between the femur and the tibia. Initiated in constructor.*/
	bool _orientation;		// Orientation of the leg (body-hip servo has different orientation for top/right and top/left legs). Initiated in constructor.
	int _h_speed;			// Characterize the speed of the body-hip servo (ms since it is used by delay function).
	int _v_speed;			// Characterize the speed of the hip-femur and femur-tibia servo.

	float *_ytraj;
	float *_ztraj;
	public:
	//Cons-des
	leg_simu();
	leg_simu(int *pin, bool orientation);
	~leg_simu();

	// Readers
	float *coordBuff_read();
	float *initCoordBuff_read();
	float *angleBuff_read();
	int *registerBuff_read();
	int *servoPin_read();
	int hSpeed_read();
	int vSpeed_read();
	float *ytraj_read();
	float *ztraj_read();

	// Writers
	void coordBuff_write(float *coordinates);
	void initCoordBuff_write(float *initCoord);
	void angleBuff_write(float *angles);
	void registerBuff_write(int *regval);
	void servoPin_write(int *pin);
	void hSpeed_write(int hSpeed);
	void vSpeed_write(int vSpeed);
	void ytraj_write(float *ytraj);
	void ztraj_write(float *ztraj);

	// Methods
	float *conv2angle(float *cartesian);
	int *conv2reg(float *angle);
  // We use "saveCoord()" to write the computed positions to a file:
	void saveCoord(string file, int iter);
  void calctraj(float ymax, int samples);
};

#endif
