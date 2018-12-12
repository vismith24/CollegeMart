from django.shortcuts import render, redirect

from . models import Feedback
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def home(request):
    print('a')
    if request.method=='POST':
        name = request.user.username
        comments = request.POST['comments']
        Feedback.objects.create(name=name, comments=comments)
        return redirect('buyer:home')
    else:
        print('b')
        return render(request,'feedback/1.html')
