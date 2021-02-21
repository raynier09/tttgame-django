from django import forms
from .models import Game, Leaderboard

class NewGameForm(forms.Form):
    player1 = forms.CharField(max_length=64, required=True)
    player2 = forms.CharField(max_length=64, required=True)

    def create(self):
        # This method will create a new game
        # This method also will call on the index views.py 
        players = [self.cleaned_data['player1'], self.cleaned_data['player2']]
        return Game.objects.create(player_x=players[0],
                                   player_o=players[1])

    def init_leaderboard(self, id):
        # This method will initialize the player leaderboards
        # This method also will call on the index views.py
        players = [self.cleaned_data['player1'], self.cleaned_data['player2']]
        return Leaderboard.objects.bulk_create([
            Leaderboard(game_id=id,player=players[0]),
            Leaderboard(game_id=id,player=players[1]),
        ])

class PlayForm(forms.Form):
    #This class will call on the game views.py
    index = forms.IntegerField(min_value=0, max_value=8)