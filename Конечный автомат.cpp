#include <iostream>
using namespace std;

enum EState {Work, Route, Rotate, Move};
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
		case Route:
			if (det->DeltaAngle(0.5)) {
				state = Rotate;
				if (det->DeltaDistance(1)) {
					state = Move;
				}
			}
		case Work:
			if (det->ClientExists()) {
				state = Route;
				break;
			}
		
		case Rotate:
			com->rotate(1);
			state = Route;
			break;
		}
	}
	void Run() {
		while (1)
			Events();
	}
};



int main() {
	Robot rob;
	rob.Run();
}

