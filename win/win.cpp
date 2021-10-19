#include<iostream>
#include<algorithm>
#include<vector>
#include<string>
#include<fstream>
#include<string>
#include <stdlib.h>
#include <time.h>
using namespace std;
int main()
{
	string str;
	vector<string> s;
	vector<pair<string,string> > ans;
	ifstream file("name_players.txt", ios::in);
	while (file >> str)
		s.push_back(str);
	file.close();
	for (int i = 0; i < s.size(); i++)
		for (int I = i + 1; I < s.size(); I++)
		{
			ans.push_back({ s[i],s[I] });
			ans.push_back({ s[i],s[I] });
		}
	vector<bool> vis;
	vis.resize(ans.size(), 0);
	ofstream file1("Players.txt", ios::out);
	ofstream file2("Players1.txt", ios::out);
	for (int i = 0; i < ans.size(); i++)
	{
		srand(time(NULL));
		int r = rand() % (ans.size() - i);
		int cnt = 0;
		for (int I = 0; I < ans.size(); I++)
		{
			if (cnt == r && !vis[I])
			{
				file1 << ans[I].first << endl << ans[I].second << endl;
				file2 << ans[I].second << endl << ans[I].first << endl;
				vis[I] = true;
			}
			if (!vis[I])
				cnt++;
		}
	}
	file1.close();
	file2.close();
}