from audioop import tomono
from selenium import webdriver
from selenium.webdriver.common import by



options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome('c:\chromedriver.exe',options= options)


driver.get("https://lichess.org/analysis/fromPosition/r1bqkbnr/1ppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR_w_KQkq_-_0_1#2")

while True:
    input("Click enter to get last moves")
    boardSizeStr = driver.find_element_by_tag_name("cg-container").get_attribute("style").split(';')[0].split(' ')[1]
    boardSize = int(boardSizeStr[:len(boardSizeStr)-2])
    squareSize = boardSize / 8

    fromMove = ''
    toMove = ''

    for peace in driver.find_elements_by_tag_name('square'):
        
        positionStr = peace.get_attribute("style")
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
            print('toMove: ' + toMove)
        else:
            fromMove = letter + str(yPos)
            print('fromMove: ' + fromMove)
        

        