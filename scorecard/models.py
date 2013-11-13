import os
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import AbstractUser
import django.db.models
# from django_enumfield import enum

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
    
class Team(models.Model):
    name = models.CharField(max_length='45')
    members = models.ManyToManyField('Player')
    
    def __unicode__(self):
        return self.name

class Player(AbstractUser):
    BATTING_SIDE_OPTIONS = (
        ('left', 'left'),
        ('right', 'right'),
        ('switch', 'switch'),
    )
    
    is_left_throw = models.BooleanField()
    batting_side = models.CharField(max_length=10, choices=BATTING_SIDE_OPTIONS)
    
    def __unicode__(self):
        return self.get_full_name()
    
class Defense_lineup(models.Model):
    pitcher = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    catcher = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    first_baseman = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    second_baseman = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    third_baseman = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    shortstop = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    left_fielder = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    center_fielder = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)
    right_fielder = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.DO_NOTHING)

class Play(models.Model):
    SINGLE = '1B'
    DOUBLE = '2B'
    TRIPLE = '3B'
    HOMERUN = 'HR'
    WALK = 'BB'
    STRIKEOUT = 'K'
    STRIKEOUT_LOOKING = 'Kc'
    FIELDERS_CHOICE = 'FC'
    HIT_BY_PITCHER = 'HP'
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
    
    PLAY_TYPE_OPTIONS = (
        (SINGLE, 'single'),
        (DOUBLE, 'double'),
        (TRIPLE, 'triple'),
        (HOMERUN, 'homerun'),
        (WALK, 'walk'),
        (STRIKEOUT, 'strikeout'),
        (STRIKEOUT_LOOKING, 'strikeout looking'),
        (FIELDERS_CHOICE, 'fielder\'s choice'),
        (HIT_BY_PITCHER, 'hit by pitcher'),
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
    
    batter = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.SET_NULL, null=True, blank=True)
    Defense_lineup = models.ForeignKey('Defense_lineup', on_delete=django.db.models.DO_NOTHING) ## do not consider changing defense during play yet
    at_bat = models.ForeignKey('At_bat', on_delete=django.db.models.DO_NOTHING)
    
    play_type = models.CharField(max_length=3, choices=PLAY_TYPE_OPTIONS)
    time = models.DateTimeField(auto_now_add=True)
    
    strikes = models.PositiveIntegerField()
    balls = models.PositiveIntegerField()
    outs = models.PositiveIntegerField() ## after the play
    run = models.PositiveIntegerField() ## after the play
    
    first_base_runner = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.SET_NULL, null=True, blank=True) ## after the play
    second_base_runner = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.SET_NULL, null=True, blank=True) ## after the play
    third_base_runner = models.ForeignKey('Player', related_name='+', on_delete=django.db.models.SET_NULL, null=True, blank=True) ## after the play
    
    def get_outs(self):
        if self.play_type in (STRIKEOUT_LOOKING, STRIKEOUT, CAUGHT_STEALING, SACRIFICE_FLY, GROUND_OUT, FLY_OUT, BUNT):
            return 1
        elif self.play_type==DOUBLE_PLAY:
            return 2
        elif self.play_type==TRIPLE_PLAY:
            return 3
        else:
            return 0
    
class At_bat(models.Model):
    inning = models.ForeignKey('Half_inning', on_delete=django.db.models.DO_NOTHING)
    
    def is_hit(self):
        return self.play_set.order_by('time').reverse()[0].play_type in (SINGLE, DOUBLE, TRIPLE, HOMERUN)
    
    
class Half_inning(models.Model):
    game = models.ForeignKey('Game', on_delete=django.db.models.DO_NOTHING)
    is_top = models.BooleanField()
    num = models.PositiveIntegerField()
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def get_run(self):
        return sum([play.run for at_bat in self.at_bat.set for play in at_bat.play_set])
            
    
class Game(models.Model):
    WEATHER_OPTIONS = (
        ('Sunny', 'Sunny'),
        ('Cloudy', 'Cloudy'),
        ('Rainy', 'Rainy'),
    )
    
    home_team = models.ForeignKey('Team', related_name='home_team', on_delete=django.db.models.DO_NOTHING)
    away_team = models.ForeignKey('Team', related_name='away_team', on_delete=django.db.models.DO_NOTHING)
    weather = models.CharField(max_length=10, choices=WEATHER_OPTIONS)
    temperature = models.PositiveIntegerField(null=True, blank=True) ## in Fahrenheit
    
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def get_current_half_inning(self):
        try:
            return self.half_inning_set.order_by('num', 'is_top').reverse()[0]
        except:
            return None
    
    
    def __unicode__(self):
        return "%s @ %s on %s"%(self.away_team.name, self.home_team.name, self.start_time)
    
    
    
    