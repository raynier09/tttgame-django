from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Game,Leaderboard
from django.db.models import Sum

def index(request):

    # POST Data validation
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            # This section will call the method on the forms.py. After the forms are validated it will redirected to the game.
            game = form.create()
            form.init_leaderboard(id=game)
            game.save()
            print('Game Created')
            return redirect(game)
    else:
        form = NewGameForm()

    # Fetching and passing the data from form/ HTML Template
    context = {'form': form}
    return render(request,'game/index.html', context=context)

def leaderboard(request):

    #This variable will fetch all the players and total scores accumulated throughout the game
    players = Leaderboard.objects.values('player').order_by('-total').annotate(total=Sum('score'))
    
    # Passing the data from HTML Template
    context = {'players': players}
    return render(request,'game/leaderboard.html', context=context)

def game(request, pk):
    game = get_object_or_404(Game, pk=pk)

    #POST Data Validation
    if request.method == 'POST':
        form = PlayForm(request.POST)
        if form.is_valid():
            # This section will changed the state of the board in model. 
            # Even closing the browser the game will continue as long as it finish and you can provide the game id in the URL.
            game.play(form.cleaned_data['index'])
            game.save()
            return redirect(game)
    
    # Passing and Fetching of data from the form/ HTML Template
    context = {'game': game}
    return render(request, 'game/gameplay.html', context=context)