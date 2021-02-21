from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Game,Leaderboard
from django.db.models import Sum

def index(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST)

        if form.is_valid():
            game = form.create()
            form.init_leaderboard(id=game)
            game.save()
            print('Game Created')
            return redirect(game)
    else:
        form = NewGameForm()

    context = {'form': form}
    return render(request,'game/index.html', context=context)

def leaderboard(request):

    players = Leaderboard.objects.values('player').order_by('-total').annotate(total=Sum('score'))
    context = {'players': players}
    return render(request,'game/leaderboard.html', context=context)

def game(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == 'POST':
        form = PlayForm(request.POST)
        if form.is_valid():
            game.play(form.cleaned_data['index'])
            game.save()
            return redirect(game)
    
    context = {'game': game}
    return render(request, 'game/gameplay.html', context=context)