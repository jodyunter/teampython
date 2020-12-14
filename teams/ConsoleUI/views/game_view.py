class GameView:
    @staticmethod
    def get_basic_view(game_view_model):
        return game_view_model.home_name + " " + str(game_view_model.home_score) + " - " + \
               str(game_view_model.away_score) + " " + game_view_model.away_name
    @staticmethod
    def get_view_with_day(game_view_model):
        return str(game_view_model.day) + " " + game_view_model.home_name + " " + str(game_view_model.home_score) + " - " + \
               str(game_view_model.away_score) + " " + game_view_model.away_name
