import unittest

from .errors import CloseTradeException
from .signal import (BFP, BPS, CB, CCS, CEP, CM, FWP, MCVIP, MVIP, PTS,
                     RM, TCA, VIPCS, WB, Signal)


class TestSignal(unittest.TestCase):
    def _assert_signal(self, cls, text, sig):
        s = Signal.parse(cls.chan_id, text)
        self.assertEqual(s.coin, sig.coin)
        self.assertEqual(s.entries, sig.entries)
        self.assertEqual(s.sl, sig.sl)
        self.assertEqual(s.targets, sig.targets)
        self.assertEqual(s.fraction, sig.fraction)
        self.assertEqual(s.leverage, sig.leverage)
        self.assertEqual(s.tag, cls.__name__)


class TestBFP(TestSignal):
    def test_1(self):
        self._assert_signal(
            BFP, """Binance Futures  Signal
Long/Buy #LINK/USDT 32.605
Targets 32.735 - 32.865 - 33.061 - 33.420 - 33.909
Stoploss 31.626
Leverage 5-10x
By (@BFP)
👆🏼👆🏼This is an Early signal. Buy #LINK when it comes around the entry price and maintain the stop loss """
            """- Just Trade with 3 to 5% of Total funds""",
            Signal("LINK", [32.605], [32.735, 32.865, 33.061, 33.42, 33.909], 31.626, 0.05, 10))

    def test_2(self):
        self._assert_signal(
            BFP, """Binance Future Signal
👇🏻👇🏻Early Signal - (IMPORTANT) This Trade should only be made, when the market price touches the  ENTRY POINT
Long/Buy #BLZ/USDT ️
Entry Point - 28390
Targets: 28500 - 28615 - 28730 - 28950 - 29525
Leverage - 10x
Stop Loss - 26970
By (@BFP)
✅✅Maintain the stop loss & Just Trade with 3 to 5% of Total funds""",
            Signal("BLZ", [28390], [28500, 28615, 28730, 28950, 29525], 26970, 0.05, 10))

    def test_3(self):
        self._assert_signal(
            BFP, """Binance Future Signal
👇🏻Early Signal - (IMPORTANT) This Trade should only be made, when the market price touches the  ENTRY POINT

Short/Sell #ALICE/USDT ️

Entry Point - 5.930

Targets: 5.905 - 5.885 - 5.855 - 5.815 - 5.690
Leverage - 10x
Stop Loss - 6.290
By (@BFP)
✅✅Maintain the stop loss & Just Trade with 3 to 5% of Total funds""",
            Signal("ALICE", [5.93], [5.905, 5.885, 5.855, 5.815, 5.69], 6.29, 0.05, 10))

    def test_4(self):
        self._assert_signal(
            BFP, """Binance Future Signal
👇🏻👇🏻Early Signal - (IMPORTANT) This Trade should only be made, when the market price touches the  ENTRY POINT

Long/Buy #SAND/USDT ️

Entry Point - 35145

Targets: 35285 - 35425 - 35565 - 35845 - 36550
Leverage - 10x
Stop Loss - 33030
By (@BFP)
✅✅Maintain the stop loss & Just Trade with 3 to 5% of Total funds""",
            Signal("SAND", [35145], [35285, 35425, 35565, 35845, 36550], 33030, 0.05, 10))


class TestBPS(TestSignal):
    def test_1(self):
        self._assert_signal(
            BPS, """Binance Futures/Bitmex/Bybit/Bitseven Signal# 1325
Get into Long #LTC/USDT @ 176
Leverage – 10x
Target - 177-178-181-186
Stop Loss - 168""", Signal("LTC", [176], [177, 178, 181, 186], 168, 0.03, 10))

    def test_2(self):
        coin = None
        try:
            self._assert_signal(
                BPS, """(in reply to Bitmex Premium Signals)
> Binance Futures/Bitmex/Bybit/Bitseven Signal# 1327
> Get into Long #LTC/USDT @ 174…
Exit trade with minor loss""", None)
        except CloseTradeException as exp:
            coin = exp.coin
        self.assertEqual(coin, "LTC")


class TestCCS(TestSignal):
    def test_1(self):
        self._assert_signal(
            CCS, """📊 FUTURES (BINANCE)

#ALGOUSDT

LONG Below : 1.038

MAX 👉5x-7x LEVERAGE Hold

TAKE PROFIT:1.065+""", Signal("ALGO", [1.038], [1.065], leverage=10))

    def test_2(self):
        self._assert_signal(
            CCS, """📊 FUTURES (BINANCE)

#FLMUSDT

LONG Below : 0.5820-0.5750

MAX 👉5x-7x LEVERAGE Hold

TAKE PROFIT: 0.6055|0.6330+""", Signal("FLM", [0.582, 0.575], [0.6055, 0.633], leverage=10))

    def test_3(self):
        self._assert_signal(
            CCS, """📊 FUTURES (BINANCE)

#TRBUSDT

LONG Below : 62.00

MAX 👉5x-7x LEVERAGE Hold

TAKE PROFIT: 64.20|65.10|69.10+

SL: 58.85""", Signal("TRB", [62], [64.2, 65.1, 69.1], 58.85, leverage=10))


class TestFWP(TestSignal):
    def test_1(self):
        self._assert_signal(
            FWP, """#DOGEUSDT #LONG

BUY : 0.3400$- 0.3650$
TAKE PROFIT:
TARGET 1 : 0.3850$
TARGET 2 : 0.4000$
TARGET 3 : 0.4140$
TARGET 4 : 0.4300$
TARGET 5 : 0.4400$
TARGET 6 : 0.4500$
TARGET 7  : 0.4600$
TARGET 8  : 0.4700$

❗️STOL LOSS : 0.28$

Use 2% Fund Only

LEVERAGE:  10X-20X (CROSS)

BUY & HOLD ✅""", Signal("DOGE", [0.34, 0.365], [0.385, 0.4, 0.414, 0.43, 0.44], 0.28, 0.02, 10))

    def test_2(self):
        self._assert_signal(
            FWP, """#ONT/USDT #LONG
(BINANCE FUTURES )
BUY : 2.25$- 2.38$
TAKE PROFIT:
TARGET 1 : 2.52$
TARGET 2 : 2.60$
TARGET 3 : 2.67$
TARGET 4 : 2.73$
TARGET 5 : 2.80$
TARGET 6 : 2.88$
TARGET 7 : 2.98$

❗️STOL LOSS :2.15$

Use 2% Fund Only ❗️

LEV :  10X-20X (CROSS)

BUY & HOLD ✅""", Signal("ONT", [2.25, 2.38], [2.52, 2.6, 2.67, 2.73, 2.8], 2.15, 0.02, 10))


class TestMCVIP(TestSignal):
    def test_1(self):
        self._assert_signal(
            MCVIP, """BTCUSDT LONG 36705-36200
Target 37000-37400-38000-38500
Leverage 10x
Stop 35680""", Signal("BTC", [36705, 36200], [37000, 37400, 38000, 38500], 35680, 0.05, 10))

    def test_2(self):
        self.assertRaises(
            AssertionError,
            self._assert_signal,
            MCVIP, """ETHUSDT Buy 2580-2626
Targets 2800-3050-3300
Stop 2333""", None)

    def test_3(self):
        coin = None
        try:
            self._assert_signal(
                MCVIP, """Close algo""", None)
        except CloseTradeException as exp:
            coin = exp.coin
        self.assertEqual(coin, "ALGO")


class TestMVIP(TestSignal):
    def test_1(self):
        self._assert_signal(
            MVIP, """⚡️⚡️ #BNB/USDT⚡️⚡️

Entry Zone :
390,50 - 391,00
Take-Profit Targets:

1) 394,91
2) 410,55
3) 430,10

Leverage ×10

Stop Targets:

1) 312,80""", Signal("BNB", [390.5, 391], [394.91, 410.55, 430.10], 312.8, 0.02, 10))

    def test_2(self):
        self._assert_signal(
            MVIP, """⚡️⚡️ #CTK/USDT ⚡️⚡️

Entry Zone:
1.500 - 1.501

Take-Profit Targets:
1) 1.560
2) 1.650
3) 1.750

Levrage ×50

Stop Targets:
1) 1.400""", Signal("CTK", [1.5, 1.501], [1.56, 1.65, 1.75], 1.4, 0.02, 10))

    def test_3(self):
        self.assertRaises(
            AssertionError,
            self._assert_signal,
            MVIP, """⚡️⚡️ #HNT/USDT ⚡️⚡️

Entry Zone:
16,0000 - 16,0700

Take-Profit Targets:

1) 19,2840
2) 24,0700
3) 32,0700

Stop Targets:

1) 15,7486""", None)

    def test_4(self):
        self._assert_signal(MVIP, """⚡️⚡️ #LTC/USDT⚡️⚡️

Entry Zone:
174 - 175

Take-Profit Targets:

1) 176
2) 178

Leverage : ×50

Stop Targets:
1) 170""", Signal("LTC", [174, 175], [176, 178], 170, 0.02, 10))

    def test_5(self):
        self.assertRaises(AssertionError, self._assert_signal, MVIP, """[In reply to 👑 MVIP 👑]
Close second trade when first tp hit 🎯""", None)

    def test_6(self):
        coin = None
        try:
            self._assert_signal(
                MVIP, """[In reply to 👑 MVIP 👑]
Close #BTC/USDT""", None)
        except CloseTradeException as exp:
            coin = exp.coin
        self.assertEqual(coin, "BTC")

    def test_7(self):
        coin = "UNKNOWN"
        try:
            self._assert_signal(
                MVIP, """🛑 Close all trades  🛑""", None)
        except CloseTradeException as exp:
            coin = exp.coin
        self.assertEqual(coin, None)


class TestTCA(TestSignal):
    def test_1(self):
        self._assert_signal(
            TCA, """Asset: EOS/USDT
Position: #LONG
Entry: 5.850 - 5.950
Targets: 6.000 - 6.100 - 6.300 - 6.500
Stop loss: 5.600
Leverage: 75x""", Signal("EOS", [5.85, 5.95], [6, 6.1, 6.3, 6.5], 5.6, 0.03, 75))

    def test_2(self):
        self._assert_signal(
            TCA, """Leverage Trading Signal
Pair: BTC/USDT #LONG
Leverage: cross 100x (not more than 3-4% balance)
Targets : 39000 - 39500 - 40000 - 41800
Entry : 38500 - 38700
SL: 37300""", Signal("BTC", [38500, 38700], [39000, 39500, 40000, 41800], 37300, 0.03, 100))

    def test_3(self):
        coin = None
        try:
            self._assert_signal(
                TCA, """Close position
BTC by 35091
Profit is +300%""", None)
        except CloseTradeException as exp:
            coin = exp.coin
        self.assertEqual(coin, "BTC")

    def test_4(self):
        coin = "UNKNOWN"
        try:
            self._assert_signal(
                TCA, """Closing all positions. Leaving the market""", None)
        except CloseTradeException as exp:
            coin = exp.coin
        self.assertEqual(coin, None)


class TestCB(TestSignal):
    def test_1(self):
        self._assert_signal(
            CB, """#BAL|USDT (Binance Futures)

LONG (Place A Bid)
Lvg. : 5x - 10x

Entry  : 26.36$ - 27.36$
Targets :  28.06$ - 29$ - 34$ - 50$ - 65$

StopLoss : 25.289$

https://www.tradingview.com/""",
            Signal("BAL", [26.36, 27.36], [28.06, 29, 34, 50, 65], 25.289, 0.03, 10))


class TestWB(TestSignal):
    def test_1(self):
        self._assert_signal(
            WB, """#SKLUSDT FUTURE Call
#LONG
BUY Order:- 0.38000-0.38500

Sell :- 0.38700-0.39000-0.39300-0.395000-0.4000

Use 10X Leverage

STOP LOSS:- 0.25000""",
            Signal("SKL", [0.38, 0.385], [0.387, 0.39, 0.393, 0.395, 0.4], 0.25, 0.03, 10))


class TestRM(TestSignal):
    def test_1(self):
        self._assert_signal(
            RM, """⚡️⚡️ #BTC/USDT ⚡️⚡️

Client: Binance Futures
Trade Type: Regular (LONG)
Leverage: Isolated (10.0X)

Entry Zone:
38500 - 38980

Take-Profit Targets:
1) 39265 - 20%
2) 39700 - 20%
3) 40100 - 20%
4) 40500 - 20%
5) 41000 - 20%

Stop Targets:
1) 36430 - 100.0%

Risk level 8/10
Published By:
provided by : @CVIP""",
            Signal("BTC", [38500, 38980], [39265, 39700, 40100, 40500, 41000], 36430, 0.03, 10))


class TestVIPCS(TestSignal):
    def test_1(self):
        self._assert_signal(
            VIPCS, """➡️ SHORT LINKUSDT | Binance

❇️ Buy: 27.00000000

☑️ Target 1: 22.95000000 (15%)

☑️ Target 2: 18.90000000 (30%)

☑️ Target 3: 14.85000000 (45%)

⛔️ Stoploss: 31.05000000  (-15%)

💫 Leverage : 10x""", Signal("LINK", [27], [22.95, 18.9, 14.85], 31.05, 0.05, 10))


class TestCEP(TestSignal):
    def test_1(self):
        self._assert_signal(
            CEP, """#ETHUSDT

📍 SHORT

Leverage : 20x

📍Use 2% of Total Account

Buy : 2700 - 2660 - 2630

Sell Targets ::

2600 - 2560 - 2510 - 2460 - 2400 - 2300 - 2200 - 2100

🔻 StopLoss : 2850


#Crypto ✅""", Signal("ETH", [2700, 2660, 2630], [2600, 2560, 2510, 2460, 2400], 2850, 0.02, 10)
        )


class TestCM(TestSignal):
    def test_1(self):
        self._assert_signal(
            CM, """Binance Futures  Call ‼️

#LTCUSDT  PERP
⬆️Long  Call

❇️ Entry :  162$ - 165$

Target 1 : 168$
Target 2 : 173$
Target 3 : 179$
Target 4 : 183$
Target 5 : 193$

➡️Leverage   :  5x - 10x
⛔️Stop Loss  :  159$

Use Only 2-5% Of Your Total Portfolio


https://www.tradingview.com/""", Signal("LTC", [162, 165], [168, 173, 179, 183, 193], 159, 0.03, 10)
        )


class TestPTS(TestSignal):
    def test_1(self):
        self._assert_signal(
            PTS, """Binance Futures  Call ‼️

#ANKRUSDT  PERP
⬆️Long  Call

❇️ Entry :  0.10352$ - 0.10745$

Target 1 : 0.10951$
Target 2 : 0.12$
Target 3 : 0.15$
Target 4 : 0.18$
Target 5 : 0.21$

➡️Leverage   :  5x - 10x
⛔️Stop Loss  :  0.10164$

Use Only 2-5% Of Your Total Portfolio

https://www.tradingview.com/""",
            Signal("ANKR", [0.10352, 0.10745], [0.10951, 0.12, 0.15, 0.18, 0.21], 0.10164, 0.03, 10)
        )