import os
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import AbstractUser
import django.db.models

# class Position(enum.Enum):
#     pitcher = 1
#     catcher = 2
#     first_baseman = 3
#     second_baseman = 4
#     third_baseman = 5
#     shortstop = 6
#     left_fielder = 7
#     center_fielder = 8
#     right_fielder = 9
    
# class Team(models.Model):
#     name = models.CharField(max_length='45')
#     players = models.ManyToManyField('Player')
#     
#     def __unicode__(self):
#         return self.name

class Player(AbstractUser):
    BATTING_SIDE_OPTIONS = (
        ('left', 'left'),
        ('right', 'right'),
        ('switch', 'switch'),
    )
    
    is_right_throw = models.BooleanField(default=True)
    batting_side = models.CharField(max_length=10, choices=BATTING_SIDE_OPTIONS, null=True)
    
    def __unicode__(self):
        return self.get_full_name()
    
# class Defense_lineup(models.Model):
#     pitcher = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     catcher = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     first_baseman = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     second_baseman = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     third_baseman = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     shortstop = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     left_fielder = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     center_fielder = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
#     right_fielder = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)

class Pitch(models.Model):
    SINGLE = '1B'
    DOUBLE = '2B'
    TRIPLE = '3B'
    HOMERUN = 'HR'
    WALK = 'BB'
    STRIKEOUT = 'K'
    STRIKEOUT_LOOKING = 'Kc'
    FIELDERS_CHOICE = 'FC'
    HIT_BY_PITCH = 'HP'
    WILD_PITCH = 'WP'
    STOLEN_BASE = 'SB'
    CAUGHT_STEALING = 'CS'
    DOUBLE_PLAY = 'DP'
    TRIPLE_PLAY = 'TP'
    ERROR = 'E'
    SACRIFICE_FLY = 'SF'
    GROUND_OUT = 'G'
    FLY_OUT = 'F'
    BUNT = 'B'
    # PASS_BALL = 'PB
    
    FLYBALL = 'FB'
    GROUNDBALL = 'GB'
    LINEDRIVE = 'LD'
    
    RESULT_OPTIONS = (
        (SINGLE, 'single'),
        (DOUBLE, 'double'),
        (TRIPLE, 'triple'),
        (HOMERUN, 'homerun'),
        (WALK, 'walk'),
        (STRIKEOUT, 'strikeout'),
        (STRIKEOUT_LOOKING, 'strikeout looking'),
        (FIELDERS_CHOICE, 'fielder\'s choice'),
        (HIT_BY_PITCH, 'hit by pitch'),
        (WILD_PITCH, 'wild pitch'),
        (STOLEN_BASE, 'stolen base'),
        (CAUGHT_STEALING, 'caught stealing'),
        (DOUBLE_PLAY, 'double play'),
        (TRIPLE_PLAY, 'triple play'),
        (ERROR, 'error'),
        (SACRIFICE_FLY, 'sacrifice fly'),
        (GROUND_OUT, 'gorund out'),
        (FLY_OUT, 'fly out'),
        (BUNT, 'bunt'),
    )
    
    RESULT_TYPE_OPTIONS = (
        (FLYBALL, 'fly ball'),
        (GROUNDBALL, 'ground ball'),
        (LINEDRIVE, 'linedrive'),
    )
    
    is_strike = models.BooleanField()
    swung = models.BooleanField()
    is_foul = models.BooleanField(default=False)
    strikes = models.PositiveIntegerField()
    balls = models.PositiveIntegerField()
    outs = models.PositiveIntegerField()
    runner_on_first = models.BooleanField(default=False)
    runner_on_second = models.BooleanField(default=False)
    runner_on_third = models.BooleanField(default=False)
    away_score = models.PositiveIntegerField()
    home_score = models.PositiveIntegerField()
    
    result = models.CharField(max_length=5, choices=RESULT_OPTIONS, blank=False)
    direction = models.CharField(max_length=5)
    run = models.PositiveIntegerField() ## after the play
    game = models.ForeignKey('Game', blank=False)
    result_type = models.CharField(max_length=5, choices=RESULT_TYPE_OPTIONS, blank=False)
    
    pitcher = models.ForeignKey('Player', related_name='pitch_pitcher')
    batter = models.ForeignKey('Player', related_name='pitch_batter')
    catcher = models.ForeignKey('Player', related_name='pitch_catcher')
    fielder = models.ForeignKey('Player', related_name='pitch_fielder')
    
    inning = models.PositiveIntegerField()
    is_top = models.BooleanField()
    
    def __unicode__(self):
        return self.result
        
    def play_outs(self):
        if reuslt=='DP':
            return 2
        elif result=='TP':
            return 3
        elif result in ('K', 'Kc', 'CS', 'SF', 'G', 'F', 'B'):
            return 1
        else:
            raise

# class Lineup(models.Model):
#     batting_order = models.ManyToManyField('Player')
#     defense_lineup = models.ForeignKey('Defense_lineup', related_name='lineup_defense_lineup', on_delete=django.db.models.DO_NOTHING)
#     team = models.ForeignKey('Team')
    
class Game(models.Model):
    WEATHER_OPTIONS = (
        ('Sunny', 'Sunny'),
        ('Cloudy', 'Cloudy'),
        ('Rainy', 'Rainy'),
    )
    
    # home_lineup = models.ForeignKey('Lineup', related_name='game_home_lineup', on_delete=django.db.models.DO_NOTHING, null=True, blank=True)
    # away_lineup = models.ForeignKey('Lineup', related_name='game_away_lineup', on_delete=django.db.models.DO_NOTHING, null=True, blank=True)
    
    home_team_name = models.CharField(max_length=100)
    away_team_name = models.CharField(max_length=100)
    
    weather = models.CharField(max_length=10, choices=WEATHER_OPTIONS)
    temperature = models.PositiveIntegerField(null=True, blank=True, help_text='in Fahrenheit')
    
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return "%s @ %s on %s"%(self.away_team_name, self.home_team_name, str(self.start_time).split()[0])
    
    
    
    