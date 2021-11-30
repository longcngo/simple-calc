from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

from .forms import InputForm
from .calculate import evaluate

# Create your views here.
def index(request):
    return_val = ''
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.clean_input()
            return_val = evaluate(input)
        else:
            return_val = form.errors['input'].as_text()[2:]

    form = InputForm(initial={'input': return_val})

    context = {
        'form' : form
    }

    return render(request, 'calc/index.html', context)
