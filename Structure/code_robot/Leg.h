#ifndef DEF_LEG
#define DEF_LEG

#include <String>

class Leg
{
	private:
	
	float A;
	float B;
	float C;
	String typeServo; // Is it really needed ? Maybe for further development (allowing to go faster and more précisely or to perform more positions)
	float servoRange[2];
	float angles[3];
	
	public:
	
	// Constructeurs/destructeur
	Leg(); // Initialize everything to values that obviously can't brake anything
	Leg(float A, float B, float C); // Not recommended to use
	Leg(float A, float B, float C, float servoRange[], float angles[]); 
	Leg(float A, float B, float C, float servoRange[], float angles[], String typeServo);
	~Leg();
	
	// get/set methods
	float get_A();
	void set_A(float A);
	float get_B();
	void set_B(float B);
	float get_C();
	void set_C(float C);
	String *get_servo();
	void set_servo(String typeServo[]);
	float get_range();
	void set_range(float servoRange[]);
	float *get_angles();
	void set_angles(float angles[]);
	
	// Méthodes "utiles" (déplacement par exemple)
	void 