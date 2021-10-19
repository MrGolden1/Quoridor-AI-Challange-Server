#include<iostream>
#include<algorithm>
#include<vector>
#include<string>
#include<fstream>
#include<string>
#include <stdlib.h>
#include <time.h>
#include<map>
#include <iomanip>
using namespace std;
vector<vector<pair<pair<int, int>, pair<int, int> > > >ans;
map<string, int> w;
int y, cnt = 0;
string str, t[3];
vector<string> s;
vector<pair<int, string> > wm;
void Win(string win)
{
	ifstream file1(win, ios::in);
	while (file1 >> t[0] >> t[1] >> t[2] >> y)
	{
		int sw = 0;
		if (t[2] == t[1])
			sw = 1;
		if (y == 0)
		{
			if (sw == 0)
				ans[w[t[0]]][w[t[1]]].first.first = 1;
			else
				ans[w[t[1]]][w[t[0]]].second.first = 1;
		}
		else
		{
			if (sw == 0)
				ans[w[t[0]]][w[t[1]]].first.second = 1;
			else
				ans[w[t[1]]][w[t[0]]].second.second = 1;
		}
	}
	file1.close();
}
int main()
{
	ifstream file("name_players.txt", ios::in);
	while (file >> str)
		s.push_back(str);
	file.close();
	sort(s.begin(), s.end());
	for (int i = 0; i < s.size(); i++)
		w[s[i]] = i;
	ans.resize(s.size());
	for (int i = 0; i < ans.size(); i++)
		ans[i].resize(s.size());
	Win("win.txt");
	Win("win1.txt");
	for (int i = 0; i < s.size(); i++)
	{
		int a = 0, b = 0;
		for (int I = 0; I < s.size(); I++)
		{
			if (i != I)
			{
				if (ans[i][I].first.first == 1)
					a++;
				else
					b++;
				if (ans[i][I].first.second == 1)
					a++;
				else
					b++;
				if (ans[i][I].second.first == 1)
					a++;
				else
					b++;
				if (ans[i][I].second.second == 1)
					a++;
				else
					b++;
			}
		}
		wm.push_back({ a,s[i] });
	}
	sort(wm.begin(), wm.end());
	while (true)
	{
		system("cls");
		cout << "1- table\n2- player\n3- close\n";
		cin >> y;
		if (y == 1)
		{
			system("cls");
			cout << "No." << setw(15) <<  "Name" << setw(6) << "Wins" << setw(6) << "Loses" << endl;
			for (int i = wm.size() - 1; i > -1; i--)
				cout << s.size() - i << "- " << setw(15) <<  wm[i].second << setw(6) << wm[i].first << setw(6) << (s.size() * 4 - wm[i].first - 4) << endl;
			system("pause>0");
		}
		if (y == 2)
		{
			system("cls");
			for (int i = 0; i < s.size(); i++)
				cout << i + 1 << "- " << s[i] << endl;
			cin >> y;
			y--;
			system("cls");
			for (int i = 0; i < s.size() && y>-1 && y < s.size(); i++)
			{
				if (y != i)
				{
					cout << s[y] << " VS " << s[i] << " --- first : " << s[y] ;
					if((ans[y][i].first.first + 1) % 2 == 0)
						cout << " --- winner : " << s[y] << endl;
					else 
						cout << " --- winner : " << s[i] << endl;
					cout << s[y] << " VS " << s[i] << " --- first : " << s[i] ;
					if((ans[y][i].first.second + 1) % 2 == 0)
						cout << " --- winner : " << s[y] << endl;
					else 
						cout << " --- winner : " << s[i] << endl;
					cout << s[i] << " VS " << s[y] << " --- first : " << s[i] ;
					if(ans[y][i].second.first == 0)
						cout << " --- winner : " << s[i] << endl;
					else 
						cout << " --- winner : " << s[y] << endl;
					cout << s[i] << " VS " << s[y] << " --- first : " << s[y];
					if(ans[y][i].second.second == 0)
						cout << " --- winner : " << s[i] << endl;
					else 
						cout << " --- winner : " << s[y] << endl;
				}
				cout << endl << endl;
			}
			y = 2;
			system("pause>0");
		}
		if (y == 3)
			break;
	}
}