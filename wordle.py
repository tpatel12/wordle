from cmath import pi
from email import feedparser
from json.encoder import INFINITY
import math

import wordList
import random
import matplotlib.pyplot as plt

def getInput():
    feed = ""
    while (not validInput(feed)):
        feed = input("Feedback: ")
    return feed
    
def validInput(str):
    if len(str) != 5:
        return False
    for char in str:
        if not char in ['b','y','g']:
            return False
    return True 

def allFeedbacks():
    return feedbackStrings(5)

def feedbackStrings(x):
    if x == 0:
        return [""]
    newList = []
    for str in feedbackStrings(x-1):
        newList.append(str + "b")
        newList.append(str + "g")
        newList.append(str + "y")
    return newList



def testWord(guess, actual):
    guessList = list(guess)
    actualList = list(actual)
    remaining = list(actual)
    
    #start with all black
    ret = ['b','b','b','b','b']
    
    #set the green ones
    for i in range(5):
        if guessList[i] == actualList[i]:
            ret[i] = 'g'
            remaining.remove(guessList[i])
    
    #Then pass through again to set yellows
    for j in range(5):
        if ret[j] != 'g':
            if guessList[j] in remaining:
                ret[j] = 'y'
                remaining.remove(guessList[j])
    return ''.join(ret)


#gives a numeric score to the guess, using the list or remaining possible answers
def evaluateGuess(guess, remaining_answers):
    
    sum = 0
    
    #For each possible word that the answer could be,
    for trueAnswer in remaining_answers:
        
        #Get the feedback of the guess against that possible answer
        feedback = testWord(guess, trueAnswer)
        if feedback == "ggggg":#["g","g","g","g","g"]:
            continue
        
        #and then count how many answers would be left if that guess was used
        newPossibilities = 0        
        for word in remaining_answers:
            if feedback == testWord(guess, word):
                newPossibilities += 1
            
        #add that number to sum (could be squared for different func)
        sum += newPossibilities
           
    return sum

def evaluateGuess2(guess, remaining_answers, all_feedbacks):
    sum = 0
    for feedback in all_feedbacks:
        counter = 0
        for answer in remaining_answers:
            if testWord(guess, answer) == feedback:
                counter += 1
        sum += counter * counter
        
    return sum

def evaluateGuess3(guess, remaining_answers_original, currentBest):
    remaining_answers = remaining_answers_original.copy()
    
    i = 0
    feedback = []
    
    feedback =  testWord(guess, remaining_answers[0])
    #print(feedback)
    sum = 0
    counter = 0
    while(len(remaining_answers) > 0):
        if i == len(remaining_answers):
            i = 0
            feedback = testWord(guess, remaining_answers[0])
            #print(feedback)
            sum += counter * counter 
            counter = 0
            if(sum > currentBest):
                return sum
                #pass
        
        if testWord(guess, remaining_answers[i]) == feedback:
            counter += 1
           # print(remaining_answers[i] + str(counter))
            remaining_answers.remove(remaining_answers[i])
        else:
            i+=1
    
    sum += counter * counter 
    return sum
    
def evaluateGuess4(guess, remaining_answers, currentBest, all_feedbacks):
    freqDict = dict.fromkeys(all_feedbacks, 0)
    for answer in remaining_answers:
        freqDict[ testWord(guess,answer)] += 1
    
    sum = 0
    for count in freqDict.values():
        sum += count * count
    
    sum -= freqDict["ggggg"] 
    return sum
    
def pickNextWord(possible_guesses, remaining_answers):
    all_feedbacks = allFeedbacks()
    bestGuess = ""
    bestScore = INFINITY
    for guess in possible_guesses:
        newScore = evaluateGuess4(guess, remaining_answers, bestScore, all_feedbacks)
        if newScore < bestScore:
            bestGuess = guess
            bestScore = newScore
            #print("new best: " + bestGuess + ", score: " + str(bestScore))
    
    
    return bestGuess



def narrowDown (guess, feedback, remaining_answers):
    newList = []
    for answer in remaining_answers:
        if testWord(guess, answer) == feedback:
            newList.append(answer)
    return newList   

#Creates a file "secondGuesses.txt" with the algorithms optimal second guess for all possible feedbacks on first guess - "roate"
def hardCodeSecondGuesses():
    f = open("secondGuessesX.txt", "w")

    for feedback in allFeedbacks():
        remaining_answers = narrowDown(FIRST_GUESS, feedback, master_answers)
        
        guess2 = pickNextWord(guesses, remaining_answers)
        print(guess2)
        
        f.write(guess2 + '\n')
    f.close()
    



FIRST_GUESS = "roate"
master_answers = wordList.getAnswerList()
guesses = wordList.getGuessesList()


f = open("sample.txt", "w")

for i in range(100):
    f.write(random.choice(master_answers) + "\n")
f.close()



l = wordList.getListFromFile("secondGuesses.txt")
SECOND_GUESSES = dict(zip(allFeedbacks(), l))


def simulate(secretWord, firstGuess, master_answers, verbose):
    answers = master_answers.copy()
    guessCount = 0 
    feedback = "bbbbb"

    manualFeedback = False

    while(feedback != "ggggg"):
        if guessCount == 0:
            guess = firstGuess
        elif guessCount == 1:
            guess = SECOND_GUESSES[feedback]
            #guess = pickNextWord(guesses,answers)
        else:
            guess = pickNextWord(guesses, answers) 
            
        
        
        guessCount += 1  
        if verbose:
            print("Guess: " + guess)
        
        if manualFeedback:
            feedback = getInput()
        else:
            feedback = testWord(guess, secretWord)
        
        if verbose:
            print("Feedback:   " + feedback)
        answers = narrowDown(guess, feedback, answers)
        #print(answers)
    
    if verbose:
        print("Guessed in " + str(guessCount) + " guesses \n")
    return guessCount



sum = 0
testSize = 100
performance = dict.fromkeys([1,2,3,4,5,6,7,8], 0)


for i in range(testSize):
    word = random.choice(master_answers)

sample = wordList.getListFromFile("sample.txt")
for i in range( len (sample)):
    word = sample[i]
    
    
    score =  simulate(word, FIRST_GUESS, master_answers, False)
    performance[score] += 1
    print(word + ": " + str(score))
    sum += score
    
plt.bar(performance.keys(), performance.values())
plt.show()
print(sum / testSize)
print(performance)

