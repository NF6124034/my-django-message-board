from django.shortcuts import render

# def hello(request):
#     return render(request, 'hello.html')

def hello(request,name):
    context = {
        'name': name,
    }
    return render(request, 'hello.html', context)
