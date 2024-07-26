from django.shortcuts import render
from .forms import ContactForm

def index(request):
    return render(request, 'home/index.html')

def faq(request):
    return render(request,'home/faq.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # process the data
            pass
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})