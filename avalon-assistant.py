class Player:
    def __init__(self, playerNumber, goodness):
        self.playerNumber = playerNumber
        self.goodness = goodness
class GameSchema:
    missionDetails = {5: [2,3,2,3,3]}
    def __init__(self, numberOfPlayers):
        self.missions = self.missionDetails[numberOfPlayers]
class Game:
    def __init__(self, numberOfPlayers):
        self.numberOfPlayers = numberOfPlayers
        self.players = []
        i = 1
        while i < numberOfPlayers:
            newPlayer = Player(i, 0.5)
            self.players.append(newPlayer)
            i = i + 1
        me = Player(numberOfPlayers, 1)
        self.players.append(me)
    def start(self):
        goodScore = 0
        badScore = 0
        gameSchema = GameSchema(self.numberOfPlayers)
        round = 1
        gameState = []
        while goodScore < 3 and badScore < 3:
            print "\nRound " + str(round)
            numberOfPlayersRequired =  gameSchema.missions[round - 1]
            i = 1
            roundPlayers = []
            roundVoting = []
            votesFor = 0
            votesAgainst = 0
            votingRound = 1
            while (votesFor <= votesAgainst):
                votesFor = 0
                votesAgainst = 0
                votingRoundDetails = []
                print "\nVoting Round " + str(votingRound)
                picker = input("Who Made The Pick: ")
                votingRoundDetails.append(picker)
                votingRoundPlayers = []
                i = 1
                while i <= numberOfPlayersRequired:
                    playerThatWent = input("Who was voted on the mission?\n")
                    votingRoundPlayers.append(playerThatWent)
                    i = i + 1
                votingRoundDetails.append(votingRoundPlayers)
                votersAgainst = []
                votersFor = []
                for player in self.players:
                    vote = input("What did Player " + str(player.playerNumber) + " vote? (0 for No-Go, 1 for Go): ")
                    if vote == 0:
                        votersAgainst.append(player.playerNumber)
                        votesAgainst = votesAgainst + 1
                    else:
                        votersFor.append(player.playerNumber)
                        votesFor = votesFor + 1
                votingRoundDetails.append([votersAgainst, votersFor])
                if (votesFor <= votesAgainst):
                    print "Voting Round " + str(votingRound) + " Failed"
                else:
                    print "Voting Round " + str(votingRound) + " Succeeded"
                votingRound = votingRound + 1
                roundVoting.append(votingRoundDetails)
            result = input("What is the mission status? (0 for Fail, 1 for Success)\n")
            if result == 1:
                goodScore = goodScore + 1
            else:
                badScore = badScore + 1
            round = round + 1
            gameState.append([roundVoting, result])
            print "\n-- State of the Game --"
            r = 1
            for currentRound in gameState:
                print "Round " + str(r) + "\n"
                p = 1
                for pick in currentRound[0]:
                    print "\nPick " + str(p) + "--"
                    print "Players Picked : " + str(pick[1])
                    print "Picked By : " + str(pick[0])
                    print "Voted For : " + str(pick[2][1])
                    print "Voted Against : " + str(pick[2][0])
                    if (len(pick[2][0]) > len(pick[2][1])):
                        print "Voting Round Failed"
                    else:
                        print "Voting Round Succeeded"
                    p = p + 1
                if currentRound[1] == 1:
                    print "\nResult: Mission Succeeded (" + str(goodScore) + "-" + str(badScore) + ")\n"
                else:
                    print "\nResult: Mission Failed (" + str(goodScore) + "-" + str(badScore) + ")\n"
                r = r + 1
        if goodScore == 3:
            print "Minions of Arthur Wins!"
        else:
            print "Minions of Mordred Wins!"

newGame = Game(5)
newGame.start()
