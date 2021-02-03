from pprint import pprint
import requests as req
import bs4 as bs


class GetCurrency:

    def __init__(self):
        self.url = 'https://el-change.com'
        self.html = req.get(self.url).text
        self.soup = bs.BeautifulSoup(self.html, 'html.parser')
        self.give_away = ''
        self.get = ''
        self.give_away_dict = []
        self.get_dict = []

    def parsing_give(self):
        self.give_away = self.soup.find('div', {'class': 'otdaete_wrap'}).find_all('span', {"class": 'valute_text'})
        for test in self.give_away:
            self.give_away_dict.append(test.contents[0])
        return self.give_away_dict

    def parsing_get(self):
        self.get = self.soup.find('div', {'class': "poluchaete_wrap"}).find_all('span', {"class": 'valute_text'})
        for test in self.get:
            self.get_dict.append(test.contents[0])
        return self.get_dict


# if __name__ == '__main__':
#     get = GetCurrency()
#     get.parsing_give()
