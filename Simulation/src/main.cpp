#include "leg_simu.h"
#include "QR_bot_simu.h"
#include <iostream>
#include <fstream>

#define TIME_DELAY 100
#define FL_OR 0
#define FR_OR 1
#define BL_OR 1
#define BR_OR 0

using namespace std;

void bufferPrinter(float *buff, int elem);
void bufferPrinter(int *buff, int elem);

int main(){

  int fl_pin[3] = {0, 1, 2};
  int fr_pin[3] = {3, 4, 5};
  int bl_pin[3] = {6, 7, 8};
  int br_pin[3] = {9, 10, 11};

  leg_simu fl_leg(fl_pin, FL_OR);
  leg_simu fr_leg(fr_pin, FR_OR);
  leg_simu bl_leg(bl_pin, BL_OR);
  leg_simu br_leg(br_pin, BR_OR);

  // Put all the angle data in one var to store them in a file
  leg_simu legStack[4] = {fl_leg, fr_leg, bl_leg, br_leg};

  float *robotData_1 = legStack->angleBuff_read();
  float *robotData_2 = (legStack+1)->angleBuff_read();
  float *robotData_3 = (legStack+2)->angleBuff_read();
  float *robotData_4 = (legStack+3)->angleBuff_read();

  float robotData[12]={*robotData_1, *(robotData_1+1), *(robotData_1+2), *robotData_2, *(robotData_2+1), *(robotData_2+2),
  *robotData_3, *(robotData_3+1), *(robotData_3+2), *robotData_4, *(robotData_4+1), *(robotData_4+2)};
  bufferPrinter(robotData, 12);

  ofstream file;
  file.open("angles.txt");

  file<<"Angle values of each servo of each leg: " << endl;

  for(int i=0; i<12; i++){
    file<<"     "<<robotData[i];
  }
  file<<endl;


  cout<< "Reading XYZ buffer: " <<"\n";
  bufferPrinter(fl_leg.coordBuff_read(), 3);
  cout<<"\n";

  cout<< "Reading angle buffer: " <<"\n";
  bufferPrinter(fl_leg.angleBuff_read(), 3);
  cout<<"\n";

  cout<< "Reading register buffer: " <<"\n";
  bufferPrinter(fl_leg.registerBuff_read(), 3);
  cout<<"\n";

  file.close();

  return 0;

}

void bufferPrinter(float *buff, int elem){
  for(int i=0; i<elem; i++){
    cout<<" "<<i+1<<" element: "<<*buff<<"\n";
    buff++;
  }
}

void bufferPrinter(int *buff, int elem){
  for(int i=0; i<elem; i++){
    cout<<" "<<i+1<<" element: "<<*buff<<"\n";
    buff++;
  }
}