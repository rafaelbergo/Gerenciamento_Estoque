from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'estoque/pages/home.html', context)