import sys
from MaxConnect4Game import maxConnect4Game
from evaluation import Evaluation

def oneMoveGame(currentGame):
    if currentGame.pieceCount == 42:
        print ('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)
    currentGame.aiPlay()
    print ('Game state after move:')
    currentGame.printGameBoard()
    currentGame.player1Score = currentGame.evaluation.getScore(currentGame.gameBoard, 1)
    currentGame.player2Score = currentGame.evaluation.getScore(currentGame.gameBoard, 2)
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()

def interactiveGame(currentGame):
    if currentGame.pieceCount == 42:
        print ('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)
    currentGame.depth = int(sys.argv[4])
    computer_txt = open("computer.txt", "w")
    human_txt = open("human.txt", "w")
    if sys.argv[3] == "computer-next":
        while (True):
            currentGame.currentTurn = 1
            currentGame.aiPlay() 
            print ('Game state after computer move:')
            currentGame.printGameBoard()
            currentGame.writeGameBoardToFile(computer_txt, 1)
            currentGame.player1Score = currentGame.evaluation.getScore(currentGame.gameBoard, 1)
            currentGame.player2Score = currentGame.evaluation.getScore(currentGame.gameBoard, 2)
            print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            while currentGame.pieceCount != 42:
                col = input("Enter column number from 1 to 7 or q to quit: ")
                if col != "q":
                    currentGame.currentTurn = 2
                    if currentGame.playPiece(int(col)-1):
                        print ('Game state afterhuman  move:')
                        currentGame.printGameBoard()
                        currentGame.writeGameBoardToFile(human_txt, 2)
                        currentGame.player1Score = currentGame.evaluation.getScore(currentGame.gameBoard, 1)
                        currentGame.player2Score = currentGame.evaluation.getScore(currentGame.gameBoard, 2)
                        print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
                        break
                else:
                    exit()
            if currentGame.pieceCount == 42:
                exit()
    elif sys.argv[3] == "human-next":
        while (True):
            while currentGame.pieceCount != 42:
                col = input("Enter column number from 1 to 7 or q to quit: ")
                if col != "q":
                    currentGame.currentTurn = 1
                    if currentGame.playPiece(int(col)-1):
                        print ('Game state after human move:')
                        currentGame.printGameBoard()
                        currentGame.writeGameBoardToFile(human_txt, 1)
                        currentGame.player1Score = currentGame.evaluation.getScore(currentGame.gameBoard, 1)
                        currentGame.player2Score = currentGame.evaluation.getScore(currentGame.gameBoard, 2)
                        print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
                        break
                else:
                    exit()
            if currentGame.pieceCount == 42:
                exit()
            currentGame.currentTurn = 2
            currentGame.aiPlay()
            print ('Game state after computer move:')
            currentGame.printGameBoard()
            currentGame.writeGameBoardToFile(computer_txt, 2)
            currentGame.player1Score = currentGame.evaluation.getScore(currentGame.gameBoard, 1)
            currentGame.player2Score = currentGame.evaluation.getScore(currentGame.gameBoard, 2)
            print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    computer_txt.close()
    human_txt.close()

def main(argv):
    if len(argv) != 5:
        print ('Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)
    game_mode, inFile = argv[1:3]
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)
    currentGame = maxConnect4Game(Evaluation())
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")
    file_lines = currentGame.gameFile.readlines()
    if file_lines:
        currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
        currentGame.currentTurn = int(file_lines[-1][0])
    else:
        currentGame.gameBoard = [[0 for _ in range(7)] for _ in range(6)]
        currentGame.currentTurn = 1
    currentGame.gameFile.close()
    print ('\nMaxConnect-4 game\n')
    print ('Game state before move:')
    currentGame.printGameBoard()
    currentGame.checkPieceCount()
    currentGame.player1Score = currentGame.evaluation.getScore(currentGame.gameBoard, 1)
    currentGame.player2Score = currentGame.evaluation.getScore(currentGame.gameBoard, 2)
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    if game_mode == 'interactive':
        interactiveGame(currentGame)
    else: 
        game_mode == 'one-move'
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
            currentGame.depth = int(argv[4])
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame)

if __name__ == '__main__':
    main(sys.argv)



