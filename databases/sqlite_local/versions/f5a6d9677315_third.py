"""third

Revision ID: f5a6d9677315
Revises: d92f3ff5fdd7
Create Date: 2021-12-29 08:53:24.753442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5a6d9677315'
down_revision = 'd92f3ff5fdd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('competitiongroup')
    op.drop_table('gamedata')
    op.drop_table('seriesrules')
    op.drop_table('games')
    op.drop_table('gamerules')
    op.drop_table('records')
    op.drop_table('series')
    op.drop_table('competitions')
    op.drop_table('subcompetitions')
    op.drop_table('teams')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teams',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('skill', sa.INTEGER(), nullable=True),
    sa.Column('active', sa.BOOLEAN(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('oid'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subcompetitions',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('sub_competition_type', sa.VARCHAR(), nullable=True),
    sa.Column('competition_id', sa.VARCHAR(), nullable=True),
    sa.Column('order', sa.INTEGER(), nullable=True),
    sa.Column('setup', sa.BOOLEAN(), nullable=True),
    sa.Column('started', sa.BOOLEAN(), nullable=True),
    sa.Column('finished', sa.BOOLEAN(), nullable=True),
    sa.Column('post_processed', sa.BOOLEAN(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('competitions',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('current_round', sa.INTEGER(), nullable=True),
    sa.Column('setup', sa.BOOLEAN(), nullable=True),
    sa.Column('started', sa.BOOLEAN(), nullable=True),
    sa.Column('finished', sa.BOOLEAN(), nullable=True),
    sa.Column('post_processed', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('series',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('sub_competition_id', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('series_round', sa.INTEGER(), nullable=True),
    sa.Column('home_team_id', sa.VARCHAR(), nullable=True),
    sa.Column('away_team_id', sa.VARCHAR(), nullable=True),
    sa.Column('series_type', sa.VARCHAR(), nullable=True),
    sa.Column('series_rules_id', sa.VARCHAR(), nullable=True),
    sa.Column('home_team_from_group_id', sa.VARCHAR(), nullable=True),
    sa.Column('home_team_value', sa.INTEGER(), nullable=True),
    sa.Column('away_team_from_group_id', sa.VARCHAR(), nullable=True),
    sa.Column('away_team_value', sa.INTEGER(), nullable=True),
    sa.Column('winner_to_group_id', sa.VARCHAR(), nullable=True),
    sa.Column('loser_to_group_id', sa.VARCHAR(), nullable=True),
    sa.Column('setup', sa.BOOLEAN(), nullable=True),
    sa.Column('post_processed', sa.BOOLEAN(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['away_team_from_group_id'], ['competitiongroup.oid'], ),
    sa.ForeignKeyConstraint(['away_team_id'], ['teams.oid'], ),
    sa.ForeignKeyConstraint(['home_team_from_group_id'], ['competitiongroup.oid'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['teams.oid'], ),
    sa.ForeignKeyConstraint(['loser_to_group_id'], ['competitiongroup.oid'], ),
    sa.ForeignKeyConstraint(['series_rules_id'], ['seriesrules.oid'], ),
    sa.ForeignKeyConstraint(['sub_competition_id'], ['subcompetitions.oid'], ),
    sa.ForeignKeyConstraint(['winner_to_group_id'], ['competitiongroup.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('records',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('rank', sa.INTEGER(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('wins', sa.INTEGER(), nullable=True),
    sa.Column('loses', sa.INTEGER(), nullable=True),
    sa.Column('ties', sa.INTEGER(), nullable=True),
    sa.Column('goals_for', sa.INTEGER(), nullable=True),
    sa.Column('goals_against', sa.INTEGER(), nullable=True),
    sa.Column('skill', sa.INTEGER(), nullable=True),
    sa.Column('team_id', sa.VARCHAR(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('gamerules',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('can_tie', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('oid'),
    sa.UniqueConstraint('name')
    )
    op.create_table('games',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('day', sa.INTEGER(), nullable=True),
    sa.Column('home_score', sa.INTEGER(), nullable=True),
    sa.Column('away_score', sa.INTEGER(), nullable=True),
    sa.Column('complete', sa.BOOLEAN(), nullable=True),
    sa.Column('processed', sa.BOOLEAN(), nullable=True),
    sa.Column('home_team_id', sa.VARCHAR(), nullable=True),
    sa.Column('away_team_id', sa.VARCHAR(), nullable=True),
    sa.Column('rules_id', sa.VARCHAR(), nullable=True),
    sa.Column('sub_competition_id', sa.VARCHAR(), nullable=True),
    sa.Column('competition_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['away_team_id'], ['teams.oid'], ),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.oid'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['teams.oid'], ),
    sa.ForeignKeyConstraint(['rules_id'], ['gamerules.oid'], ),
    sa.ForeignKeyConstraint(['sub_competition_id'], ['subcompetitions.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('seriesrules',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('game_rules_id', sa.VARCHAR(), nullable=True),
    sa.Column('series_type', sa.VARCHAR(), nullable=True),
    sa.Column('home_pattern', sa.VARCHAR(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.Column('required_wins', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['game_rules_id'], ['gamerules.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('gamedata',
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('current_day', sa.INTEGER(), nullable=True),
    sa.Column('current_year', sa.INTEGER(), nullable=True),
    sa.Column('is_year_setup', sa.BOOLEAN(), nullable=True),
    sa.Column('is_year_finished', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('competitiongroup',
    sa.Column('oid', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('parent_group_id', sa.VARCHAR(), nullable=True),
    sa.Column('sub_competition_id', sa.VARCHAR(), nullable=True),
    sa.Column('level', sa.INTEGER(), nullable=True),
    sa.Column('group_type', sa.VARCHAR(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['parent_group_id'], ['competitiongroup.oid'], ),
    sa.ForeignKeyConstraint(['sub_competition_id'], ['subcompetitions.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    # ### end Alembic commands ###