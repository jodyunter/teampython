class RecordView:
    @staticmethod
    def format_string():
        return "{0:<15} {1:3} {2:3} {3:3} {4:3} {5:4} {6:4} {7:4}"

    @staticmethod
    def get_table_header():
        return str.format(RecordView.format_string(), "Name", "W", "L", "T", "Pts", "GP", "GF", "GA")

    @staticmethod
    def get_table_row(model):
        return str.format(RecordView.format_string(),
                          model.team_name,
                          model.wins,
                          model.loses,
                          model.ties,
                          model.points,
                          model.games,
                          model.goals_for,
                          model.goals_against)

