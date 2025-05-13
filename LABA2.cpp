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
	string FORM[2] = { "ÊÐÓÃ", "ÊÂÀÄÐÀÒ" };

	per.brend = BREND[rand() % 4];
	per.material = MATERIAL[rand() % 4];
	per.version = VERSION[rand() % 4];
	per.form = FORM[rand() % 2];
	per.power = rand() % (10000 - 3000) + 3000;
	per.noise = rand() % (71 - 20) + 20;
	per.price = rand() % (100000 - 10000 + 1) + 10000;
}

void show_struct(cleaner& per) {
	cout << "ÁÐÅÍÄ: " << per.brend << " ÌÀÒÅÐÈÀË: " << per.material << " Âåðñèÿ: " << per.version << " Ôîðìà: " << per.form;
	cout << " Ìîùíîñòü: " << per.power << " Öåíà: " << per.price << " Óðîâåíü øóìà: " << per.noise << endl;
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
		cout << "  1. Çàïîëíèòü áàçó ñëó÷àéíûìè äàííûìè.\n";
		cout << "  2. Ñîõðàíèòü áàçó äàííûõ â ôàéë.\n";
		cout << "  3. Çàãðóçèòü áàçó äàííûõ èç ôàéëà.\n";
		cout << "  4. Ïîêàçàòü áàçó äàííûõ.\n";
		cout << "  5. Ïîñ÷èòàòü êîë-âî ïûëåñîñîâ êàæäîãî áðåíäà.\n";
		cout << "  6. Îïðåäåëèòü ìîäåëè ñ öåíîé, ìåíüøåé ÷åì n ðóá.\n";
		cout << "  7. Íàéòè ìîäåëü ñ ìîùíîñòüþ, áîëüøåé ÷åì ñðåäíåå àðèôìåòè÷åñêîå ìîùíîñòåé è ïî ñàìîé íèçêîé öåíå.\n";
		cout << "  ESC. Âûõîä.\n";
		req = _getch();
		switch (req)
		{
		case MENU_1: {
			system("cls");
			for (int i = 0; i < n; i++) { fill_ctr(robot[i]); }
			cout << "Çàïîëíèë ñëó÷àéíî";
			_getch();
			break;
		}
		case MENU_2: {
			system("cls");
			ofstream file("text.t33", ios::binary);
			file.write((char*)robot, sizeof(robot));
			file.close();
			cout << "ÇÀÏÈÑÀË Â ÔÀÉË";
			_getch();
			break;
		}
		case MENU_3: {
			system("cls");
			ifstream file("text.t33", ios::binary);
if (file.is_open()){
			file.read((char*)robot, sizeof(robot));
			file.close();
			cout << "ÏÐÎ×ÈÒÀË ÈÇ ÔÀÉË";}
else {cout<<"Ошибка при открытие файла"}
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
			cout << "Ïîñ÷èòàòü êîë-âî ïûëåñîñîâ êàæäîãî áðåíäà\n";
			for (int i = 0; i < n; i++) {
				if (robot[i].brend == "ROBOROCK") count_roborock++;
				else if (robot[i].brend == "DREAME") count_dreame++;
				else if (robot[i].brend == "XIAOMI") count_xiaomi++;
				else if (robot[i].brend == "DYSON") count_dyson++;
			}
			cout << "ÑÒÀÒÈÑÒÈÊÀ ÏÎ ÁÐÅÍÄÀÌ:\n";
			cout << "ROBOROCK: " << count_roborock << " øò.\n";
			cout << "DREAME: " << count_dreame << " øò.\n";
			cout << "XIAOMI: " << count_xiaomi << " øò.\n";
			cout << "DYSON: " << count_dyson << " øò.\n";
			_getch();
			break;
		}
		case MENU_6: {
			system("cls");
			int price = 0;
			cout << "Îïðåäåëèòü ìîäåëè ñ öåíîé, ìåíüøåé ÷åì n ðóá.\n";
			cout << "Ââåäèòå ÷èñëî n: ";
			cin >> price;
			cout << "Ìîäåëè, äåøåâëå íàçíà÷åííîé öåíû: " << endl;
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
			cout << "Íàéòè ìîäåëü ñ ìîùíîñòüþ, áîëüøåé ÷åì ñðåäíåå àðèôìåòè÷åñêîå ìîùíîñòåé è ïî ñàìîé íèçêîé öåíå" << endl;
			cout << "ÍÀÉÄÅÍÍÀß ÌÎÄÅËÜ: " << endl;
			show_struct(pust);
			_getch();
			break;
		}
		}
	}
}
