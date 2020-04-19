#ifndef _QR_BOT_SIMU_H_
#define _QR_BOT_SIMU_H_

#include "leg_simu.h"
#include "const.h"
class QR_bot_simu{

	private:
	leg_simu _legs[4];			// Leg objects that represent the 4 legs of the bot.
	float _direction;	// Angle defining the direction which the robot is pointing to.
	float _speed;		// Moving speed of the robot: The highest is this "speed", the further the robot will go onwards at each step.
	float _newDir;
	float _newSpd;
	int _sequence;		// Define the robot's way of moving itself. Each number correspond to a predefined sequence.
	bool _orientation;

	public:
	// Builders
	QR_bot_simu(leg_simu *legs);
	~QR_bot_simu();

	// Readers
	leg_simu *legs_read();
	float direction_read();
	float speed_read();
	float newDir_read();
	float newSpd_read();
	int sequence_read();

	// Writers
	void legs_write(leg_simu *legs);
	void direction_write(float dir);
	void speed_write(float spd);
	void newDir_write(float newDir);
	void newSpd_write(float newSpd);
	void sequence_write(int sequence);

	// Methods
	//// A voir si l'on veut utiliser l'argument "speed" chargé par une autre fonction
	//// (dans le cas d'une détection d'obstacle par exemple) ou si l'on veut le donner
	//// à cette fonction comme argument. Le deuxième cas permettrait d'avoir une bonne
	//// synchronisation sans avoir à faire tant d'effort de conception, mais limitera
	//// probablement les options de développement.
	//// Edit:
	//// Cette fonction ne calcule ni le nouvel angle ni la nouvelle vitesse, elle les
	//// récupère toutes deux d'un autre calcul. Cett fonction doit simplement calculer
	//// les points de contacts pour chaque jambe pour la prochaine phase de dépolacement.
	//// Ainsi on a pas besoin de prendre des nouvelles valeurs, simplement les valeurs
	//// des paramètres de la classe préalablement chargés par une autre fonction.
	//// edit target: del "float newDir, float newSpd"
	//// Edit 2:
	//// Les paramètres _direction et _speed donne une information sur l'état actuel du
	//// système. Ainsi il est important qu'ils ne soient pas chargés avec des infos qui
	//// concernent un état futur, mais qu'ils isoient mis à jour au moment où ces infos
	//// futures sont traitées.
	//// edit2 target: creation des attributs "_newDir" et "_newSpd".
	float *traj2leg();
	void updatePos(float *newCoord);
	void moveLeg(int leg, std::array <float, 3> coord);

};
#endif
