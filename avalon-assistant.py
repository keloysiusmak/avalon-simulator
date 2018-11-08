class Player:
    def __init__(self, playerNumber, goodness):
        self.playerNumber = playerNumber
        self.goodness = goodness
class GameSchema:
    missionDetails = {5: [2,3,2,3,3], 6: [2,3,4,3,4]}
    missionWeight = [0.01, 0.02, 0.04, 0.08, 0.16]
    missionNonVotedWeight = [0.001, 0.002, 0.004, 0.008, 0.016]
    def __init__(self, numberOfPlayers):
        self.missions = self.missionDetails[numberOfPlayers]


class Game:
    def __init__(self, numberOfPlayers):
        self.numberOfPlayers = numberOfPlayers
        self.players = []
        me = Player(1, 1)
        self.players.append(me)
        i = 2
        while i <= numberOfPlayers:
            newPlayer = Player(i, 0.5)
            self.players.append(newPlayer)
            i = i + 1

    def generateMatrix(self, remaining, players):
        newPlayers = players[0: len(players)]
        if (remaining == 0):
            return [[]]
        else:
            if len(newPlayers) == 0:
                return [[]]
            else:
                interestedPlayer = newPlayers[0]
                del newPlayers[0]
                matrix1 = self.generateMatrix(remaining - 1, newPlayers)
                updatedMatrix = []
                for m in matrix1:
                    m.append(interestedPlayer.playerNumber)
                    updatedMatrix.append(m)
                matrix2 = self.generateMatrix(remaining, newPlayers)
                for m in matrix2:
                    if (len(m) == remaining):
                        updatedMatrix.append(m)
                return updatedMatrix

    def start(self):
        matrix = self.generateMatrix(3, self.players)
        newMatrix = []
        for m in matrix:
            if 1 in m:
                newMatrix.append(m)
        matrix = newMatrix
        goodScore = 0
        badScore = 0
        gameSchema = GameSchema(self.numberOfPlayers)
        round = 1
        gameState = []
        while goodScore < 3 and badScore < 3:
            print "\nRound " + str(round) + " Input"
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
                print "\n-- Voting Round " + str(votingRound) + " --"
                picker = input("Who Made The Pick: ")
                votingRoundDetails.append(picker)
                votingRoundPlayers = []
                i = 1
                while i <= numberOfPlayersRequired:
                    playerThatWent = input("Who was voted on the mission: ")
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
                    print "-- Voting Round " + str(votingRound) + " Failed --"
                else:
                    print "-- Voting Round " + str(votingRound) + " Succeeded --"
                votingRound = votingRound + 1
                roundVoting.append(votingRoundDetails)
            result = input("What is the mission status (0 for Fail, 1 for Success): ")
            noVotes = roundVoting[len(roundVoting) - 1][2][0]
            yesVotes = roundVoting[len(roundVoting) - 1][2][1]
            if result == 1:
                for i in yesVotes:
                    multiplier = 1
                    if (i in roundVoting[len(roundVoting) - 1][1]):
                        multiplier = 1.5
                    self.players[i - 1].goodness = self.players[i - 1].goodness + gameSchema.missionWeight[round - 1] * multiplier
                for i in noVotes:
                    multiplier = 1
                    if (i in roundVoting[len(roundVoting) - 1][1]):
                        multiplier = -1
                    self.players[i - 1].goodness = self.players[i - 1].goodness - gameSchema.missionWeight[round - 1] * multiplier
                i = 1
                while i <= self.numberOfPlayers:
                    if self.players[i - 1].goodness > 1:
                        self.players[i - 1].goodness = 1
                    if self.players[i - 1].goodness < 0:
                        self.players[i - 1].goodness = 0
                    i = i + 1
                goodScore = goodScore + 1
            else:
                for i in yesVotes:
                    multiplier = 1
                    if (i in roundVoting[len(roundVoting) - 1][1]):
                        multiplier = 1.5
                    self.players[i - 1].goodness = self.players[i - 1].goodness - gameSchema.missionWeight[round - 1] * multiplier
                for i in noVotes:
                    multiplier = 1
                    if (i in roundVoting[len(roundVoting) - 1][1]):
                        multiplier = -1
                    self.players[i - 1].goodness = self.players[i - 1].goodness + gameSchema.missionWeight[round - 1] * multiplier
                i = 1
                while i <= self.numberOfPlayers:
                    if self.players[i - 1].goodness > 1:
                        self.players[i - 1].goodness = 1
                    if self.players[i - 1].goodness < 0:
                        self.players[i - 1].goodness = 0
                    i = i + 1
                badScore = badScore + 1
                newMatrix = []
                for m in matrix:
                    isItem = True
                    for n in votingRoundDetails[1]:
                        isItem = isItem and n in m
                    if not isItem:
                        newMatrix.append(m)
                matrix = newMatrix
            round = round + 1
            gameState.append([roundVoting, result])
            print "\n-- State of the Game --"
            self.players[0].goodness = 1
            for player in self.players:
                count = 0
                for m in matrix:
                    if player.playerNumber in m:
                        count = count + 1
                prob = (count * 100.00 / len(matrix)) * (player.goodness / 0.5)
                if prob > 100.0:
                    prob = 100.0
                player.currentProb = prob
                player.variableScore = 0.0
            r = 1
            for currentRound in gameState:
                print "==Round " + str(r) + "=="
                p = 1
                for pick in currentRound[0]:
                    print "--Pick " + str(p) + "--"
                    print "Players Picked : " + str(pick[1])
                    pickGoodProb = 1.0
                    for i in pick[1]:
                        pickGoodProb = pickGoodProb * (self.players[i - 1].currentProb / 100.0)
                    print "Good Probability : " + str(pickGoodProb * 100) + "%"
                    expectedProb = ((2.0 / (len(self.players) - 1)) ** len(pick[1])) * 100
                    if (p != len(currentRound)):
                        calc = ( pickGoodProb * 100 / expectedProb - 1 ) * gameSchema.missionNonVotedWeight[r - 1]
                        for p in pick[2][1]:
                            self.players[p - 1].variableScore = self.players[p - 1].variableScore + calc
                        for p in pick[2][0]:
                            self.players[p - 1].variableScore = self.players[p - 1].variableScore - calc
                    print "Picked By : " + str(pick[0])
                    print "Voted For : " + str(pick[2][1])
                    print "Voted Against : " + str(pick[2][0])
                    if (len(pick[2][0]) > len(pick[2][1])):
                        print "Voting Round Failed"
                    else:
                        print "Voting Round Succeeded"
                    p = p + 1
                if currentRound[1] == 1:
                    print "\nResult: Mission Succeeded\n"
                else:
                    print "\nResult: Mission Failed\n"
                r = r + 1
            print "Score : (" + str(goodScore) + "-" + str(badScore) + ")\n"
            for player in self.players:
                playerGoodness = player.goodness + player.variableScore
                reverseProb = player.currentProb / (player.goodness / 0.5)
                if (player.playerNumber == 1):
                    playerGoodness = 1
                    reverseProb = 100
                prob = reverseProb * ((playerGoodness / 0.5))
                if prob > 100.0:
                    prob = 100.0
                if prob < 0.0:
                    prob = 0.0
                if playerGoodness > 1:
                    playerGoodness = 1
                if playerGoodness < 0:
                    playerGoodness = 0
                print "Player " + str(player.playerNumber) + "'s Probability of Being Good : " + str(prob) + "% | Score : " + str(playerGoodness)
        if goodScore == 3:
            print "Minions of Arthur Wins!"
        else:
            print "Minions of Mordred Wins!"

numberOfPlayers = input("How many players are there: ")
newGame = Game(numberOfPlayers)
newGame.start()
