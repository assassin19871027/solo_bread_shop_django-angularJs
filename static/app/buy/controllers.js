angular.module('buy.controllers', ['buy.services', 'stripe.checkout'])
    .controller('CtrlBuy', ['$scope', 'Product', '$rootScope', '$state', 'cart',
        function($scope, Product, $rootScope, $state, cart) {
            $scope.products = Product.query();

            $scope.productFilterFn = function(product) {
                return $rootScope.keyword == null ||
                    $rootScope.keyword == '' ||
                    product.name.toLowerCase().indexOf($rootScope.keyword.toLowerCase()) > 0;
            }

            $scope.show_detail = function(product) {
                $rootScope.selected_product = product;
                $state.go('app2.product-detail');
            }

            $scope.add_cart = function(product) {
                cart.addProduct(product);
            }
        }
    ])
    .controller('CtrlProductDetail', ['$scope', 'Product', '$rootScope', 'cart',
        function($scope, Product, $rootScope, cart) {
            $scope.add_cart = function(product) {
                cart.addProduct(product);
            }
        }
    ]);

angular.module('app')
    .controller('CtrlCart', function($scope, Product, $rootScope, cart, StripeCheckout, $log, toastr) {
        $scope.products = cart.getProducts();

        $scope.computeTotal = function() {
            var total = 0;
            for (var i = 0; i < $scope.products.length; i++) {
                total += $scope.products[i].unit_price * $scope.products[i].quantity;
            }
            return total + $scope.computeDeliveryFee();
        }

        $scope.computeDeliveryFee = function() {
            // var total_fee = 0;
            // for(var i = 0; i < $scope.products.length; i++) {
            //     total_fee += $scope.products[i].delivery_fee;
            // }
            // return total_fee;            
            return 5.99;
        }

        var handler = StripeCheckout.configure({
            name: "GetFreshBaked",
            token: function(token, args) {
                $log.debug("Got stripe token: " + token.id);
            }
        });

        this.doCheckout = function(token, args) {
            var options = {
                description: "",
                amount: $scope.computeTotal() * 100
            };

            handler.open(options)
                .then(function(result) {
                    toastr.success('Thank you for your purchase!\nYou are successfully checked out with ' + result[0].id + '!');
                }, function() {
                    alert("Stripe Checkout closed without making a sale :(");
                });
        };
    });
