from multiprocessing import context
from django.shortcuts import render
from django.views.generic import View
from shop.models import Product
# Create your views here.


def home(request):

    qs = Product.objects.all()[0:4]
    qs_order = Product.objects.all().order_by('-id')
 

    

    context = {
        'products': qs,
        'products_order': qs_order,
    }

    return render(request, 'index.html', context=context)



def delivery(request):

    return render(request, 'delivery.html')

def contact(request):

    return render(request, 'contact.html')