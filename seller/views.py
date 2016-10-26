from datetime import datetime, timedelta
import os
import stripe
import jwt
import json
import requests
import base64

from django.shortcuts import render

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
            response = jsonify(message='There is already a Facebook account that belongs to you')
            response.status_code = 409
            return response

        payload = parse_token(request)

        user = User.query.filter_by(id=payload['sub']).first()
        if not user:
            response = jsonify(message='User not found')
            response.status_code = 400
            return response

        user.facebook = profile['id']
        user.display_name = user.display_name or profile['name']
        db.session.commit()
        token = create_token(user)
        return jsonify(token=token)

    # Step 4. Create a new account or return an existing one.
    user = User.query.filter_by(facebook=profile['id']).first()
    if user:
        token = create_token(user)
        return jsonify(token=token)

    u = User(facebook=profile['id'], display_name=profile['name'], email=profile['email'])
    db.session.add(u)
    db.session.commit()
    token = create_token(u)
    return jsonify(token=token)


# @app.route('/auth/stripe', methods=['POST'])
def stripe_():
    access_token_url = 'https://connect.stripe.com/oauth/token'
    params = {
        'client_id': request.json['clientId'],
        'client_secret': app.config['STRIPE_API_KEY'],
        'code': request.json['code'],   
        'grant_type': 'authorization_code',
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, params=params)
    access_token = r.json()

    # Step 2. Retrieve information about the current user.
    stripe.api_key = app.config['STRIPE_API_KEY']
    profile = stripe.Account.retrieve(access_token["stripe_user_id"])
    
    # Step 3. (optional) Link accounts.
    if request.headers.get('Authorization'):
        user = User.query.filter_by(facebook=profile['id']).first()
        if user:
            response = jsonify(message='There is already a Facebook account that belongs to you')
            response.status_code = 409
            return response

        payload = parse_token(request)

        user = User.query.filter_by(id=payload['sub']).first()
        if not user:
            response = jsonify(message='User not found')
            response.status_code = 400
            return response

        user.facebook = profile['id']
        user.display_name = user.display_name or profile['name']
        db.session.commit()
        token = create_token(user)
        return jsonify(token=token)

    # Step 4. Create a new account or return an existing one.
    user = User.query.filter_by(facebook=profile['id']).first()
    if user:
        token = create_token(user)
        return jsonify(token=token)

    u = User(facebook=profile['id'], display_name=profile['name'], email=profile['email'])
    db.session.add(u)
    db.session.commit()
    token = create_token(u)
    return jsonify(token=token)