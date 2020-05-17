#ifndef _LEG_SIMU_H_
#define _LEG_SIMU_H_

#include <string>
#include <fstream>
#include <vector>
#include <array>
#include "input.h"
#include "const.h"

class leg_simu{
	private:
	std::array <float, 3> _coord_buff; 	// Cartesian coordinates of the position for the servo to reach.
	std::array <float, 3> _init_coord_buff;
	std::array <float, 3> _angle_buff;// Converted angle value of the position for the servo to reach.
	std::array <int, 3> _register_buff;	// Converted register value of the position for the servo to reach.
	int _servoPin[3];		/* Pin number on the PCA9685 the servo is associated to. Index 0 of the array is servo between the body and
							the hip, index 1 between the hip and the femur and index 2 between the femur and the tibia. Initiated in constructor.*/
	bool _orientation;		// Orientation of the leg (body-hip servo has different orientation for top/right and top/left legs). Initiated in constructor.
	int _h_speed;			// Characterize the speed of the body-hip servo (ms since it is used by delay function).
	int _v_speed;			// Characterize the speed of the hip-femur and femur-tibia servo.

	std::vector <float> _xtraj;
	std::vector <float> _ytraj;
	std::vector <float> _ztraj;
	std::vector <float> _angleA;
	std::vector <float> _angleB;
	std::vector <float> _angleC;

	// Leg's parameters
	float _length_A;
	float _length_B;
	float _length_C;

	float _init_X;
	float _init_Y;
	float _init_Z;
	float _max_Z;

	float _tilt_angle;
	int _leg_traj_samples;

	public:
	//Cons-des
	leg_simu();
	leg_simu(int *pin, bool orientation, input &param);
	~leg_simu();

	// Readers
	std::array <float, 3> coordBuff_read();
  std::array <float, 3> initCoordBuff_read();
	std::array <float, 3> angleBuff_read();
	std::array <int, 3> registerBuff_read();
	int *servoPin_read();
	int hSpeed_read();
	int vSpeed_read();
	std::vector <float> ytraj_read();
	std::vector <float> ztraj_read();
	float init_X_read();
	float init_Y_read();
	float init_Z_read();

	// Writers
	void coordBuff_write(std::array <float, 3> coordinates);
	void initCoordBuff_write(std::array <float, 3> initCoord);
	void angleBuff_write(std::array <float, 3> angles);
	void registerBuff_write(std::array <int, 3> regval);
	void servoPin_write(int *pin);
	void hSpeed_write(int hSpeed);
	void vSpeed_write(int vSpeed);
	void ytraj_write(std::vector <float> ytraj);
	void ztraj_write(std::vector <float> ztraj);

	// Cleaner
	void xtraj_clear();
	void ytraj_clear();
	void ztraj_clear();
	void angleA_clear();
	void angleB_clear();
	void angleC_clear();

	// Methods
	//std::array <float, 3> conv2angle();
	void conv2angle();
	std::array <int, 3> conv2reg(float *angle);
  // We use "saveCoord()" to write the computed positions to a file:
	void saveCoord(std::fstream &file);
	void saveAngle(std::fstream &file);
  void calctraj(int choice);
	void freeze();
};

#endif
