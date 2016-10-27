angular.module('app')
    .config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider', '$authProvider',
        function($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $authProvider) {
            $urlRouterProvider
                .otherwise('app2/ui/products');

            $stateProvider
            // Overall
                .state('app', {
                    url: '/app',
                    templateUrl: "/static/app/app.html"
                })
                .state('app2', {
                    url: '/app2',
                    templateUrl: "/static/app/app2.html" // No app-sidebar, the rest is the same with app.html
                })
                .state('app.dashboard', {
                    url: '/dashboard',
                    templateUrl: "/static/app/dashboard/dashboard.html"
                })
                .state('app2.login', {
                    url: '/login',
                    templateUrl: '/static/app/seller/templates/login.html'
                })
                .state('app2.ui-products', {
                    url: '/ui/products',
                    templateUrl: '/static/app/buy/templates/product_list.html'
                })
                .state('app2.product-detail', {
                    url: '/ui/product/detail',
                    templateUrl: '/static/app/buy/templates/product_detail.html'
                })
                .state('app2.product-add', {
                    url: '/product/add',
                    templateUrl: '/static/app/buy/templates/product_add.html'
                })
                .state('app2.page-about', {
                    url: '/page/about',
                    templateUrl: '/static/app/page/about.html'
                })
                .state('app2.page-cart', {
                    url: '/page/cart',
                    templateUrl: '/static/app/buy/templates/cart.html'
                })
                .state('app2.seller-profile', {
                    url: '/seller/profile',
                    templateUrl: '/static/app/seller/templates/profile.html'
                })
                // eCommerce
                .state('app.ecommerce-products', {
                    url: '/ecommerce/products',
                    templateUrl: 'app/ecommerce/products.html'
                })
                .state('app.ecommerce-horizontal-products', {
                    url: '/ecommerce/horizontal-products',
                    templateUrl: 'app/ecommerce/horizontal-products.html'
                })
                .state('404', {
                    url: '/404',
                    templateUrl: "app/page-extra/404.html"
                })
                .state('500', {
                    url: '/500',
                    templateUrl: "app/page-extra/500.html"
                })
                .state('maintenance', {
                    url: '/maintenance',
                    templateUrl: "app/page-extra/maintenance.html"
                });

            $authProvider.oauth2({
                name: 'stripe',
                url: '/auth/stripe',
                clientId: 'ca_8Qcy5FPjST3HuFl7xXjisiodyjKE5d8V',
                redirectUri: window.location.origin || window.location.protocol + '//' + window.location.host,
                authorizationEndpoint: 'https://connect.stripe.com/oauth/authorize',
                scope: ['email'],
                scopeDelimiter: ',',
                display: 'popup',
                oauthType: '2.0',
                popupOptions: { width: 580, height: 400 }
            });

        }
    ]);
