

def getAnswerList():
    return getListFromFile("wordle_answers.txt")
    
def getGuessesList():
    return getListFromFile("wordle_guesses.txt")



def getListFromFile(fileName):
    words = []
    f = open(fileName, "r")
    for line in f:
        words.append(line.strip())
    return words


