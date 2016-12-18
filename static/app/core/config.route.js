angular.module('app')
    .config(function($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $authProvider, StripeCheckoutProvider, flowFactoryProvider) {
        $urlRouterProvider
            .otherwise('app2/ui/products');

        $stateProvider
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
                templateUrl: '/static/app/buy/templates/product_add.html',
                data: { requiredLogin: true }
            })
            .state('app2.seller-add', {
                url: '/seller/add',
                templateUrl: '/static/app/seller/templates/seller_add.html'
            })
            .state('app2.page-about', {
                url: '/page/about',
                templateUrl: '/static/app/page/about.html'
            })
            .state('app2.page-cart', {
                url: '/page/cart',
                templateUrl: '/static/app/buy/templates/cart.html',
                resolve: {
                    stripe: StripeCheckoutProvider.load
                }
            })
            .state('app2.seller-profile', {
                url: '/seller/profile',
                templateUrl: '/static/app/seller/templates/profile.html',
                data: { requiredLogin: false },
                params: { pk: 2 }
            })
            .state('app2.order-done', {
                url: '/order/done',
                templateUrl: '/static/app/buy/templates/order_done.html',
                params: { order: null }
            })
            .state('app2.seller-availability', {
                url: '/seller/availability',
                templateUrl: '/static/app/seller/templates/availability.html',
                data: { requiredLogin: true }
            })
            .state('404', {
                url: '/404',
                templateUrl: "/static/app/page-extra/404.html"
            })
            .state('500', {
                url: '/500',
                templateUrl: "/static/app/page-extra/500.html"
            })
            .state('maintenance', {
                url: '/maintenance',
                templateUrl: "/static/app/page-extra/maintenance.html"
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

        StripeCheckoutProvider.defaults({
            key: "pk_test_Q4RGBzPFhWbMP2daCqMg6Rj7"
        });

        flowFactoryProvider.defaults = {
            target: 'upload_product_photo',
            permanentErrors: [404, 500, 501],
            maxChunkRetries: 1,
            chunkRetryInterval: 5000,
            simultaneousUploads: 4,
            singleFile: true,
            testChunks: false
        };

        flowFactoryProvider.on('catchAll', function(event) {
            // console.log('catchAll', arguments);
        });
    }).run(function($rootScope, $state, $auth, $mdSidenav) {
        $rootScope.$on('$stateChangeStart',
            function(event, toState) {
                $mdSidenav('right').close();
                var requiredLogin = false;
                if (toState.data && toState.data.requiredLogin)
                    requiredLogin = true;

                if (requiredLogin && !$auth.isAuthenticated()) {
                    event.preventDefault();
                    $state.go('app2.login');
                }
            });
    });;
