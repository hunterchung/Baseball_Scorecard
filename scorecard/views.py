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
            c['message'] = 'A new game was added.'
            return welcome(request)
        else:
            c['errors'] = bpd_form.errors
    else:
        form = Game_form()
    c['form'] = form
        
    return render(request, 'new_game.html', c)
    
def current_game(request):
    game = Game.objects.filter(end_time=None).prefetch_related('half_inning_set__at_bat_set__play_set').reverse()[0]
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
    

    c = {
        'game': game,
        'score_board_col_names': score_board_col_names,
        'half_inning_scoreboards': [top_inning_scoreboard, bottom_inning_scoreboard],
        'current_half_inning': current_half_inning,
    }
    
    return render(request, 'current_game.html', c)
    
    
    
    
    
    
def welcome(request):
    return render(request, 'welcome.html')