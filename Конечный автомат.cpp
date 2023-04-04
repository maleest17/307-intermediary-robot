#include <iostream>
using namespace std;

enum EState {Work, Drinking, Rotate, Move};
class Detector {
public:
	bool ClientExists();
	bool DeltaAngle(float det);
	bool DeltaDistance(float det);
};

class Commands {
public:
	void rotate(float angle);
	void move(float distance);
};

class Messages {
	void Plug() {
		cout << "Пользователь попил" << endl;
	}

};
class Robot {
	Detector *det;
	EState state;
	Commands *com;
public:
	Robot();
	Robot(Detector*det, Commands*com) {
		state = Work;
	}

	void Events() {
		switch (state) {
		case Drinking:
			if (det->DeltaAngle(0.5)) {
				state = Rotate;
				if (det->DeltaDistance(1)) {
					state = Move;
				}
			}
		case Work:
			if (det->ClientExists()) {
				state = Drinking;
				break;
			}
		
		case Rotate:
			com->rotate(1);
			state = Drinking;
			break;
		}
	}
	void Running() {
		while (1)
			Events();
	}
};



int main() {
	Robot r;
	r.Running();
}

