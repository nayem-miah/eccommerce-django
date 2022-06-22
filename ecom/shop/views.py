from ast import And
from audioop import add
from time import process_time_ns
from django.shortcuts import redirect, render,get_object_or_404
from . import models
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from  . form import CheckoutForm
from django.utils import timezone
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY



class Cart_view(View,LoginRequiredMixin):

    

    def get(self, *args, **kwargs):

        if self.request.user.is_authenticated:

            user = self.request.user

            cart = models.Card.objects.filter(user = user)


            length = len(cart)

            def whole_total_price():
                a = 0
                for da in cart:  
                    a= a+da.final_total_money()
                return a
            
            def whole_total_discount():
                a = 0
                for da in cart:  
                    a= a+da.total_discount_price()
                return a
            
            def total_price():
                a = 0
                for da in cart:  
                    a= a+da.total_product_price()
                return a


            context = {
                'carts': cart,
                'total_price': total_price(),
                'final_total_price': whole_total_price(),
                'total_discount': whole_total_discount(),
                'len':length
            }

            return render(self.request, 'cart.html', context=context) 
        else:
            return redirect('home')


class Products(View):
    def get(self, request, *args, **kwargs):
        qs = models.Product.objects.all()  

        context = {
            'products': qs
        }
        return render(request, 'products.html', context=context)





class Products_detail(View):
    def get(self, *args, **kwargs):


        unique_id=kwargs['unique_id']
        qs=models.Product.objects.get(unique_id = unique_id)

        context ={
            "products": qs
        }

        return render(self.request, 'product_details.html', context=context)




def add_to_cart(request, unique_id):

    product = get_object_or_404(models.Product, unique_id=unique_id)

    try:
        if request.user.is_authenticated:
            card_product = models.Card.objects.get(product = product, user= request.user)
            card_product.quantity+=1
            card_product.save()
            return redirect('cart')
        else:
            return redirect('home')

    except ObjectDoesNotExist:

        add_product = models.Card.objects.create(
            product=product,
            user=request.user,
        )

    return redirect('home')



def remove_from_cart(request, unique_id):

    product = get_object_or_404(models.Product, unique_id=unique_id)
    try:
        esist_product = models.Card.objects.get(product = product, user= request.user)
        esist_product.quantity-=1

        if esist_product.quantity < 1:
            return redirect('cart')

        esist_product.save()  
        return redirect('cart')

    except ObjectDoesNotExist:
        return redirect('cart')



def delete_cart(request, unique_id):

    product = get_object_or_404(models.Product, unique_id=unique_id)
    try:
        esist_product = models.Card.objects.get(product = product, user= request.user)
        esist_product.delete()   
        return redirect('cart')

    except ObjectDoesNotExist:
        return redirect('cart')


class Checkout(View):

    def get(self,*args, **kwargs):
        try:
            address = models.Address.objects.filter(user = self.request.user)[0]

         
            if address:
                initial={

                        'apartment_address':address.apartment_address,
                        'country': address.country,
                        'zip': address.zip
                }

                context = {
                    'form':CheckoutForm(initial = initial)
                }
            

                return render(self.request, 'checkout.html', context=context)
            
       
            return render(self.request, 'checkout.html', context=context)

        except:
            context = {
            'form':CheckoutForm()
            }

            return render(self.request, 'checkout.html', context=context)


    
    def post(self, *args, **kwargs):

        form = CheckoutForm(self.request.POST)

        if form.is_valid():
           
            apartment_address = form.cleaned_data.get('apartment_address')
        
            country = form.cleaned_data.get('country')
         
            zip = form.cleaned_data.get('zip')
    

            address = models.Address.objects.create(
                user = self.request.user,
                apartment_address = apartment_address,
                country = country,
                zip = zip
                
                )
           
            
            order = models.Order.objects.create(user= self.request.user, address=address)
            cards = models.Card.objects.filter(user = self.request.user)

            for card in cards:

                order_item = models.Order_Item.objects.create(
                      user =self.request.user,
                      product = card.product,
                      quantity = card.quantity,
                      
                      )
                order.order_item.add(order_item)
            
            
            cards.delete()
        
            return redirect('payment')




class Payment_view(View):
    def get(self, *args, **kwargs):
        order = models.Order.objects.filter(user=self.request.user, ordered=False)[0]

        if order.address:
            context = {
                'order': order,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
     
            return redirect("checkout")

    def post(self, *args, **kwargs):

        order = models.Order.objects.filter(user=self.request.user, ordered=False)[0]
        token = self.request.POST['stripeToken']
        amount = int(order.get_total() * 100)


        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token,
            )
            # create the payment
            payment = models.Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order
            order.ordered = True
            order.paid = True
            order.payment = payment
            order.save()

            return redirect("/")
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
         
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
        
            print(e)
            return redirect("/")

