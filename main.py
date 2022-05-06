from audioop import tomono
import imp
from telnetlib import EC
from selenium import webdriver
from stockfish import Stockfish
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


stockfish = Stockfish(r'C:\stockfish.exe', parameters={"Threads" : 7, "Ponder" : True, "Minimum Thinking Time": 20, "Skill Level": 20, "Hash":16, "Contempt": 0, "Slow Mover": 84})
stockfish.set_depth(16)

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome('c:\chromedriver.exe',options= options)


driver.get("https://lichess.org/")


def getLastMoveSet():
    boardSizeStr = driver.find_element_by_tag_name("cg-container").get_attribute("style").split(';')[0].split(' ')[1]
    boardSize = int(boardSizeStr[:len(boardSizeStr)-2])
    squareSize = boardSize / 8

    fromMove = ''
    toMove = ''

    reversedSet = False

    for piece in driver.find_elements_by_tag_name('piece'):
        if driver.find_elements_by_tag_name('square')[1].get_attribute("style") == piece.get_attribute("style"):
            reversedSet = True

    for piece in driver.find_elements_by_tag_name('square'):
        
        positionStr = piece.get_attribute("style")
        # transform: translate(0px, 95px);
        xPosStr = positionStr.split('(')[1].split(',')[0]
        xPos = int(xPosStr[:len(xPosStr)-2])
        letter = 'a'
        if xPos is not 0:
            xPos = xPos / squareSize
        letter = chr(ord(letter)+int(xPos))
        yPosStr = positionStr.split('(')[1].split(',')[1].split(' ')[1]
        yPos = int(yPosStr[:len(yPosStr)-4])
        if yPos is 0:
            yPos = 8
        else:
            yPos =  int((boardSize - yPos) / squareSize)


        if toMove is '':
            toMove = letter + str(yPos)
        else:
            fromMove = letter + str(yPos)
    if reversedSet:
        return toMove + fromMove
    return fromMove + toMove



lastMoveSet = ""
gameOver = False
wait = WebDriverWait(driver, 150)
gameMoveSet = []
while True:
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'rclock-turn__text')))
    turnElement = driver.find_element(By.CLASS_NAME, 'rclock-turn__text')
    wait.until(ec.invisibility_of_element(turnElement))
    lastMove = getLastMoveSet()
    print(lastMove)
    gameMoveSet.append(lastMove)
    stockfish.set_position(gameMoveSet)
    print("Best next: " + stockfish.get_best_move())