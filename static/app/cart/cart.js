angular.module("cart", [])
    .factory("cart", function() {
        var cartData = [];
        return {
            addProduct: function(product) {
                var addedToExistingItem = false;
                for (var i = 0; i < cartData.length; i++) {
                    if (cartData[i].id == product.id) {
                        // cartData[i].count++;
                        addedToExistingItem = true;
                        break;
                    }
                }
                if (!addedToExistingItem) {
                    product.quantity = product.min_order_unit;
                    product.delivery_fee = (Math.random() * 5).toFixed(2) * 1;
                    cartData.push(product);
                }
            },
            removeProduct: function(id) {
                for (var i = 0; i < cartData.length; i++) {
                    if (cartData[i].id == id) {
                        cartData.splice(i, 1);
                        break;
                    }
                }
            },
            getProducts: function() {
                return cartData;
            }
        }
    })
    .directive("cartSummary", function(cart) {
        return {
            restrict: "E",
            templateUrl: "components/cart/cartSummary.html",
            controller: function($scope) {
                var cartData = cart.getProducts();
                $scope.total = function() {
                    var total = 0;
                    for (var i = 0; i < cartData.length; i++) {
                        total += (cartData[i].price * cartData[i].count);
                    }
                    return total;
                }
                $scope.itemCount = function() {
                    var total = 0;
                    for (var i = 0; i < cartData.length; i++) {
                        total += cartData[i].count;
                    }
                    return total;
                }
            }
        };
    });;
