class SeriesView:
    @staticmethod
    def get_basic_series_view(series_view_model):
        return f"{series_view_model.name} {series_view_model.team1.name:>10} : {series_view_model.team1_wins:>3} - {series_view_model.team2_wins:<3} : {series_view_model.team2.name:<10}"


