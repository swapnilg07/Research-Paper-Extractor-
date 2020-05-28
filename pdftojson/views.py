from django.http import HttpResponse
from django.shortcuts import render
from . import converter

def index(request):
    return render(request,'index.html')

def converted(request):
    q="";s=""
    try:
        q=request.GET.get('filename','default')
        if q=='default':
            return index(request)
    except Exception as e:
        print(e)
        return HttpResponse("Please insert valid file.")

    try:
        s="C:\\Users\\swapn\\pythonproject\\pdftojson\\pdftojson\\"+q
        my_details=converter.pdftojson(s)
    except Exception as e:
        print(e)
        return HttpResponse("Entered file is missing or may be empty.")

    return render(request,'last.html',my_details)
