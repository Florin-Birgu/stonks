import unittest
import time
import pandas as pd
from peterlynchscreener.screener import Screener


class ScreenerTestCase(unittest.TestCase):
    def test_get_eps(self):
        s = Screener("PEP")
        eps = s.get_eps()
        eps.plot()
        self.assertGreater(eps.count(), 1)

    def test_get_de(self):
        s = Screener("PEP")
        de = s.get_de()
        self.assertGreater(de, 0)

    def test_get_de_industry(self):
        s = Screener("PEP")
        de = s.get_de_industry()

        self.assertGreater(de, 0)

    def test_esp_growth(self):
        s = Screener("PEP")
        eps_grow = s.is_eps_growth_met()
        self.assertEqual(eps_grow, False)

    def test_pe_to_industry(self):
        s = Screener("PEP")
        pe_to_industry = s.is_pe_to_industry_met()
        self.assertEqual(pe_to_industry, False)

    def test_de_to_industry(self):
        s = Screener("PEP")
        de_to_industry = s.is_de_to_industry_met()
        self.assertEqual(de_to_industry, False)

    def test_pandas_test(self):
        ticker = "PEP"
        #s = Screener("PEP")
        #de_to_industry = s.is_de_to_industry_met()
        results = pd.DataFrame(columns=['Ticker', 'b', 'pe'])
        #results = results.set_index('Ticker', inplace=True)
        #results.iloc[ticker] = True
        entry = (ticker, True)
        new_row = pd.Series({"Ticker": ticker, "b": True})
        results.loc[-1] = new_row
        print(results)
        self.assertEqual(results.empty, True)


if __name__ == '__main__':
    unittest.main()
