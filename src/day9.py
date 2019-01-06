import re


class Marble:
    def __init__(self, number):
        self.left = self
        self.right = self
        self.number = number

    def get_left(self, n):
        marble = self
        for i in range(n):
            marble = marble.left
        return marble

    def get_right(self, n):
        marble = self
        for i in range(n):
            marble = marble.right
        return marble

    def insert_right(self, marble, n):
        """
        Inserts a marble between the marble n and the marble n+1 to the right
        :param marble:
        :param n:
        :return:
        """
        marble.left = self.get_right(n)
        marble.right = self.get_right(n+1)
        self.get_right(n+1).left = marble
        self.get_right(n).right = marble

    def remove_left(self, n):
        marble = self.get_left(n)
        l = self.get_left(n+1)
        r = self.get_left(n-1)
        l.right = r
        r.left = l
        return marble

    def __repr__(self):
        return "Marble {}. Left: {}. Right: {}".format(self.number, self.left.number, self.right.number)


class Game:
    def __init__(self, num_players, last_marble):
        self.last_marble = last_marble
        self.players_points = [0]*num_players
        self.current_marble: "Marble" = Marble(0)
        self.__current_player = -1
        self.__current_number = 0

    def next_marble(self):
        self.__current_number += 1
        return self.__current_number

    def next_player(self):
        self.__current_player += 1
        self.__current_player = self.__current_player %  len(self.players_points)
        return self.__current_player

    def _play_round(self):
        player = self.next_player()
        marble = Marble(self.next_marble())
        if marble.number % 23 != 0:
            self.current_marble.insert_right(marble,1)
            self.current_marble = marble
            # print("[{}]. {}".format(player+1, self.current_marble))
        else:
            self.players_points[player] += marble.number
            self.players_points[player] += self.current_marble.remove_left(7).number
            self.current_marble: "Marble" = self.current_marble.get_left(6)

    def play(self):
        for i in range(self.last_marble):
            self._play_round()
        bestscore = max(self.players_points)
        print("Winner: {} with a score of {}".format(self.players_points.index(bestscore) + 1, bestscore))
        return bestscore


def part1():
    game = Game(9, 25)
    assert game.play() == 32
    game = Game(10, 1618)
    assert game.play() == 8317
    game = Game(13, 7999)
    assert game.play() == 146373
    with open("../input/2018/day9.txt", "r") as file:
        games = file.readlines()
        for line in games:
            values = re.findall(r"(\d+)\splayers.*worth\s(\d+).*", line)[0]
            game = Game(int(values[0]), int(values[1]))
            game.play()


def part2():
    game = Game(403, 7192000)
    game.play()


part1()
part2()
