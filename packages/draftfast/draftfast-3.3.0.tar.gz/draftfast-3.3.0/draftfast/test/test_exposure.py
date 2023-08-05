import os
from nose import tools as ntools
from draftfast.optimize import run_multi
from draftfast import rules
from draftfast.csv_parse import salary_download

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-nfl-salaries.csv'.format(CURRENT_DIR)
fd_nfl_salary_file = '{}/data/fd-nfl-salaries.csv'.format(CURRENT_DIR)
projection_file = '{}/data/dk-nfl-projections.csv'.format(CURRENT_DIR)


def test_deterministic_exposure_limits():
    iterations = 2
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    rosters, exposure_diffs = run_multi(
        iterations=2,
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
        exposure_bounds=[
            {'name': 'Andrew Luck', 'min': 0.5, 'max': 0.7},
            {'name': 'Alshon Jeffery', 'min': 1, 'max': 1},
        ],
    )
    ntools.assert_equal(len(rosters), iterations)
    ntools.assert_equal(len(exposure_diffs), 0)

    players = [p.name for p in rosters[0].players]
    ntools.assert_true('Andrew Luck' in players)
    ntools.assert_true('Alshon Jeffery' in players)

    players = [p.name for p in rosters[1].players]
    ntools.assert_true('Andrew Luck' not in players)
    ntools.assert_true('Alshon Jeffery' in players)


def test_random_exposure_limits():
    iterations = 10
    players = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        projection_file_location=projection_file,
        game=rules.DRAFT_KINGS,
    )
    rosters, exposure_diffs = run_multi(
        iterations=iterations,
        exposure_random_seed=42,
        rule_set=rules.DK_NFL_RULE_SET,
        player_pool=players,
    )
    ntools.assert_equal(len(rosters), iterations)
    ntools.assert_equal(len(exposure_diffs), 0)
