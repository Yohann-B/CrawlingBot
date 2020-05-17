#include <iomanip>
#include <math.h>
#include "input.h"

input::input() : fin("par.txt"){

}

input::input(const std::string &file_name) : fin(file_name.c_str()){

}

input::~input(){

}

void input::read(){
  std::string item_temp;
  if(!fin)
    throw("Unable to find the input file.");
  getline(fin, item_temp);
  if(item_temp != "PARAMETER FILE")
    throw("Incorrect format of input file.");
  std::cout << item_temp << std::endl;

  get_items();
}

void input::get_items(){
  std::string line_temp, item_temp, value_temp;
  std::stringstream ss;

  while(! fin.eof()){
    getline(fin, line_temp);
    if(line_temp != ""){
      ss.clear();
      ss.str(line_temp);
      ss >> item_temp;
      ss >> value_temp;
      std::pair<std::string, std::string> item (item_temp, value_temp);
      item_map.insert(item);

      std::cout << std::setw(20) << std::left << item_temp << value_temp << std::endl;
    }
    else std::cout << std::endl;
  }
}
