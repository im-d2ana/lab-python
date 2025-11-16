#include <iostream>
#include <string>
using namespace std;

int main() {
    int n = 8;
    int sum = 0;
    int i = 0;
    
    while (i < n) {
        if (i % 2 == 0 && i != 4) {
            cout << "Четное: " << i << endl;
            int j = 0;
            while (j < 2) {
                if ((j != 0) || i > 3) {
                    cout << "j = " << j << endl;
                }
                sum = sum + i + j;
                j++;
            }
        } else if ((i % 3 != 0) && i != 1) {
            cout << "Не кратно 3 и не 1: " << i << endl;
        }
        
        i++;
    }
    
    string message = "Сумма: ";
    bool isPositive = sum > 0;
    
    if (isPositive && (sum >= 30)) {
        cout << message << sum << endl;
        if ((sum % 2 == 0)) {
            cout << "Четная сумма" << endl;
        } else {
            cout << "Нечетная сумма" << endl;
        }
    } 
    else if (isPositive == false) {
        cout << "Сумма не положительная" << endl;
    }
    else {
        cout << "Сумма малая" << endl;
    }
    
    int counter = 0;
    while ((counter < 2)) {
        cout << "Счетчик: " << counter << endl;
        int y = 0;
        while (y < 2) {
            if ((y == 0) && (counter == 1)) {
                cout << "Особая точка" << endl;
            }
            y = y + 1;
        }
        counter = counter + 1;
    }
    
    int a = 5;
    int b = 10;
    
    if ((a < b) && (b > 8)) {
        cout << "a < b и b > 8" << endl;
        if ((a == 5) || (b == 10)) {
            cout << "Значения стандартные" << endl;
        }
    }
    
    return 0;
}