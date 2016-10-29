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

from models import Product, Baker
from rest_framework import viewsets
from serializers import ProductSerializer, SellerSerializer


class ProductViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows products to viewed or edited.
	"""
	queryset = Product.objects.all().order_by('-date_created')
	serializer_class = ProductSerializer


class SellerViewSet(viewsets.ModelViewSet):
	"""
	API endpoint for sellers
	"""
	queryset = Baker.objects.all()
	serializer_class = SellerSerializer

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
                 first_name=profile['display_name'].split('.')[0],
                 last_name=profile['display_name'].split('.')[1],
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
    token = req.META.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_SECRET'])


@csrf_exempt
def upload_product_photo(request):
    myfile = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    return JsonResponse({'ok': uploaded_file_url})
