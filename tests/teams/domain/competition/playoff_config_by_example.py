from teams.domain.comp_configorator import CompetitionConfigurator
from teams.domain.competition_configuration import CompetitionConfiguration, RankingGroupConfiguration, \
    SubCompetitionConfiguration, SeriesConfiguration
from teams.domain.game import GameRules
from teams.domain.series_rules import SeriesRules, SeriesByWinsRules
from teams.domain.team import Team

toronto = Team("Toronto", 5, True)
montreal = Team("Montreal", 5, True)
ottawa = Team("Ottawa", 5, True)
quebec_city = Team("Quebec City", 5, True)
calgary = Team("Calgary", 5, True)
edmonton = Team("Edmonton", 5, True)
vancouver = Team("Vancouver", 5, True)
winnipeg = Team("Winnipeg", 5, True)
victoria = Team("Victoria", 5, True)
saskatoon = Team("Saskatoon", 5, True)
hamilton = Team("Hamilton", 5, True)
halifax = Team("Halifax", 5, True)

playoff_game_rules = GameRules("Playoff Rules", False)
series_rules = SeriesByWinsRules("Best of 7", 4, playoff_game_rules, [0, 0, 1, 1, 0, 1, 0])

competition_config = CompetitionConfiguration("Playoff Test", [], 1, 1, None)

playoff_config = SubCompetitionConfiguration("Playoff", competition_config, 1, SubCompetitionConfiguration.PLAYOFF_TYPE, 1, None)
competition_config.sub_competitions.append(playoff_config)

# seeding group
league = RankingGroupConfiguration("League", playoff_config, None, 1, 1, None)

# playoff groups
r1_winners = RankingGroupConfiguration("R1 Winners", playoff_config, None, 1, 1, None)
r2_winners = RankingGroupConfiguration("R2 Winners", playoff_config, None, 1, 1, None)
champion = RankingGroupConfiguration("Champion", playoff_config, None, 1, 1, None)
runner_up = RankingGroupConfiguration("Runner Up", playoff_config, None, 1, 1, None)

group_configs = [league, r1_winners, r2_winners, champion, runner_up]

# round 1
r1s1 = SeriesConfiguration("R1S1", 1, playoff_config, league, 1, league, 8, series_rules, r1_winners, league, None, None, 1, None)
r1s2 = SeriesConfiguration("R1S2", 1, playoff_config, league, 2, league, 7, series_rules, r1_winners, league, None, None, 1, None)
r1s3 = SeriesConfiguration("R1S3", 1, playoff_config, league, 3, league, 6, series_rules, r1_winners, league, None, None, 1, None)
r1s4 = SeriesConfiguration("R1S4", 1, playoff_config, league, 4, league, 5, series_rules, r1_winners, league, None, None, 1, None)
# round 2
r2s1 = SeriesConfiguration("R2S1", 2, playoff_config, r1_winners, 1, r1_winners, 4, series_rules, r2_winners, league, None, None, 1, None)
r2s2 = SeriesConfiguration("R2S2", 2, playoff_config, r1_winners, 2, r1_winners, 3, series_rules, r2_winners, league, None, None, 1, None)
# round 3
r3s1 = SeriesConfiguration("R3S1", 3, playoff_config, r2_winners, 1, r2_winners, 4, series_rules, champion, league, runner_up, league, 1, None)

series_configs = [r1s1, r1s2, r1s3, r1s4, r2s2, r2s1, r3s1]

current_groups = []
competition = CompetitionConfigurator.create_competition(competition_config, 1)
playoff = CompetitionConfigurator.create_sub_competition(playoff_config, competition)
CompetitionConfigurator.create_competition_group(league, current_groups, competition)

for series_config in series_configs:
    CompetitionConfigurator.process_series_configuration(series_config, current_groups, playoff)

