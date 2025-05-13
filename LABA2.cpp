#include <conio.h>
#include <iostream>
#include <stdio.h>
#include <fstream>
using namespace std;
struct cleaner
{
	int power;
	int price;
	int noise;
	string brend;
	string material;
	string version;
	string form;

};

void fill_ctr(cleaner& per) {
	string BREND[4] = { "ROBOROCK", "DREAME", "XIAOMI","DYSON" };
	string MATERIAL[4] = { "PLASTIC", "METAL", "ALUMINUM", "CARBON" };
	string VERSION[4] = { "PRO", "LITE", "STANDARD", "ULTIMATE" };
	string FORM[2] = { "КРУГ", "КВАДРАТ" };

	per.brend = BREND[rand() % 4];
	per.material = MATERIAL[rand() % 4];
	per.version = VERSION[rand() % 4];
	per.form = FORM[rand() % 2];
	per.power = rand() % (10000 - 3000) + 3000;
	per.noise = rand() % (71 - 20) + 20;
	per.price = rand() % (100000 - 10000 + 1) + 10000;
}

void show_struct(cleaner& per) {
	cout << "БРЕНД: " << per.brend << " МАТЕРИАЛ: " << per.material << " Версия: " << per.version << " Форма: " << per.form;
	cout << " Мощность: " << per.power << " Цена: " << per.price << " Уровень шума: " << per.noise << endl;
}

int main()
{
	const int MENU_1 = 49;
	const int MENU_2 = 50;
	const int MENU_3 = 51;
	const int MENU_4 = 52;
	const int MENU_5 = 53;
	const int MENU_6 = 54;
	const int MENU_7 = 55;
	const int MENU_8 = 56;
	const int MENU_EXIT = 27;
	srand(time(0));
	setlocale(LC_ALL, "rus");
	const int n = 15;
	cleaner robot[n];
	int req = 0;

	while (req != MENU_EXIT) {
		system("cls");
		cout << "  1. Заполнить базу случайными данными.\n";
		cout << "  2. Сохранить базу данных в файл.\n";
		cout << "  3. Загрузить базу данных из файла.\n";
		cout << "  4. Показать базу данных.\n";
		cout << "  5. Посчитать кол-во пылесосов каждого бренда.\n";
		cout << "  6. Определить модели с ценой, меньшей чем n руб.\n";
		cout << "  7. Найти модель с мощностью, большей чем среднее арифметическое мощностей и по самой низкой цене.\n";
		cout << "  ESC. Выход.\n";
		req = _getch();
		switch (req)
		{
		case MENU_1: {
			system("cls");
			for (int i = 0; i < n; i++) { fill_ctr(robot[i]); }
			cout << "Заполнил случайно";
			_getch();
			break;
		}
		case MENU_2: {
			system("cls");
			ofstream file("text.t33", ios::binary);
			file.write((char*)robot, sizeof(robot));
			file.close();
			cout << "ЗАПИСАЛ В ФАЙЛ";
			_getch();
			break;
		}
		case MENU_3: {
			system("cls");
			ifstream file("text.t33", ios::binary);
			file.read((char*)robot, sizeof(robot));
			file.close();
			cout << "ПРОЧИТАЛ ИЗ ФАЙЛ";
			_getch();
			break;
		}
		case MENU_4: {
			system("cls");
			for (int i = 0; i < n; i++) { show_struct(robot[i]); }
			_getch();
			break;
		}
		case MENU_5: {
			system("cls");
			int count_roborock = 0, count_dreame = 0, count_xiaomi = 0, count_dyson = 0;
			cout << "Посчитать кол-во пылесосов каждого бренда\n";
			for (int i = 0; i < n; i++) {
				if (robot[i].brend == "ROBOROCK") count_roborock++;
				else if (robot[i].brend == "DREAME") count_dreame++;
				else if (robot[i].brend == "XIAOMI") count_xiaomi++;
				else if (robot[i].brend == "DYSON") count_dyson++;
			}
			cout << "СТАТИСТИКА ПО БРЕНДАМ:\n";
			cout << "ROBOROCK: " << count_roborock << " шт.\n";
			cout << "DREAME: " << count_dreame << " шт.\n";
			cout << "XIAOMI: " << count_xiaomi << " шт.\n";
			cout << "DYSON: " << count_dyson << " шт.\n";
			_getch();
			break;
		}
		case MENU_6: {
			system("cls");
			int price = 0;
			cout << "Определить модели с ценой, меньшей чем n руб.\n";
			cout << "Введите число n: ";
			cin >> price;
			cout << "Модели, дешевле назначенной цены: " << endl;
			for (int i = 0; i < n; i++)
			{
				if (robot[i].price < price)
				{
					show_struct(robot[i]);
				}
			}
			_getch();
			break;
		}
		case MENU_7: {
			system("cls");
			int count = 0, sum = 0;
			for (int i = 0; i < n; i++)
			{
				sum += robot[i].power;
				count++;
			}
			if (count == 0 or sum <= 0) {
				cout << "ERROR";
				_getch();
				break;
			}
			float sr_arif = (float)sum / count;
			int min_price = 110000;
			cleaner pust;
			for (int i = 0; i < n; i++)
			{
				if (robot[i].power > sr_arif and robot[i].price < min_price)
				{
					min_price = robot[i].price;
					pust = robot[i];
				}
			}
			cout << "Найти модель с мощностью, большей чем среднее арифметическое мощностей и по самой низкой цене" << endl;
			cout << "НАЙДЕННАЯ МОДЕЛЬ: " << endl;
			show_struct(pust);
			_getch();
			break;
		}
		}
	}
}
