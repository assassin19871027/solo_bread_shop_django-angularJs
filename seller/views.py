from datetime import datetime, timedelta
import stripe
import jwt
import json
import requests

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from twilio.rest import TwilioRestClient

from models import *
from rest_framework import viewsets
from serializers import ProductSerializer, SellerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to viewed or edited.
    """
    queryset = Product.objects.all().order_by('-date_created')
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['baker_id'] = parse_token(request)['sub']
        data['image'] = 'products/' + data['image']
        # print data, '@@@@@@'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        product = Product(**data)
        product.save()
        # headers = self.get_success_headers(serializer.data)
        return JsonResponse('success', status=201, safe=False)

class SellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for sellers to display or edited.
    """
    queryset = Baker.objects.all()
    serializer_class = SellerSerializer

    def create(self, request, *args, **kwargs):
        sd = 'ok it is'
        print sd
        data = request.data.copy()
        data['business_id'] = parse_token(request)['sub']
        data['logo'] = 'bakers/' + data['logo']
        # print data, '@@@@@@'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        seller = Baker(**data)
        seller.save()
        # headers = self.get_success_headers(serializer.data)
        return JsonResponse('success', status=201, safe=False)

    def retrieve(self, request, pk=None):
        parsed_token = parse_token(request)
        pk = parsed_token['sub'] if parsed_token else pk
        baker = Baker.objects.get(pk=pk)
        serializer = SellerSerializer(baker)
        return Response(serializer.data)


def facebook():
    access_token_url = 'https://graph.facebook.com/v2.5/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/v2.5/me?fields=id,name,email'

    params = {
        'client_id': request.json['clientId'],
        'redirect_uri': request.json['redirectUri'],
        'client_secret': app.config['FACEBOOK_SECRET'],
        'code': request.json['code']
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.get(access_token_url, params=params)
    # access_token = dict(parse_qsl(r.text))
    access_token = json.loads(r.text)

    # Step 2. Retrieve information about the current user.
    r = requests.get(graph_api_url, params=access_token)
    profile = json.loads(r.text)

    # Step 3. (optional) Link accounts.
    if request.headers.get('Authorization'):
        user = User.query.filter_by(facebook=profile['id']).first()
        if user:
            response = json.dumps(message='There is already a Facebook account that belongs to you')
            response.status_code = 409
            return response

        payload = parse_token(request)

        user = User.query.filter_by(id=payload['sub']).first()
        if not user:
            response = json.dumps(message='User not found')
            response.status_code = 400
            return response

        user.facebook = profile['id']
        user.display_name = user.display_name or profile['name']
        db.session.commit()
        token = create_token(user)
        return json.dumps(token=token)

    # Step 4. Create a new account or return an existing one.
    user = User.query.filter_by(facebook=profile['id']).first()
    if user:
        token = create_token(user)
        return json.dumps(token=token)

    u = User(facebook=profile['id'], display_name=profile['name'], email=profile['email'])
    db.session.add(u)
    db.session.commit()
    token = create_token(u)
    return json.dumps(token=token)

@csrf_exempt
def stripe_(request):
    access_token_url = 'https://connect.stripe.com/oauth/token'
    request_json = json.loads(request.body)
    params = {
        'client_id': request_json['clientId'],
        'client_secret': settings.STRIPE_KEYS['API_KEY'],
        'code': request_json['code'],
        'grant_type': 'authorization_code',
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, params=params)
    access_token = r.json()

    # Step 2. Retrieve information about the current user.
    stripe.api_key = settings.STRIPE_KEYS['API_KEY']
    profile = stripe.Account.retrieve(access_token["stripe_user_id"])

    # Step 3. (optional) Link accounts.
    if request.META.get('Authorization'):
        print 'Step 3 triggered ###'
        user = Baker.objects.filter(stripe_acct_id=profile['id']).first()
        if user:
            response = JsonResponse({'message': 'There is already a stripe account that belongs to you'})
            response.status_code = 409
            return response

        payload = parse_token(request)

        user = Baker.objects.filter(id=payload['sub']).first()
        if not user:
            response = JsonResponse({'message': 'User not found'})
            response.status_code = 400
            return response

        user.stripe_acct_id = profile['id']
        user.display_name = user.username or profile['display_name']
        user.save()
        token = create_token(user)
        return JsonResponse({'token': token})

    # Step 4. Create a new account or return an existing one.
    user = Baker.objects.filter(stripe_acct_id=profile['id']).first()
    if user:
        token = create_token(user)
        return JsonResponse({'token': token})

    user = Baker(logo=profile['business_logo'],
                 business_name=profile['business_name'],
                 url_business_website=profile['business_url'],
                 business_contact_name=profile['display_name'],
                 username=profile['email'].split('@')[0],
                 email=profile['email'],
                 stripe_acct_id=profile['id'])

    user.save()
    token = create_token(user)
    return JsonResponse({'token': token})

def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, settings.TOKEN_SECRET)
    return token.decode('unicode_escape')

def parse_token(req):
    if req.META.get('HTTP_AUTHORIZATION'):
        token = req.META.get('HTTP_AUTHORIZATION').split()[1]
        return jwt.decode(token, settings.TOKEN_SECRET)


@csrf_exempt
def upload_product_photo(request):
    myfile = request.FILES['file']
    location = settings.MEDIA_ROOT+'/products/'
    fs = FileSystemStorage(location=location)
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    return JsonResponse({'ok': 'products/'+filename})


@csrf_exempt
def charge(request):
    print request.body
    params = json.loads(request.body)
    stripe.api_key = settings.STRIPE_KEYS['API_KEY']

    total_price = 0
    for product in params['products']:
        price_in_cents = float(product['unit_price']) * float(product['quantity']) * 100
        tax = product['delivery_fee'] * 100
        total_price += int(price_in_cents + tax)

    # charge to app
    total_charge = stripe.Charge.create(
        amount=total_price,
        currency="usd",
        source=params['token'],
        description='Thank you for your purchase!'
    )

    for product in []:#params['products']:
        baker = Baker.objects.get(id=product['baker_id'])
        price_in_cents = float(product['unit_price']) * float(product['quantity']) * 100
        tax = product['delivery_fee'] * 100

        # send division to each baker
        transfer = stripe.Transfer.create(
            amount=int(price_in_cents+tax),
            currency="usd",
            destination=baker.stripe_acct_id,
            application_fee = int(price_in_cents * 0.05),
            description='Thank you for your purchase!'
        )

        sale = Sale()
        sale.baker = baker
        sale.delivery_address = params['address']
        sale.customer = params['username']
        sale.phone = params['phone']
        sale.email = params['email']
        sale.charge_id = transfer.id
        sale.save()

        # send email
        email_subject = 'Order Confirmation'
        email_body = "Dear %s.\n\nYou've got an order from Customer: %s \nAddress: %s\nPhone Number: %s\nProduct: %s\nQuantity: %.2f\nPlease confirm the order and fulfill it.\n\nThank you." % (baker.business_name, sale.customer, sale.delivery_address, sale.phone, product['name'], product['quantity'])

        send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [baker.email], fail_silently=False)
        send_SMS(baker.business_cell_phone)

    return JsonResponse({'status': 'success'})


def send_SMS(phone_number):
    '''
    send SMS to the baker to confirm the order using twillio
    '''
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        to='+1'+phone_number,
        from_="+18582473889",
        body="You have a new order from GetFreshBaked. Please check your email and confirm with the buyer.",
    )


@csrf_exempt
def comment(request):
    print request.body
    params = json.loads(request.body)
    type_ = params['type']

    if type_ == 'product':
        product = Product.objects.get(id=params['item'])
        product.num_likes = params['rate']
        product.save()

        params['product_id'] = params['item']
        params.pop('item', None)
        params.pop('type', None)
        params.pop('rate', None)
        comment = ProductComment(**params)
        comment.save()
    else:
        baker = Baker.objects.get(id=params['item'])
        baker.rate = params['rate']
        baker.save()

        params['baker_id'] = params['item']
        params.pop('item', None)
        params.pop('type', None)
        params.pop('rate', None)
        comment = BakerComment(**params)
        comment.save()

    return JsonResponse({'status': 'ok'})
