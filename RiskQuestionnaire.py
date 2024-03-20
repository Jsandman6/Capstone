class RiskQuestion:
  def __init__(self, questionText, weight=1):
    self.questionText = questionText
    self.weight = weight
    self.answers = []

class RiskQuestionAnswer:
  def __init__(self, answerText, score, selected=False):
    self.answerText = answerText
    self.score = score
    self.selected = selected

class RiskQuestionnaire:
  def __init__(self):
    self.questions = []


toleranceQuestionnaire = RiskQuestionnaire()

question1 = RiskQuestion("In general, how would your best friend describe you as a risk taker?", 2)
question1.answers.append(RiskQuestionAnswer("A real gambler",4))
question1.answers.append(RiskQuestionAnswer("Willing to take risks after completing adequate research",3))
question1.answers.append(RiskQuestionAnswer("Cautious",2))
question1.answers.append(RiskQuestionAnswer("A real risk avoider",1))

question2 = RiskQuestion("You are on a TV game show and can choose one of the following. Which would you take?")
question2.answers.append(RiskQuestionAnswer("$1,000 in cash",1))
question2.answers.append(RiskQuestionAnswer("A 50% chance at winning $5,000",2))
question2.answers.append(RiskQuestionAnswer("A 25% chance at winning $10,000",3))
question2.answers.append(RiskQuestionAnswer("A 5% chance at winning $100,000",4))

question3 = RiskQuestion("When you think of the word risk which of the following words comes to mind first?")
question3.answers.append(RiskQuestionAnswer("Loss",1))
question3.answers.append(RiskQuestionAnswer("Uncertainty",2))
question3.answers.append(RiskQuestionAnswer("Opportunity",3))
question3.answers.append(RiskQuestionAnswer("Thrill",4))

toleranceQuestionnaire.questions.append(question1)
toleranceQuestionnaire.questions.append(question2)
toleranceQuestionnaire.questions.append(question3)

capacityQuestionnaire = RiskQuestionnaire()

question4 = RiskQuestion("You are able to save money regularly.")
question4.answers.append(RiskQuestionAnswer("Completely false",1))
question4.answers.append(RiskQuestionAnswer("Somewhat true",2))
question4.answers.append(RiskQuestionAnswer("Completely true",3))

question5 = RiskQuestion("You can pay all your monthly bills on time -- including any credit card or other debt.")
question5.answers.append(RiskQuestionAnswer("Completely false",1))
question5.answers.append(RiskQuestionAnswer("Somewhat true",2))
question5.answers.append(RiskQuestionAnswer("Completely true",3))

question6 = RiskQuestion("If you lose money investing today, your current lifestyle would not be impacted.")
question6.answers.append(RiskQuestionAnswer("Completely false",1))
question6.answers.append(RiskQuestionAnswer("Somewhat true",2))
question6.answers.append(RiskQuestionAnswer("Completely true",3))

question7 = RiskQuestion("You do not need to draw down more than 5% of your investment portfolio for any major financial goal in the next five years.")
question7.answers.append(RiskQuestionAnswer("Completely false",1))
question7.answers.append(RiskQuestionAnswer("Somewhat true",2))
question7.answers.append(RiskQuestionAnswer("Completely true",3))

capacityQuestionnaire.questions.append(question4)
capacityQuestionnaire.questions.append(question5)
capacityQuestionnaire.questions.append(question6)
capacityQuestionnaire.questions.append(question7)

print("Risk Tolerance: \n")
for question in toleranceQuestionnaire.questions:
  print(question.questionText)
  for answer in question.answers:
    print(" -" + answer.answerText)
  print("\n")

print("Risk Capacity: \n")
for question in capacityQuestionnaire.questions:
  print(question.questionText)
  for answer in question.answers:
    print(" -" + answer.answerText)
  print("\n")

class RiskQuestionnaire:
  def __init__(self):
    self.questions = []

  def loadQuestionnaire(self, riskQuestionsFileName, riskAnswersFileName, type):

    if not (type in ["Tolerance", "Capacity"]):
            raise ValueError('Type must be Tolerance or Capacity.')

    import pandas as pd
    riskQuestions = pd.read_csv(riskQuestionsFileName).reset_index()
    riskAnswers = pd.read_csv(riskAnswersFileName).reset_index()

    if (type == "Tolerance"):
      toleranceQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Tolerance')].reset_index()
      for index, row in toleranceQuestions.iterrows():
          self.questions.append(RiskQuestion(row['QuestionText'], row['QuestionWeight']))
          answers = riskAnswers[(riskAnswers['QuestionID'] == row['QuestionID'])]
          for indexA, rowA in answers.iterrows():
                self.questions[index].answers.append(RiskQuestionAnswer(rowA['AnswerText'],rowA['AnswerValue']))
    else:
      capacityQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Capacity')].reset_index()
      for index, row in capacityQuestions.iterrows():
          self.questions.append(RiskQuestion(row['QuestionText'], row['QuestionWeight']))
          answers = riskAnswers[(riskAnswers['QuestionID'] == row['QuestionID'])]
          for indexA, rowA in answers.iterrows():
                self.questions[index].answers.append(RiskQuestionAnswer(rowA['AnswerText'],rowA['AnswerValue']))

questionsFileName = './Data/Risk Questions.csv'
answersFileName = './Data/Risk Answers.csv'

toleranceQuestionnaire = RiskQuestionnaire()
toleranceQuestionnaire.loadQuestionnaire(questionsFileName, answersFileName, "Tolerance")

capacityQuestionnaire = RiskQuestionnaire()
capacityQuestionnaire.loadQuestionnaire(questionsFileName, answersFileName, "Capacity")

print("Risk Tolerance: \n")
for question in toleranceQuestionnaire.questions:
  print(question.questionText)
  for answer in question.answers:
    print(" -" + answer.answerText)
  print("\n")

print("Risk Capacity: \n")
for question in capacityQuestionnaire.questions:
  print(question.questionText)
  for answer in question.answers:
    print(" -" + answer.answerText)
  print("\n")

toleranceQuestionnaire.questions[0].answers[1].selected = True
toleranceQuestionnaire.questions[1].answers[0].selected = True
toleranceQuestionnaire.questions[2].answers[2].selected = True

capacityQuestionnaire.questions[0].answers[1].selected = True
capacityQuestionnaire.questions[1].answers[1].selected = True
capacityQuestionnaire.questions[2].answers[2].selected = True
capacityQuestionnaire.questions[3].answers[1].selected = True

class RiskQuestionnaire:
  def __init__(self):
    self.questions = []

  def loadQuestionnaire(self, riskQuestionsFileName, riskAnswersFileName, type):

    if not (type in ["Tolerance", "Capacity"]):
            raise ValueError('Type must be Tolerance or Capacity.')

    import pandas as pd
    riskQuestions = pd.read_csv(riskQuestionsFileName).reset_index()
    riskAnswers = pd.read_csv(riskAnswersFileName).reset_index()

    if (type == "Tolerance"):
      toleranceQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Tolerance')].reset_index()
      for index, row in toleranceQuestions.iterrows():
          self.questions.append(RiskQuestion(row['QuestionText'], row['QuestionWeight']))
          answers = riskAnswers[(riskAnswers['QuestionID'] == row['QuestionID'])]
          for indexA, rowA in answers.iterrows():
                self.questions[index].answers.append(RiskQuestionAnswer(rowA['AnswerText'],rowA['AnswerValue']))
    else:
      capacityQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Capacity')].reset_index()
      for index, row in capacityQuestions.iterrows():
          self.questions.append(RiskQuestion(row['QuestionText'], row['QuestionWeight']))
          answers = riskAnswers[(riskAnswers['QuestionID'] == row['QuestionID'])]
          for indexA, rowA in answers.iterrows():
                self.questions[index].answers.append(RiskQuestionAnswer(rowA['AnswerText'],rowA['AnswerValue']))
    

  def answerQuestionnaire(self):
    for i in range(len(self.questions)):
      question = self.questions[i]
      print(question.questionText)
      for n in range(len(question.answers)):
        answer = question.answers[n]
        print(str(n) + ": " + answer.answerText)
      nChosen = int(input("Choose your answer between 0 and " + str(len(question.answers)-1) + ": "))
      self.questions[i].answers[nChosen].selected = True
      print("\n")

questionsFileName = './Data/Risk Questions.csv'
answersFileName = './Data/Risk Answers.csv'

toleranceQuestionnaire = RiskQuestionnaire()
toleranceQuestionnaire.loadQuestionnaire(questionsFileName, answersFileName, "Tolerance")

capacityQuestionnaire = RiskQuestionnaire()
capacityQuestionnaire.loadQuestionnaire(questionsFileName, answersFileName, "Capacity")

toleranceQuestionnaire.answerQuestionnaire()
capacityQuestionnaire.answerQuestionnaire()

class RiskQuestionnaire:
  def __init__(self):
    self.questions = []
    self.score = 0

  def loadQuestionnaire(self, riskQuestionsFileName, riskAnswersFileName, type):

    if not (type in ["Tolerance", "Capacity"]):
            raise ValueError('Type must be Tolerance or Capacity.')

    import pandas as pd
    riskQuestions = pd.read_csv(riskQuestionsFileName).reset_index()
    riskAnswers = pd.read_csv(riskAnswersFileName).reset_index()

    if (type == "Tolerance"):
      toleranceQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Tolerance')].reset_index()
      for index, row in toleranceQuestions.iterrows():
          self.questions.append(RiskQuestion(row['QuestionText'], row['QuestionWeight']))
          answers = riskAnswers[(riskAnswers['QuestionID'] == row['QuestionID'])]
          for indexA, rowA in answers.iterrows():
                self.questions[index].answers.append(RiskQuestionAnswer(rowA['AnswerText'],rowA['AnswerValue']))
    else:
      capacityQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Capacity')].reset_index()
      for index, row in capacityQuestions.iterrows():
          self.questions.append(RiskQuestion(row['QuestionText'], row['QuestionWeight']))
          answers = riskAnswers[(riskAnswers['QuestionID'] == row['QuestionID'])]
          for indexA, rowA in answers.iterrows():
                self.questions[index].answers.append(RiskQuestionAnswer(rowA['AnswerText'],rowA['AnswerValue']))
    

  def answerQuestionnaire(self):
    for i in range(len(self.questions)):
      question = self.questions[i]
      print(question.questionText)
      for n in range(len(question.answers)):
        answer = question.answers[n]
        print(str(n) + ": " + answer.answerText)
      nChosen = int(input("Choose your answer between 0 and " + str(len(question.answers)-1) + ": "))
      self.questions[i].answers[nChosen].selected = True
      print("\n")

  def calculateScore(self):
    print("Risk Score:")
    myTotalScore = 0
    for question in self.questions:
      for answer in question.answers:
        if (answer.selected == True):
          myTotalScore = myTotalScore + (answer.score * question.weight)
          print(answer.answerText + ": " + str(answer.score * question.weight))
    print("Total Risk Score: " + str(myTotalScore) + "\n")
    self.score = myTotalScore

questionsFileName = './Data/Risk Questions.csv'
answersFileName = './Data/Risk Answers.csv'

toleranceQuestionnaire = RiskQuestionnaire()
toleranceQuestionnaire.loadQuestionnaire(questionsFileName, answersFileName, "Tolerance")

capacityQuestionnaire = RiskQuestionnaire()
capacityQuestionnaire.loadQuestionnaire(questionsFileName, answersFileName, "Capacity")

toleranceQuestionnaire.answerQuestionnaire()
capacityQuestionnaire.answerQuestionnaire()

toleranceQuestionnaire.calculateScore()
capacityQuestionnaire.calculateScore()
