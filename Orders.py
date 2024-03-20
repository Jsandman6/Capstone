class Allocation:
  def __init__(self, ticker, percentage):
    self.ticker = ticker
    self.percentage = percentage
    self.units = 0.0

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

class Goal:
  def __init__(self, name, targetYear, targetValue, initialContribution=0, monthlyContribution=0, priority=""):
    self.name = name
    self.targetYear = targetYear
    self.targetValue = targetValue
    self.initialContribution = initialContribution
    self.monthlyContribution = monthlyContribution
    if not (priority == "") and not (priority in ["Dreams", "Wishes", "Wants", "Needs"]):
            raise ValueError('Wrong value set for Priority.')
    self.priority = priority

  def getGoalProbabilities(self):
    if (self.priority == ""):
            raise ValueError('No value set for Priority.')
    lookupTable=pd.read_csv('./Data/Goal Probability Table.csv')
    match = (lookupTable['Realize'] == self.priority)
    minProb = lookupTable['MinP'][(match)]
    maxProb = lookupTable['MaxP'][(match)]
    return minProb.values[0], maxProb.values[0]

class AccountType():
  def __init__(self, value: str):
    if not value in("Taxable", "Roth IRA", "Traditional IRA"):
      raise ValueError("Allowed types: Taxable, Roth IRA, Traditional IRA")
    self.value = value
  def __eq__(self, other):
      return self.value == other.value

class AccountStatus():
  def __init__(self, value: str):
    if not value in("PENDING", "IN_REVIEW", "APPROVED", "REJECTED", "SUSPENDED"):
      raise ValueError("Allowed statuses: PENDING, IN_REVIEW, APPROVED, REJECTED, SUSPENDED")
    self.value = value
  def __eq__(self, other):
      return self.value == other.value

class Account():
  def __init__(self, number: str, accountType: AccountType, accountStatus: AccountStatus, cashBalance: float=0.0):
    self.goals = []
    self.number = number
    self.cashBalance = cashBalance
    self.accountType = accountType
    self.accountStatus = accountStatus

class Goal:
  def __init__(self, name: str, targetYear: int, targetValue: float, portfolio: Portfolio=None, initialContribution: float=0, monthlyContribution: float=0, priority: str=""):
    self.name = name
    self.targetYear = targetYear
    self.targetValue = targetValue
    self.initialContribution = initialContribution
    self.monthlyContribution = monthlyContribution
    if not (priority == "") and not (priority in ["Dreams", "Wishes", "Wants", "Needs"]):
            raise ValueError("Wrong value set for Priority.")
    self.priority = priority
    self.portfolio = portfolio

  def getGoalProbabilities(self):
    if (self.priority == ""):
            raise ValueError("No value set for Priority.")
    lookupTable=pd.read_csv("./Data/Goal Probability Table.csv")
    match = (lookupTable["Realize"] == self.priority)
    minProb = lookupTable["MinP"][(match)]
    maxProb = lookupTable["MaxP"][(match)]
    return minProb.values[0], maxProb.values[0]

class TransactionType():
  def __init__(self, value: str):
    if not value in("BUY", "SELL"):
      raise ValueError("Allowed types: BUY, SELL.")
    self.value = value
  def __eq__(self, other):
      return self.value == other.value

class OrderStatus():
  def __init__(self, value: str):
    if not value in("NEW", "PENDING", "FILLED", "REJECTED"):
      raise ValueError("Allowed statuses: NEW, PENDING, FILLED, REJECTED.")
    self.value = value
  def __eq__(self, other):
      return self.value == other.value

  class Order:
  def __init__(self, account: Account, goal: Goal, transactionType: TransactionType, status: OrderStatus=OrderStatus("NEW"), dollarAmount: float=0.0):
    
    self.account = account
    self.transactionType = transactionType
    self.dollarAmount = dollarAmount
    self.goal = goal
    self.status = status

class Order:
  def __init__(self, account: Account, goal: Goal, transactionType: TransactionType, status: OrderStatus=OrderStatus("NEW"), dollarAmount: float=0.0):
    
    self.account = account
    self.transactionType = transactionType
    self.dollarAmount = dollarAmount
    self.goal = goal
    self.status = status

  def checkAccountStatus(self) -> bool:
    if self.account.accountStatus == AccountStatus("APPROVED"):
      return True
    else:
      return False

  def checkOrderSize(self) -> bool:
    if self.dollarAmount > 1.00:
      return True
    else:
      return False

  def checkBuyPower(self) -> bool:
    if self.transactionType == TransactionType("BUY") and self.account.cashBalance >= self.dollarAmount:
      return True
    elif self.transactionType == TransactionType("SELL"):
      return True
    else:
      return False

  def checkOrderViability(self) -> bool:
    if self.checkAccountStatus() and self.checkOrderSize() and self.checkBuyPower() and isMarketOpen():
      return True
    else:
      return False

myPortfolio = Portfolio("VTI TLT IEI GLD DBC", expectedReturn = 0.05, portfolioName = "Moderate", riskBucket = 3)
myGoal = Goal(name="Vacation", targetYear=2027, targetValue=10000, priority="Dreams", portfolio=myPortfolio)
myAccount=Account(number="123456789", accountType="Taxable", accountStatus=AccountStatus("APPROVED"), cashBalance=11.0)
myAccount.goals.append(myGoal)

newOrder = Order(account=myAccount, goal=myGoal, transactionType=TransactionType("BUY"), dollarAmount=10.0)
print(newOrder.checkOrderViability())

class SplitOrder:
  def __init__(self, originalOrder: Order, ticker: str, dollarAmount: float):
    
    self.originalOrder = originalOrder
    self.ticker = ticker
    self.dollarAmount = dollarAmount
    self.units = 0

class Order:
  def __init__(self, account: Account, goal: Goal, transactionType: TransactionType, status: OrderStatus=OrderStatus("NEW"), dollarAmount: float=0.0):
    
    self.account = account
    self.transactionType = transactionType
    self.dollarAmount = dollarAmount
    self.goal = goal
    self.status = status

  def checkAccountStatus(self) -> bool:
    if self.account.accountStatus == AccountStatus("APPROVED"):
      return True
    else:
      return False

  def checkOrderSize(self) -> bool:
    if self.dollarAmount > 1.00:
      return True
    else:
      return False

  def checkBalances(self) -> bool:
    if self.transactionType == TransactionType("BUY") and self.account.cashBalance >= self.dollarAmount:
      return True
    elif self.transactionType == TransactionType("SELL"):
      goalValue = 0.0
      for allocation in self.goal.portfolio.allocations:
        price = float(yf.Ticker(allocation.ticker).basic_info["previous_close"])
        goalValue += allocation.units * price
      if self.dollarAmount <= goalValue:
        return True
      else:
        return False
    else:
      return False

  def checkOrderViability(self) -> bool:
    if self.checkAccountStatus() and self.checkOrderSize() and self.checkBalances() and isMarketOpen():
      return True
    else:
      return False

  def split(self) -> list:
    splits = []
    for allocation in self.goal.portfolio.allocations:
      if (allocation.percentage > 0):
        splits.append(SplitOrder(originalOrder=self, ticker=allocation.ticker, dollarAmount=allocation.percentage * self.dollarAmount))
    return splits

class MasterOrder:
  def __init__(self, status: OrderStatus=OrderStatus("NEW")):
    
    self.splitOrders = []
    self.masterTable = pd.DataFrame(columns=['Account','Symbol','Type','DollarAmount'])
    self.status = status

  def addSplitOrder(self, splitOrder: SplitOrder):
    self.splitOrders.append(splitOrder)

  def aggregate(self) -> pd.DataFrame:
    for split in self.splitOrders:
      new_row = {'Account':split.originalOrder.account.number,'Symbol':split.ticker,'Type':split.originalOrder.transactionType.value,'DollarAmount':split.dollarAmount}
      self.masterTable = self.masterTable.append(new_row, ignore_index=True)
    
    return self.masterTable.groupby(['Symbol','Type']).sum().reset_index()
    
  def orderSent(self):
    newStatus = OrderStatus("PENDING")
    self.status = newStatus
    for split in self.splitOrders:
      split.originalOrder.status = newStatus

  def allocateAccounts(self, filledMasterOrderFile: pd.DataFrame) -> pd.DataFrame:
    accountTable = pd.DataFrame(columns=['Account','Symbol','Type','Units'], index=self.masterTable.index)
    for index, row in filledMasterOrderFile.iterrows():
      ordersToAllocate = self.masterTable[(self.masterTable['Symbol'] == row['Symbol']) & (self.masterTable['Type'] == row['Type'])]
      totalValue = float(ordersToAllocate.groupby(['Symbol','Type'])['DollarAmount'].sum()[0])
      for index2, row2 in ordersToAllocate.iterrows():
        unitsAllocated = (row2['DollarAmount'] / totalValue) * row['Units']
        new_row = {'Account':row2['Account'],'Symbol':row2['Symbol'],'Type':row2['Type'],'Units':unitsAllocated}
        accountTable.iloc[index2] = new_row
        self.splitOrders[index2].units = unitsAllocated
        self.splitOrders[index2].originalOrder.account.cashBalance -= unitsAllocated * row['Price']
        #print(self.splitOrders[index2].originalOrder.account.number)
    return accountTable

  def allocateGoals(self):
    for order in self.splitOrders:
      portfolioAllocations = order.originalOrder.goal.portfolio.allocations
      #print(order.originalOrder.goal.portfolio.name)
      for idx, item in enumerate(portfolioAllocations):
        if item.ticker == order.ticker and order.originalOrder.transactionType == TransactionType("BUY"):
          order.originalOrder.goal.portfolio.allocations[idx].units += order.units
          #print(item.ticker + ": " + str(order.units))
        elif item.ticker == order.ticker and order.originalOrder.transactionType == TransactionType("SELL"):
          order.originalOrder.goal.portfolio.allocations[idx].units -= order.units    

  def orderFilled(self):
    newStatus = OrderStatus("FILLED")
    self.status = newStatus
    for split in self.splitOrders:
      split.originalOrder.status = newStatus

myPortfolio2 = Portfolio("VTI TLT IEI GLD DBC", expectedReturn = 0.03, portfolioName = "Conservative", riskBucket = 2)
myGoal2 = Goal(name="Car", targetYear=2025, targetValue=5000, priority="Dreams", portfolio=myPortfolio2)
myAccount2=Account(number="987654321", accountType="Taxable", accountStatus=AccountStatus("APPROVED"), cashBalance=21.0)
myAccount2.goals.append(myGoal2)

