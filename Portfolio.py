class Portfolio:
  def __init__(self, name, riskBucket, expectedReturn=0, expectedRisk=0):
    self.name = name
    self.riskBucket = riskBucket
    self.allocations = []
    self.expectedReturn = expectedReturn
    self.expectedRisk = expectedRisk

class Allocation:
  def __init__(self, ticker, percentage):
    self.ticker = ticker
    self.percentage = percentage

stocks = Allocation("SPY", 0.6)
bonds = Allocation("TLT", 0.4)
myPortfolio = Portfolio("Growth", 4)
myPortfolio.allocations.append(stocks)
myPortfolio.allocations.append(bonds)

import yfinance as yf
spy = yf.Ticker("SPY")
tlt = yf.Ticker("TLT")

spy.basic_info

import matplotlib.pyplot as plt
import numpy as np

assetClassWeights = [myPortfolio.allocations[0].percentage, myPortfolio.allocations[1].percentage]
assetClassLabels = ["Stocks", "Bonds"]

plt.pie(assetClassWeights, labels = assetClassLabels)
plt.show()

stockMarket = spy.info["market"]
bondMarket = tlt.info["market"]

import pandas as pd
df = pd.DataFrame([[stockMarket,myPortfolio.allocations[0].percentage],[bondMarket,myPortfolio.allocations[1].percentage]])
df = df.groupby(0).sum().reset_index()

assetClassWeights = [df.loc[0][1]]
assetClassLabels = [df.loc[0][0]]

plt.pie(assetClassWeights, labels = assetClassLabels)
plt.show()

sectors1 = spy.info["sectorWeightings"]
sectors2 = tlt.info["sectorWeightings"]

df = pd.DataFrame(sectors1)
df2 = pd.DataFrame(sectors2)
df = df.append(df2)
df.index.name = "index"

df = df.groupby("index", dropna=True).sum().sum().reset_index()

for index, value in sectorLabels.iteritems():
  sectorLabels[index] = (value.capitalize().replace("_", " "))

plt.pie(sectorWeights, labels = sectorLabels)
plt.show()

df = yf.download("SPY TLT", group_by="Ticker", period="20y")

class Portfolio:
  def __init__(self, name, riskBucket, expectedReturn=0, expectedRisk=0):
    self.name = name
    self.riskBucket = riskBucket
    self.allocations = []
    self.expectedReturn = expectedReturn
    self.expectedRisk = expectedRisk

  def getDailyPrices(self, period):
    tickerStringList = ""
    for allocation in self.allocations:
      tickerStringList = tickerStringList + str(allocation.ticker) + " "
    data = yf.download(tickerStringList, group_by="Ticker", period=period)
    data = data.iloc[:, data.columns.get_level_values(1)=="Close"]
    data = data.dropna()
    data.columns = data.columns.droplevel(1)
    return data

stocks = Allocation("SPY", 0.6)
bonds = Allocation("TLT", 0.4)
myPortfolio = Portfolio("Growth", 4)
myPortfolio.allocations.append(stocks)
myPortfolio.allocations.append(bonds)

df = myPortfolio.getDailyPrices("20y")
df

import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# Optimize for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
ef.portfolio_performance(verbose=True)

import matplotlib.pyplot as plt
from pypfopt import plotting
fig, ax = plt.subplots()
ef = EfficientFrontier(mu, S)
plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)
plt.show()

ef.clean_weights()

ef = EfficientFrontier(mu, S)
ef.efficient_return(0.02)
portfolio1 = ef.clean_weights()
print(portfolio1)
ef.efficient_return(0.04)
portfolio2 = ef.clean_weights()
print(portfolio2)
ef.efficient_return(0.05)
portfolio3 = ef.clean_weights()
print(portfolio3)
ef.efficient_return(0.06)
portfolio4 = ef.clean_weights()
print(portfolio4)
ef.efficient_return(0.07)
portfolio5 = ef.clean_weights()
print(portfolio5)

def getDailyPrices(tickerStringList, period):
    data = yf.download(tickerStringList, group_by="Ticker", period=period)
    data = data.iloc[:, data.columns.get_level_values(1)=="Close"]
    data = data.dropna()
    data.columns = data.columns.droplevel(1)
    return data
df = getDailyPrices("VTI TLT IEI GLD DBC", "20y")
df

mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

ef = EfficientFrontier(mu, S)
ef.efficient_return(0.02)
portfolioWeights1 = ef.clean_weights()
print(portfolioWeights1)
ef.efficient_return(0.03)
portfolioWeights2 = ef.clean_weights()
print(portfolioWeights2)
ef.efficient_return(0.04)
portfolioWeights3 = ef.clean_weights()
print(portfolioWeights3)
ef.efficient_return(0.06)
portfolioWeights4 = ef.clean_weights()
print(portfolioWeights4)
ef.efficient_return(0.07)
portfolioWeights5 = ef.clean_weights()
print(portfolioWeights5)

class Portfolio:
  def __init__(self, name, riskBucket, expectedReturn=0, expectedRisk=0):
    self.name = name
    self.riskBucket = riskBucket
    self.allocations = []
    self.expectedReturn = expectedReturn
    self.expectedRisk = expectedRisk

  def getDailyPrices(self, period):
    tickerStringList = ""
    for allocation in self.allocations:
      tickerStringList = tickerStringList + str(allocation.ticker) + " "
    data = yf.download(tickerStringList, group_by="Ticker", period=period)
    data = data.iloc[:, data.columns.get_level_values(1)=="Close"]
    data = data.dropna()
    data.columns = data.columns.droplevel(1)
    return data

  def printPortfolio(self):
    print("Portfolio Name: " + self.name)
    print("Risk Bucket: " + str(self.riskBucket))
    print("Expected Return: " + str(self.expectedReturn))
    print("Expected Risk: " + str(self.expectedRisk))
    print("Allocations: ")
    for allocation in self.allocations:
      print("Ticker: " + allocation.ticker + ", Percentage: " + str(allocation.percentage))

newPortfolio = Portfolio("Aggressive Growth", 5)

for key, value in portfolioWeights5.items():
  newAllocation = Allocation(key, value)
  newPortfolio.allocations.append(newAllocation)

newPortfolio.printPortfolio()

def getPortfolio(riskBucket: int) -> Portfolio:

  df = getDailyPrices("SPY TLT AAPL GOOG MSFT", "20y")

  mu = expected_returns.mean_historical_return(df)
  S = risk_models.sample_cov(df)

  ef = EfficientFrontier(mu, S)
  expectedReturn = 0
  portfolioName = ""

  if(riskBucket == 1):
    expectedReturn = 0.02
    portfolioName = "Conservative"
  elif(riskBucket == 2):
    expectedReturn = 0.04
    portfolioName = "Moderate"
  elif(riskBucket == 3):
    expectedReturn = 0.06
    portfolioName = "Moderate Growth"
  elif(riskBucket == 4):
    expectedReturn = 0.08
    portfolioName = "Growth"
  elif(riskBucket == 5):
    expectedReturn = 0.12
    portfolioName = "Aggressive Growth"
  else:
    return -1

  ef.efficient_return(expectedReturn)
  expectedRisk = ef.portfolio_performance()[1]
  portfolioWeights = ef.clean_weights()

  newPortfolio = Portfolio(portfolioName, riskBucket)
  newPortfolio.expectedReturn = expectedReturn
  newPortfolio.expectedRisk = expectedRisk

  for key, value in portfolioWeights.items():
    newAllocation = Allocation(key, value)
    newPortfolio.allocations.append(newAllocation)

  return newPortfolio

myPortfolio = getPortfolio(5)
myPortfolio.printPortfolio()

class Portfolio:

  def __init__(self, tickerString: str, expectedReturn: float, portfolioName: str, riskBucket: int):

    self.name = portfolioName
    self.riskBucket = riskBucket
    self.expectedReturn = expectedReturn
    self.allocations = []

    from pypfopt.efficient_frontier import EfficientFrontier
    from pypfopt import risk_models
    from pypfopt import expected_returns

    df = self.__getDailyPrices(tickerString, "20y")

    self.mu = expected_returns.mean_historical_return(df)
    self.S = risk_models.sample_cov(df)

    ef = EfficientFrontier(self.mu, self.S)

    ef.efficient_return(expectedReturn)
    self.expectedRisk = ef.portfolio_performance()[1]
    portfolioWeights = ef.clean_weights()

    for key, value in portfolioWeights.items():
      newAllocation = Allocation(key, value)
      self.allocations.append(newAllocation)

  def __getDailyPrices(self, tickerStringList, period):
    data = yf.download(tickerStringList, group_by="Ticker", period=period)
    data = data.iloc[:, data.columns.get_level_values(1)=="Close"]
    data = data.dropna()
    data.columns = data.columns.droplevel(1)
    return data

  def printPortfolio(self):
    print("Portfolio Name: " + self.name)
    print("Risk Bucket: " + str(self.riskBucket))
    print("Expected Return: " + str(self.expectedReturn))
    print("Expected Risk: " + str(self.expectedRisk))
    print("Allocations: ")
    for allocation in self.allocations:
      print("Ticker: " + allocation.ticker + ", Percentage: " + str(allocation.percentage))

  def showEfficientFrontier(self):
      import copy
      import numpy as np
      ef = EfficientFrontier(self.mu, self.S)
      fig, ax = plt.subplots()
      #ef_max_sharpe = copy.deepcopy(ef)
      ef_max_sharpe = EfficientFrontier(self.mu, self.S)
      #ef_return = copy.deepcopy(ef)
      ef_return = EfficientFrontier(self.mu, self.S)
      plotting.plot_efficient_frontier(ef, ax=ax, show_assets=False)

      # Generate random portfolios
      n_samples = 10000
      w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
      rets = w.dot(ef.expected_returns)
      stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
      sharpes = rets / stds
      ax.scatter(stds, rets, marker=".", c=sharpes, cmap="viridis_r")

      # Find the tangency portfolio
      ef_max_sharpe.max_sharpe()
      ret_tangent, std_tangent, _ = ef_max_sharpe.portfolio_performance()
      ax.scatter(std_tangent, ret_tangent, marker="*", s=100, c="r", label="Max Sharpe")

      # Find the return portfolio
      ef_return.efficient_return(self.expectedReturn)
      ret_tangent2, std_tangent2, _ = ef_return.portfolio_performance()
      returnP = str(int(self.expectedReturn*100))+"%"
      ax.scatter(std_tangent2, ret_tangent2, marker="*", s=100, c="y", label=returnP)

      # Output
      ax.set_title("Efficient Frontier for " + returnP + " returns")
      ax.legend()
      plt.tight_layout()
      plt.show()

myPortfolio = Portfolio("SPY TLT AAPL AMZN NFLX GOOGL MSFT", expectedReturn = 0.08, portfolioName = "Aggressive Growth", riskBucket = 5)
myPortfolio.printPortfolio()

myPortfolio.showEfficientFrontier()

class Portfolio:

  def __init__(self, tickerString: str, expectedReturn: float, portfolioName: str, riskBucket: int):

    self.name = portfolioName
    self.riskBucket = riskBucket
    self.expectedReturn = expectedReturn
    self.allocations = []

    from pypfopt.efficient_frontier import EfficientFrontier
    from pypfopt import risk_models
    from pypfopt import expected_returns

    df = self.__getDailyPrices(tickerString, "20y")

    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    ef = EfficientFrontier(mu, S)

    ef.efficient_return(expectedReturn)
    self.expectedRisk = ef.portfolio_performance()[1]
    portfolioWeights = ef.clean_weights()

    for key, value in portfolioWeights.items():
      newAllocation = Allocation(key, value)
      self.allocations.append(newAllocation)

  def __getDailyPrices(self, tickerStringList, period):
    data = yf.download(tickerStringList, group_by="Ticker", period=period)
    data = data.iloc[:, data.columns.get_level_values(1)=="Close"]
    data = data.dropna()
    data.columns = data.columns.droplevel(1)
    return data

  def printPortfolio(self):
    print("Portfolio Name: " + self.name)
    print("Risk Bucket: " + str(self.riskBucket))
    print("Expected Return: " + str(self.expectedReturn))
    print("Expected Risk: " + str(self.expectedRisk))
    print("Allocations: ")
    for allocation in self.allocations:
      print("Ticker: " + allocation.ticker + ", Percentage: " + str(allocation.percentage))

  @staticmethod
  def getPortfolioMapping(riskToleranceScore, riskCapacityScore):
    import pandas as pd
    allocationLookupTable=pd.read_csv('./Data/Risk Mapping Lookup.csv')
    matchTol = (allocationLookupTable['Tolerance_min'] <= riskToleranceScore) & (allocationLookupTable['Tolerance_max'] >= riskToleranceScore)
    matchCap = (allocationLookupTable['Capacity_min'] <= riskCapacityScore) & (allocationLookupTable['Capacity_max'] >= riskCapacityScore)
    portfolioID = allocationLookupTable['Portfolio'][(matchTol & matchCap)]
    return portfolioID.values[0]

myPortfolio = Portfolio("SPY TLT AAPL GOOG MSFT", expectedReturn = 0.12, portfolioName = "Aggressive Growth", riskBucket = 5)
myPortfolio.printPortfolio()


