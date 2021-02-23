class GameView:
    @staticmethod
    def get_basic_view(game_view_model):
        return game_view_model.home_name + " " + str(game_view_model.home_score) + " - " + \
               str(game_view_model.away_score) + " " + game_view_model.away_name

    @staticmethod
    def get_view_with_day(game_view_model):
        return str(game_view_model.day) + " " + game_view_model.home_name + " " + str(game_view_model.home_score) + " - " + \
               str(game_view_model.away_score) + " " + game_view_model.away_name


class GameDayView:
    @staticmethod
    def get_view(game_day_view_model):
        result = str(game_day_view_model.day)

        for g in game_day_view_model.games:
            result = result + "\n" + GameView.get_basic_view(g)

        return result
