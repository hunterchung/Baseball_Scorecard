import os
from django.shortcuts import render, redirect, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.db.models import Q
from scorecard.models import *
from scorecard.forms import *


def add_player(request):
    c = {}
    c.update(csrf(request))
    
    if request.method=='POST':
        form = Player_form(request.POST)
        if form.is_valid():
            player = form.save()
            c['message'] = '%s was added.'%(player.get_full_name())
            form = Player_form()
            return redirect('/add_lineups/')
        else:
            c['errors'] = bpd_form.errors
    else:
        form = Player_form()
    c['form'] = form
        
    return render(request, 'add_player.html', c)
    
def new_game(request):
    c = {}
    c.update(csrf(request))
    
    if request.method=='POST':
        form = Game_form(request.POST)
        if form.is_valid():
            game = form.save()

        else:
            c['errors'] = bpd_form.errors
    else:
        form = Game_form()
    c['form'] = form
        
    return render(request, 'new_game.html', c)

def add_lineups(request):
    c = {}
    c['game'] = Game.objects.filter(end_time=None).prefetch_related('home_team__players').prefetch_related('away_team__players').reverse()[0]
    c['positions'] = (
        'P',
        'C',
        '1B',
        '2B',
        '3B',
        'SS',
        'RF',
        'CF',
        'LF',
        'DH',
    )
    c['order'] = range(1, 11)
    return render(request, 'add_lineups.html', c)

def get_scoreboard(game):
    current_half_inning = game.get_current_half_inning()
    
    ## need at least 9 innings.
    if current_half_inning:
        score_board_col_names = range(1, max(current_half_inning.num, 9)+1)
    else:
        score_board_col_names = range(1, 10)

    top_inning_scoreboard = ['' for i in range(len(score_board_col_names))]
    for i, inning in enumerate(game.half_inning_set.filter(is_top=True)):
        top_inning_scoreboard[i] = inning.get_run()
    top_inning_scoreboard.append(sum(filter(lambda x: x!='', top_inning_scoreboard)))
        
    bottom_inning_scoreboard = ['' for i in range(len(score_board_col_names))]
    for i, inning in enumerate(game.half_inning_set.filter(is_top=False)):
        bottom_inning_scoreboard[i] = inning.get_run()
    bottom_inning_scoreboard.append(sum(filter(lambda x: x!='', bottom_inning_scoreboard)))

    score_board_col_names += ['R', 'H', 'E']
    
    ## add hits    
    top_inning_scoreboard.append(
        [at_bat.is_hit() for half_inning in game.half_inning_set.filter(is_top=True) for at_bat in half_inning.at_bat_set.all()].count(True)
    )
    
    bottom_inning_scoreboard.append(
        [at_bat.is_hit() for half_inning in game.half_inning_set.filter(is_top=False) for at_bat in half_inning.at_bat_set.all()].count(True)
    )
    
    ## add error (get from the other half innings)
    top_inning_scoreboard.append(
        [play.play_type==Play.ERROR for half_inning in game.half_inning_set.filter(is_top=False) 
                for at_bat in half_inning.at_bat_set.all()
                    for play in at_bat.play_set.all()].count(True)
    )
    
    bottom_inning_scoreboard.append(
        [play.play_type==Play.ERROR for half_inning in game.half_inning_set.filter(is_top=True) 
                for at_bat in half_inning.at_bat_set.all()
                    for play in at_bat.play_set.all()].count(True)
    )
    
    return score_board_col_names, top_inning_scoreboard, bottom_inning_scoreboard

def current_game(request):
    game = Game.objects.filter(end_time=None).prefetch_related('half_inning_set__at_bat_set__play_set').reverse()[0]
    current_half_inning = game.get_current_half_inning()
    
    if request.method=='POST':
        if current_half_inning:
            pass
        else:
            half_inning = Half_inning.objects.create(game)
            at_bat = At_bat.objects.create(half_inning)
    
    score_board_col_names, top_inning_scoreboard, bottom_inning_scoreboard = get_scoreboard(game)

    c = {
        'game': game,
        'score_board_col_names': score_board_col_names,
        'half_inning_scoreboards': [top_inning_scoreboard, bottom_inning_scoreboard],
        'current_half_inning': current_half_inning,
    }
    c.update(csrf(request))
    
    return render(request, 'current_game.html', c)
    
    
    
    
    
    
def welcome(request):
    return render(request, 'welcome.html')