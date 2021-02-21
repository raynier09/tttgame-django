from collections import Counter
from django.urls import reverse
from django.db import models



class Game(models.Model):

    # This class will define the board state for Tic Tac Toe Game.
    # The board is meant to be played a 9 character string (Standard Game).
    # This model will meant to be played by two players which is player 1 (X) and player 2 (O).

    board = models.CharField(max_length=9, default=" " * 9)
    player_x = models.CharField(max_length=64)
    player_o = models.CharField(max_length=64)
    winner = models.CharField(max_length=1, null=True)

    # This method will displayed the string on django administration and other use cases.
    def __str__(self):
        return '{0} vs {1}, state="{2}"'.format(self.player_x, self.player_o, self.board)

    # This is useful for passing of primary to url and other use cases.
    def get_absolute_url(self):
        return reverse('game:detail', kwargs={'pk': self.pk})

    # Define a database table when migrating to other database (ex. POSTGRESQL.)
    class Meta:
        db_table = 'ttt_game'

    @property
    def next_player(self):
        # Counter is a useful class that counts objects to determine which player will be played next.
        # If player 1 has played more than player 2, it's player 2 turn; otherwise, player 1 plays.
        count = Counter(self.board)
        if count.get('X', 0) > count.get('O', 0):
            return 'O'
        return 'X'

    # List of Winning Pattern that will determine the winner of the game.
    WINNING_COMBINATION = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],  
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    @property
    def is_game_over(self):
        
        # This method will check if there is a winning pattern. 
        board = list(self.board)
        for wins in self.WINNING_COMBINATION:
            w = (board[wins[0]], board[wins[1]], board[wins[2]])
            if w == ('X', 'X', 'X'):
                return 'X'
            if w == ('O', 'O', 'O'):
                return 'O'
        
        # Check for draw
        if ' ' in board:
            return None
        return ' '

    def play(self, index):

    # Raises Validation when user input is not valid     
        if index < 0 or index >= 9:
            raise IndexError("Invalid board index")

        if self.board[index] != ' ':
            raise ValueError("Square already played")
        
        # This section will change the state of the board and who the player plays this time.
        board = list(self.board)
        board[index] = self.next_player
        self.board = u''.join(board)

    # This method will override the save on views.py
    def save(self, *args, **kwargs):
        self.winner = self.is_game_over        
        
        # This section will update the player who won the game 
        try:
            score_count_x = Leaderboard.objects.get(game_id=self.id, player=self.player_x)
            score_count_o = Leaderboard.objects.get(game_id=self.id, player=self.player_o)
            if self.winner == 'X':
                score_count_x.score = 1 
                score_count_x.save()
            if self.winner == 'O':
                score_count_o.score = 1 
                score_count_o.save()
        except Exception as e:
            print(e)

        return super(Game, self).save(*args, **kwargs)

class Leaderboard(models.Model):

    game_id = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    player = models.CharField(max_length=30)
    score = models.IntegerField(null=True, default=0)

    # This method will displayed the string on django administration and other use cases.
    def __str__(self):
        return '{0} - {1}'.format(self.player, self.score)

    # Define a database table when migrating to other database (ex. POSTGRESQL.)
    class Meta:
        db_table = 'ttt_leaderboard'
    
    