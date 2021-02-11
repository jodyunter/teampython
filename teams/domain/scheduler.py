# use this as a basis to create a game
class ScheduledGame:

    def __init__(self, home_id, away_id, rules_id, year, day):
        self.home_id = home_id
        self.away_id = away_id
        self.rules_id = rules_id
        self.year = year
        self.day = day

    def does_team_play_in_game(self, other_game):
        home_plays = other_game.home_id == self.home_id or other_game.home_id == self.away_id
        away_plays = other_game.away_id == self.home_id or other_game.away_id == self.away_id

        return home_plays or away_plays


class Scheduler:
    matrix = []
    num_list = []
    odd = False
    anchor = -5
    pairs = 0
    total_teams = -1

    def schedule_games(self, team_ids, rules_id, year, starting_day, home_and_away):
        self.total_teams = len(team_ids)
        result = []
        self.setup()
        current_day = starting_day
        if self.total_teams % 2 == 0:
            iterations = self.total_teams - 1
        else:
            iterations = self.total_teams

        for x in range(iterations):
            self.populate_matrix()
            # create games
            for n in range(len(self.matrix)):
                home_num = self.matrix[n][0]
                away_num = self.matrix[n][1]

                if not home_num == -1:
                    result.append(ScheduledGame(team_ids[home_num],
                                                team_ids[away_num],
                                                rules_id,
                                                year, current_day))

            # increment day
            current_day += 1

        if home_and_away:
            days_to_add = current_day - starting_day
            new_games = []

            for game in result:
                new_games.append(ScheduledGame(game.away_id, game.home_id, game.rules_id,
                                               game.year, game.day + days_to_add))

            result.extend(new_games)

            current_day += days_to_add

        return result

    def populate_matrix(self):
        self.matrix = []

        for x in range(self.pairs):
            self.matrix.append([0, 0])
            if x == 0:
                self.matrix[0][0] = self.anchor
                self.matrix[0][1] = self.num_list[0]
            else:
                self.matrix[x][0] = self.num_list[x]
                self.matrix[x][1] = self.num_list[len(self.num_list) - x]

        self.num_list = [self.get_next_value(x, self.total_teams - 1, self.anchor + 1) for x in self.num_list]

    @staticmethod
    def get_next_value(current, max_value, min_value):
        current += 1
        if current > max_value:
            current = min_value

        return current

    def setup(self):
        if self.total_teams % 2 == 1:
            self.pairs = int((self.total_teams + 1) / 2)
            self.anchor = -1
            self.odd = True
        else:
            self.pairs = int(self.total_teams / 2)
            self.anchor = 0
            self.odd = False

        self.num_list = list(range(self.anchor + 1, self.total_teams))

    @staticmethod
    def does_team_play_in_games_list(games, team_id):
        for g in games:
            if g.home_team.oid == team_id or g.away_team.oid == team_id:
                return True

        return False

    @staticmethod
    def does_any_team_play_in_other_list(new_games, games):
        for n in new_games:
            for g in games:
                if n.home_team.oid in [g.home_team.oid, g.away_team.oid] or n.away_team.oid in [g.home_team.oid, g.away_team.oid]:
                    return True

        return False

    @staticmethod
    def set_day_for_new_series_game(new_game, current_games, days_between=0):
        last_day = max(g.day for g in current_games)

        new_game_day = last_day + 1 + days_between

        new_game.day = new_game_day


