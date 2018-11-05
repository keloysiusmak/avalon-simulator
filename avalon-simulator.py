import random

class GameSchema:
    def isBad(self, playerRole):
        return playerRole == 3 or playerRole == 5
    def isGood(self, playerRole):
        return not self.isBad(playerRole)
    def isMerlin(self, playerRole):
        return playerRole == 2

class Player:
    def __init__(self, role, playerNumber, players):
        self.role = role
        self.playerNumber = playerNumber
        self.playersGoodness = []
        i = 1
        while i <= players:
            if (i != playerNumber):
                self.playersGoodness.append(0.5)
            else:
                if GameSchema().isGood(self.role):
                    self.playersGoodness.append(1)
                else:
                    self.playersGoodness.append(0)
            i = i + 1

    def setGoodness(self, playerNumber, goodness):
        self.playersGoodness[playerNumber - 1] = goodness

    def pick(self, playersRequired):
        selectedPlayers = []
        if GameSchema().isBad(self.role):
            selectedPlayers.append(self.playerNumber)
        while len(selectedPlayers) < playersRequired:
            playerCount = 0
            for i in self.playersGoodness:
                playerCount = playerCount + 1
                if random.random() <= i:
                    selectedPlayers.append(playerCount)
                if len(selectedPlayers) == playersRequired:
                    break
            if len(selectedPlayers) < playersRequired:
                if GameSchema().isBad(self.role):
                    selectedPlayers = [self.playerNumber]
                else:
                    selectedPlayers = []


        return selectedPlayers

    def executeMission(self):
        if self.role == 3 or self.role == 5:
            return False
        else:
            return True

class Round:
    result = 0
    numberOfMissionPlayers = {5: [2,3,2,3,3]}
    def __init__(self, players, startingPlayer, roundNumber):
        self.thisPlayer = players[startingPlayer - 1]
        self.players = players
        self.roundNumber = roundNumber
        self.startingPlayer = startingPlayer
    def start(self):
        print "Round " + str(self.roundNumber) + "--"
        print "Player " + str(self.startingPlayer) + " makes the pick."
        playersRequired = self.numberOfMissionPlayers[len(self.players)][self.roundNumber - 1]
        player = self.players[self.startingPlayer - 1]
        print player.playersGoodness
        selectedPlayers = player.pick(playersRequired)
        missionState = True
        for player in selectedPlayers:
            playerState = self.players[player - 1].executeMission()
            missionState = missionState and playerState
            print "Player " + str(player) + ": " + str(playerState)
        return missionState

class Game:
    ## Roles
    # 1 : Perceival
    # 2 : Merlin
    # 3 : Morgana
    # 4 : Minion of Arthur (Good)
    # 5 : Minion of Mordred (Evil)
    roleNames = ["Perceival", "Merlin", "Morgana", "Minion of Arthur (Good)", "Minion of Mordred (Evil)"]
    roles = {5: [1,2,3,4,5]}
    players = []
    goodPlayers = []
    badPlayers = []
    def __init__(self, players):
        i = 1
        gameRoles = []
        while i <= players:
            gameRoles = self.roles[players]
            assignedRole = random.randint(1, len(gameRoles))
            newPlayer = Player(gameRoles[assignedRole - 1], i, players)
            self.players.append(newPlayer)
            if GameSchema().isGood(gameRoles[assignedRole - 1]):
                if GameSchema().isMerlin(gameRoles[assignedRole - 1]):
                    self.merlin = i
                self.goodPlayers.append(i)
            else:
                self.badPlayers.append(i)
            print "Player " + str(i) + " has a role of " + self.roleNames[gameRoles[assignedRole - 1] - 1]
            del gameRoles[assignedRole - 1]
            i = i + 1
        print self.badPlayers
        print self.goodPlayers
        for badPlayer in self.badPlayers:
            for otherBadPlayer in self.badPlayers:
                self.players[badPlayer - 1].setGoodness(otherBadPlayer, 0)
            self.players[self.merlin - 1].setGoodness(badPlayer, 0)
        for goodPlayer in self.goodPlayers:
            for badPlayer in self.badPlayers:
                self.players[badPlayer - 1].setGoodness(goodPlayer, 1)
            self.players[self.merlin - 1].setGoodness(goodPlayer, 1)


    def startGame(self):
        goodScore = 0
        badScore = 0
        startingPlayer = random.randint(1, len(self.players))
        while goodScore < 3 and badScore < 3:
            newRound = Round(self.players, startingPlayer, (goodScore + badScore + 1))
            if newRound.start() == False:
                badScore = badScore + 1
            else:
                goodScore = goodScore + 1
            startingPlayer = startingPlayer % len(self.players) + 1
        if goodScore == 3:
            print "Minions of Arthur Wins!"
        else:
            print "Minions of Mordred Wins!"


#numberOfPlayers = input("Number of Players: ")
numberOfPlayers = 5
newGame = Game(numberOfPlayers)
newGame.startGame()
