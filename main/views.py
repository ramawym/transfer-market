from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name' : 'Walyul\'ahdi Maulana Ramadhan',
        'npm' : '2406426012',
        'class' : 'PBP - F'
    }
    
    return render(request, "main.html", context)
