# payments/views.py

from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import stripe
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

class HomePageView(TemplateView): #Basic plan view
    template_name = 'home.html'

class HomePageViewPro(TemplateView): #Pro plan view
    template_name = 'homepro.html'

@csrf_exempt
def StripeConfig(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def CreateCheckoutSessionBasic(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': 'price_1OwkGv04HRGJNzM4N608reGR',
                        'quantity': 1,
                    }
                ]
            )
            request.session['subscription_id'] = checkout_session['subscription']
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def CreateCheckoutSessionPro(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': 'price_1OwkJF04HRGJNzM4lrNADpqb',
                        'quantity': 1,
                    }
                ]
            )
            request.session['subscription_id'] = checkout_session['subscription']
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'

@csrf_exempt
def CancelSubscription(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Obtener todas las suscripciones activas
            subscriptions = stripe.Subscription.list(status='active')
            
            # Filtrar las suscripciones para eliminar las canceladas
            active_subscriptions = [subscription for subscription in subscriptions.data if not subscription.cancel_at_period_end]
            
            # Verificar si hay suscripciones activas
            if active_subscriptions:
                # Obtener la última suscripción activa
                last_active_subscription = active_subscriptions[-1]
                
                # Obtener el ID de la última suscripción activa
                subscription_id = last_active_subscription.id
                
                # Cancelar la última suscripción activa utilizando la API de Stripe
                stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
                
                return JsonResponse({'success': True, 'message': 'Subscription successfully canceled.'})
            else:
                return JsonResponse({'success': False, 'error': 'No active subscriptions found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed.'})
    
@csrf_exempt
def ReactivateSubscription(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Obtener todas las suscripciones
            subscriptions = stripe.Subscription.list()
            
            # Verificar si hay suscripciones canceladas
            canceled_subscriptions = []
            for subscription in subscriptions.data:
                if subscription.cancel_at_period_end:
                    canceled_subscriptions.append(subscription)
            
            # Verificar si hay suscripciones canceladas
            if canceled_subscriptions:
                # Obtener la última suscripción cancelada
                last_canceled_subscription = canceled_subscriptions[-1]
                
                # Obtener el ID de la última suscripción cancelada
                subscription_id = last_canceled_subscription.id
                
                # Reactivar la última suscripción cancelada utilizando la API de Stripe
                stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=False  # Establecer cancel_at_period_end a False para reactivar
                )
                
                return JsonResponse({'success': True, 'message': 'Subscription successfully reactivated.'})
            else:
                return JsonResponse({'success': False, 'error': 'No canceled subscriptions found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed.'})
    
class CancelledSubscriptionView(TemplateView):
    template_name = 'cancelsubscription.html'
