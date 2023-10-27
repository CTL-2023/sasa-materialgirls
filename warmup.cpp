#include <iostream>
#include <cmath>
using namespace std;

float r1, r2, c1, c2, circlesArea, arcLength; 
const float pi = acos(-1);

void getNumbers() {
    cout << "\nEnter center coordinate of the first circle: ";
    if (!(cin >> c1)) {
        cout << "\nInvalid input. Please enter a numeric value.\nProgram stopped.\n\n";
        exit(EXIT_FAILURE);
    }

    cout << "Enter radius of the first circle: ";
    if (!(cin >> r1)) {
        cout << "\nInvalid input. Please enter a numeric value.\nProgram stopped.\n\n";
        exit(EXIT_FAILURE);
    }
    r1 = std::abs(r1);

    cout << "Enter center coordinate of the second circle: ";
    if (!(cin >> c2)) {
        cout << "\nInvalid input. Please enter a numeric value.\nProgram stopped.\n\n";
        exit(EXIT_FAILURE);
    }

    cout << "Enter radius of the second circle: ";
    if (!(cin >> r2)) {
        cout << "\nInvalid input. Please enter a numeric value.\nProgram stopped.\n\n";
        exit(EXIT_FAILURE);
    }
    r2 = std::abs(r2);
}

void calculations() {
    float triangleBase = std::abs(c2 - c1);

    if (triangleBase >= (r1 + r2)) {
        circlesArea = pi/2 * (r1*r1 + r2*r2);
        arcLength = pi * (r1 + r2);
    }
    else if (triangleBase + r1 <= r2) {
        circlesArea = r2*r2 * pi/2;
        arcLength = r2 * pi;
    }
    else if (triangleBase + r2 <= r1) {
        circlesArea = r1*r1 * pi/2;
        arcLength = r1 * pi;
    }
    else {
        float s = (r1 + r2 + triangleBase) / 2;
        float triangleArea = sqrt(s * (s - r1) * (s - r2) * (s - triangleBase));
        float height = 2 * triangleArea / triangleBase;
        float contactPoint = sqrt(r1*r1 - height*height);
        float phi1 = asin(height/r1);
        float phi2 = asin(height/r2);

        circlesArea = r1*r1 * (pi - phi1)/2 + r2*r2 * (pi - phi2)/2 + triangleArea;
        arcLength = r1 * (pi - phi1) + r2 * (pi - phi2);
    }
}

int main() {
    getNumbers();
    calculations();
    cout << "\nThe area is: " << circlesArea << ", the arclength is: " << arcLength << ".\n";
    main();
	return 0;
}
