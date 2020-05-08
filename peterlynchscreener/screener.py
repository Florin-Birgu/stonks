import pandas as pd
import requests
import math
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Screener:
    def __init__(self, ticker):
        assert isinstance(ticker, str)
        self.ticker = ticker

        ua = UserAgent()
        self.eps_min = 0.10
        self.eps_max = 0.40
        self.header = {
            "User-Agent": ua.random
        }
        self.base_url = "https://www.zacks.com/"

        url = "https://www.zacks.com/stock/research/" + self.ticker + "/industry-comparison"
        page = requests.get(url, headers=self.header)

        self.industry_soup = BeautifulSoup(page.content, 'html.parser')

    def get_eps(self):
        eps_url = "https://widget3.zacks.com/data/chart/json/" + self.ticker + "/eps/www.zacks.com"
        json = requests.get(eps_url, headers=self.header)
        df = pd.read_json(json.text)
        df.index = pd.to_datetime(df.index)
        print(df.head())
        monthly_eps = pd.to_numeric(df['monthly_eps'], errors='coerce')
        print("monthly_eps:", monthly_eps.head())
        return monthly_eps

    def get_pe(self):
        pe = self.industry_soup.select(
            '#financials > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)'
        )[0].text
        pe = float(pe)
        print("pe:", pe)
        return pe

    def get_pe_industry(self):
        pe = self.industry_soup.select(
            '#financials > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > a:nth-child(1)'
        )[0].text
        pe = float(pe)
        print("pe industry:", pe)
        return pe

    # Debt to Equity
    def get_de(self):
        de_url = "https://widget3.zacks.com/data/chart/json/" + self.ticker + "/debt_to_equity/www.zacks.com"
        json = requests.get(de_url, headers=self.header)
        df = pd.read_json(json.text)
        df.index = pd.to_datetime(df.index)
        print(df.head())
        monthly_de = pd.to_numeric(df['monthly_debt_to_equity'], errors='coerce')
        print(monthly_de.head())
        de = monthly_de[0] / 100
        print("de:", de)
        return de

    def get_de_industry(self):
        # TODO lazy load
        de_industry_url = self.industry_soup.select(
            'html body#home div#main_content.content_wrapper div#right_content.right_sticky_wrapper section#quote_ribbon_v2.stock_ribbon_view div.quote_rank_summary div.zr_rankbox.industry_rank p.rank_view a.sector'
        )[0]
        de_industry_url = self.base_url + de_industry_url['href']
        print(de_industry_url)

        page = requests.get(de_industry_url, headers=self.header)
        soup = BeautifulSoup(page.content, 'html.parser')

        de = \
            soup.select(
                "#financial_ratio > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)"
            )[0].text
        de = float(de)
        print("de industry:", de)

        return de

    def is_eps_growth_met(self):
        df = self.get_eps()
        index = 1 if math.isnan(df[0]) else 0
        df = df[index:24 + index]
        df = df.reset_index().iloc[::-1]
        print(df.head())
        d = {'monthly_eps': 'sum'}

        res = df.groupby(df.index // 4).agg(d)
        print(res.head())

        res = res['monthly_eps'].pct_change()
        res = res.dropna()

        print(res.head())
        average = res.mean()

        print("eps growth average:", average)

        return self.eps_min <= average <= self.eps_max

    def is_pe_to_industry_met(self):
        try:
            pe = self.get_pe()
            pe_industry = self.get_pe_industry()
            if math.isnan(pe) or math.isnan(pe_industry):
                return False
            return pe < pe_industry
        except:
            print("An exception occurred in is_pe_to_industry_met")
            return False

    def is_de_to_industry_met(self):
        de = self.get_de()
        de_industry = self.get_de_industry()
        if math.isnan(de) or math.isnan(de_industry):
            return False

        return de < de_industry
