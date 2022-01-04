from teams.domain.game_rules import GameRules
from teams.domain.series import Series
from teams.domain.series_by_goals_rules import SeriesByGoalsRules
from teams.domain.series_by_wins_rules import SeriesByWinsRules
from teams.domain.series_rules import SeriesRules
from teams.domain.team import Team
from teams.services.view_models.game_view_models import GameRulesViewModel
from teams.services.view_models.playoff_view_models import SeriesByWinsRulesViewModel, SeriesByGoalsRulesViewModel
from teams.services.view_models.team_view_models import TeamViewModel


def get_vm(model):
    if isinstance(model, Team):
        return get_team_vm(model)
    elif isinstance(model, GameRules):
        return get_game_rules_vm(model)
    elif isinstance(model, SeriesByWinsRules):
        return get_series_by_wins_rules_vm(model)
    elif isinstance(model, SeriesByGoalsRules):
        return get_series_by_goals_rules_vm(model)
    elif isinstance(model, SeriesRules):
        raise NotImplementedError("Series Rules has no vm")
    elif isinstance(model, Series):
        return NotImplementedError("Series has no vm")
    else:
        return NotImplementedError("This object did not have a vm")


def get_team_vm(team):
    return TeamViewModel(team.oid, team.name, team.skill, team.active)


def get_series_by_goals_rules_vm(rules):
    return SeriesByGoalsRulesViewModel(
        rules.oid,
        rules.name,
        rules.games_to_play,
        get_game_rules_vm(rules.game_rules),
        get_game_rules_vm(rules.last_game_rules),
        rules.home_pattern
    )


def get_series_by_wins_rules_vm(rules):
    return SeriesByWinsRulesViewModel(
        rules.oid,
        rules.name,
        rules.required_wins,
        get_game_rules_vm(rules.game_rules),
        rules.home_pattern
    )


def get_game_rules_vm(rules):
    return GameRulesViewModel(rules.oid, rules.name, rules.can_tie)
