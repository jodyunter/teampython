class GameView:
    @staticmethod
    def get_view(game_view_model):
        return game_view_model.home_name + " " + str(game_view_model.home_score) + " - " + \
               str(game_view_model.away_score) + " " + game_view_model.away_name
