import random
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Baseball_Scorecard.settings'
from scorecard.models import *


for team_name in ('Irvine', 'LA'):
    team = Team.objects.create(name=team_name)
    
    for i in range(9):
        player = Player.objects.create(
            username='player_%s%d'%(team_name, i+1),
            first_name='%s%d'%(team_name, i+1),
            is_left_throw=random.choice((True, False)),
            batting_side=random.choice(('left', 'right', 'switch')),
        )
        team.players.add(player)