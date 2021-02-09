from pprint import pprint
import requests as req
import bs4 as bs
from string import whitespace


class GetCurrency:

    def __init__(self):
        self.url = 'https://el-change.com'
        self.html = req.get(self.url).text
        self.soup = bs.BeautifulSoup(self.html, 'html.parser')
        self.give_away = ''
        self.get = ''
        self.give_away_dict = {}
        self.get_list = []

    def parsing_give(self):
        self.give_away_dict = {}
        self.give_away = self.soup.find('div', {'class': 'otdaete_wrap'}).find_all('div', {"class": "obmen_btns"})
        for currency in self.give_away:
            self.give_away_dict[f'{currency.attrs["title"]}'] = [currency.attrs["num_recive"],
                                                                 [currency.attrs["min_summ"],
                                                                  currency.attrs["max_summ"]]]
        return self.give_away_dict

    def parsing_get(self, num_receive):
        self.get_list = []
        self.get = self.soup.find('div', {'class': "poluchaete_wrap"}).find('div', {"num_recive": num_receive}).find_all(
            'div', {"class": "obmen_btns"})
        for currency in self.get:
            self.get_list.append(
                [currency.attrs["title"], f'{currency.attrs["send_course"]}:{currency.attrs["recive_course"]}',
                 currency.contents[5].text.translate(dict.fromkeys(map(ord, whitespace)))])
        return self.get_list


if __name__ == "__main__":
    parser = GetCurrency()
    # pprint(parser.parsing_give())
    pprint(parser.parsing_get(num_receive='recive_7'))
