angular.module('buy.controllers', ['buy.services'])
.controller('CtrlBuy', ['$scope', 'Product', '$rootScope', '$state', 'cart',
    function($scope, Product, $rootScope, $state, cart) {
        $scope.products = Product.query();

        $scope.productFilterFn = function (product) {
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
])
.controller('CtrlCart', ['$scope', 'Product', '$rootScope', 'cart',
    function($scope, Product, $rootScope, cart) {
        $scope.products = cart.getProducts();

        $scope.computeTotal = function() {
            var total = 0;
            for(var i = 0; i < $scope.products.length; i++) {
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
            return 5;
        }
    }
]);
