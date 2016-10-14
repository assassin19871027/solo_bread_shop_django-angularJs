
angular.module('app')
    .config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider',

        function($stateProvider, $urlRouterProvider, $ocLazyLoadProvider) {
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

                // Home
                .state('app.dashboard', {
                    url: '/dashboard',
                    templateUrl: "/static/app/dashboard/dashboard.html"
                })

                .state('app2.ui-products', {
                    url: '/ui/products',
                    templateUrl: '/static/app/buy/templates/product_list.html'
                })
                .state('app2.product-detail', {
                    url: '/ui/product/detail',
                    templateUrl: '/static/app/buy/templates/product_detail.html'
                })
                .state('app2.page-about', {
                    url: '/page/about',
                    templateUrl: '/static/app/page/about.html'
                })
                .state('app2.page-cart', {
                    url: '/page/cart',
                    templateUrl: '/static/app/buy/templates/cart.html'
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
                .state('app.ecommerce-invoice', {
                    url: '/ecommerce/invoice',
                    templateUrl: 'app/ecommerce/invoice.html'
                })

                // Extra
                .state('404', {
                    url: '/404',
                    templateUrl: "app/page-extra/404.html"
                })
                .state('500', {
                    url: '/500',
                    templateUrl: "app/page-extra/500.html"
                })
                .state('signin', {
                    url: '/signin',
                    templateUrl: 'app/page-extra/signin.html'
                })
                .state('signup', {
                    url: '/signup',
                    templateUrl: 'app/page-extra/signup.html'
                })
                .state('forgot-password', {
                    url: '/forgot-password',
                    templateUrl: 'app/page-extra/forgot-password.html'
                })
                .state('confirm-email', {
                    url: '/confirm-email',
                    templateUrl: 'app/page-extra/confirm-email.html'
                })
                .state('lock-screen', {
                    url: '/lock-screen',
                    templateUrl: 'app/page-extra/lock-screen.html'
                })
                .state('maintenance', {
                    url: '/maintenance',
                    templateUrl: "app/page-extra/maintenance.html"
                })
            ;
        }
    ]);