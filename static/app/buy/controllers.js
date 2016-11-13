angular.module('buy.controllers', ['buy.services', 'stripe.checkout', 'rzModule'])
    .controller('CtrlBuy', function($scope, Product, $rootScope, $state, cart, toastr) {
        // geoip2.city(function(response){
        //     $scope.geoinfo = response;
        //     $scope.lat = response.location.latitude;
        //     $scope.lng = response.location.longitude;

        //     L.mapbox.accessToken = 'pk.eyJ1Ijoiam9neW4iLCJhIjoiY2lsdHpvaGUzMDBpMHY5a3MxcDMycHltZSJ9.VhDkOW21B44br30e9Td3Pg';
        //     L.mapbox.config.FORCE_HTTPS = true;
        //     $rootScope.map = L.mapbox.map('map', 'mapbox.streets', {attributionControl: false})
        //     .setView([$scope.lat, $scope.lng], 12);

        //     $scope.attribution = L.control.attribution();
        //     $scope.attribution.setPrefix('');
        //     $scope.attribution.addAttribution(
        //       '© <a href="https://www.mapbox.com/map-feedback/">Mapbox</a> \
        //        © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> \
        //        <strong><a href="https://www.mapbox.com/map-feedback/" \
        //        target="_blank">Improve this map</a></strong>');
        //     $scope.attribution.addTo($rootScope.map);

        //     var currentIcon = L.icon({
        //         iconUrl: '/static/img/pin.png',
        //         iconSize:     [50, 45], // size of the icon
        //         iconAnchor:   [13, 35], // point of the icon which will correspond to marker's location
        //         popupAnchor:  [0, -24]  // point from which the popup should open relative to the iconAnchor
        //     });

        //     var marker = L.marker([$scope.lat, $scope.lng], {icon: currentIcon}).addTo($rootScope.map); 

        // });
        
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
            toastr.success('The product is added to the cart!');
        }
    })
    .controller('CtrlProductDetail', function($scope, Product, $rootScope, cart, toastr) {
        $scope.add_cart = function(product) {
            cart.addProduct(product);
            toastr.success('The product is added to the cart!');
        }
    })
    .controller('CtrlProduct', function($scope, Product, $rootScope, toastr, $state) {
        $scope.product = {}

        $scope.$on('flow::fileAdded', function (event, $flow, flowFile) {
            $scope.product.image = flowFile.name;
        });

        // for availability
        $scope.dow = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        $scope.rangeSlider = [];

        for(var i = 0; i < $scope.dow.length; i++) {
            $scope.rangeSlider.push({ 
                minValue: 5, 
                maxValue: 21,
                title: $scope.dow[i],
                enabled: true,
                options: {
                    floor: 0,
                    disabled: false,
                    ceil: 23,
                    step: 1
                }
            });    
        }

        $scope.set_time_enable = function(slider, time_enabled) {
            slider.options.disabled = !time_enabled;
        }        

        $scope.encode_availability = function() {
            var availability = [];
            for(var i = 0; i < $scope.rangeSlider.length; i++) {
                var item = $scope.rangeSlider[i].minValue+'-'+$scope.rangeSlider[i].maxValue;
                if ($scope.rangeSlider[i].enabled) {
                    item = '1-'+item;
                } else {
                    item = '0-'+item;
                }
                availability.push(item);
            }
            return availability.join('@');
        }

        $scope.post_product = function() {
            $scope.product.availability = $scope.encode_availability();

            console.log($scope.product);
            Product.save($scope.product, function(success) {
                toastr.success('The product is saved successfully!');
                $state.go('app2.seller-profile');
            },
            function(error) {
                toastr.error('Something is wrong!');
            });
        }
    }).directive('starRating', function () {
        return {
            restrict: 'A',
            template: '<ul class="rating">' +
                '<li ng-repeat="star in stars" ng-class="star" ng-click="toggle($index)">' +
                '\u2605' +
                '</li>' +
                '</ul>',
            scope: {
                ratingValue: '=',
                max: '=',
                interactive: '='
            },
            link: function (scope, elem, attrs) {

                var updateStars = function () {
                    scope.stars = [];
                    for (var i = 0; i < scope.max; i++) {
                        scope.stars.push({
                            filled: i < scope.ratingValue
                        });
                    }
                };

                scope.toggle = function (index) {
                    if (scope.interactive)
                        scope.ratingValue = index + 1;
                };

                scope.$watch('ratingValue', function (oldVal, newVal) {
                    if (newVal) {
                        updateStars();
                    }
                });
                updateStars();
            }
        }
    });

angular.module('app')
    .controller('CtrlCart', function($scope, Product, $rootScope, cart, StripeCheckout, $log, toastr, $state, $http) {
        $scope.products = cart.getProducts();

        if ($scope.products.length == 0) {
            toastr.error('There is no item in the cart!');
            $state.go('app2.ui-products');
        }

        $scope.contact = {};
        $scope.autocomplete = new google.maps.places.Autocomplete((document.getElementById('delivery_address')), { types: ['geocode'] });

        $scope.decrease_quantity = function(product) {
            if (product.quantity -1 >= product.min_order_unit)
                product.quantity -= 1;
        }

        $scope.increase_quantity = function(product) {
            product.quantity += 1;
        }

        $scope.remove_product = function(product) {
            cart.removeProduct(product.id);
        }

        $scope.computeTotal = function() {
            var total = 0;
            for (var i = 0; i < $scope.products.length; i++) {
                total += $scope.products[i].unit_price * $scope.products[i].quantity;
            }
            return total + $scope.computeDeliveryFee();
        }

        $scope.computeDeliveryFee = function() {
            var total_fee = 0;
            for(var i = 0; i < $scope.products.length; i++) {
                total_fee += $scope.products[i].delivery_fee;
            }
            return total_fee;            
        }

        var handler = StripeCheckout.configure({
            name: "GetFreshBaked",
            token: function(token, args) {
                $log.debug("Got stripe token: " + token.id);
                $scope.contact.token = token.id;
                $scope.contact.products = $scope.products
                $http.post('/charge/', $scope.contact).then(function(res){
                    $state.go('app2.order-done', {'order': $scope.contact});                    
                },
                function(res) {
                    toastr.error("Something is wrong! Please try again!");
                });
            }
        });

        this.doCheckout = function(formValid) {
            // google autocomplete does not bind itself.
            $scope.contact.address = angular.element(delivery_address).val();

            if (formValid) {
                var options = {
                    description: "",
                    currency: "usd",
                    amount: $scope.computeTotal() * 100
                };

                handler.open(options).then(function(result) {
                    // toastr.success('Thank you for your purchase!\nYou are successfully checked out with ' + result[0].id + '!');
                }, function() {
                    toastr.error("Stripe Checkout closed without making a sale :(");
                });                
            } else {
                toastr.error("Please fill all fields in contact form!");
            }
        };
    })
    .controller('CtrlOrderDone', function($scope, cart, $stateParams, $http, toastr) {
        $scope.order = $stateParams.order;
        $scope.order = {"username": "Thmos", "phone": 234234, "token": "tok_19F95dFsevkGFSwEZh2UEB6J", "products": [{"image": "http://localhost:8000/static/media/products/2.jpg", "hashtags": null, "delivery_fee": 1.54, "order_fulfilment": null, "num_likes": 0, "id": 7, "num_orders": 0, "ingredients": "nut", "baker_logo": "/static/media/bakers/231.jpeg", "num_views": 0, "unit_price": "4.55", "min_order_unit": 12, "delivery_service": 0, "customer_rating": null, "description": "Traditional cookie", "num_shares": 0, "min_order_amount": "1.00", "name": "Trad Cookie", "baker_name": "Bear", "delivery_method": 2, "baker_id": 2, "date_created": "2016-11-12T03:42:40.666310Z", "quantity": 12}, {"image": "http://localhost:8000/static/media/products/1.jpg", "hashtags": "cok", "delivery_fee": 3.82, "order_fulfilment": null, "num_likes": 0, "id": 6, "num_orders": 0, "ingredients": "cocoa", "baker_logo": "/static/media/bakers/231.jpeg", "num_views": 0, "unit_price": "3.33", "min_order_unit": 10, "delivery_service": 0, "customer_rating": null, "description": "Nice yellow cookie", "num_shares": 0, "min_order_amount": "1.00", "name": "yellow cookie", "baker_name": "Bear", "delivery_method": 2, "baker_id": 2, "date_created": "2016-11-12T03:42:01.345606Z", "quantity": 10}], "address": "234 Huntington Avenue, Boston, MA, United States", "email": "ad@min.com"};

        for(var i=0; i < $scope.order.products.length; i++) {
            $scope.order.products[i].rate = 0;
            $scope.order.products[i].baker_rate = 0;
            $scope.order.products[i].commented = false;
            $scope.order.products[i].baker_commented = false;
        }

        $scope.product_comment = function(product, type) {
            var data = {};
            data.customer_name = $scope.order.username;
            data.customer_email = $scope.order.email;

            if (type == 1) {    // product
                data.item = product.id;
                data.text = product.comment;
                data.type = 'product';
                data.rate = product.rate;
            } else {            // baker
                data.item = product.baker_id;
                data.text = product.baker_comment;
                data.type = 'baker';
                data.rate = product.baker_rate;
            }

            console.log(data);

            $http.post('/comment/', data).then(function(res){
                if (type == 1)
                    product.commented = true;
                else 
                    product.baker_commented = true;
            },
            function(res) {
                toastr.error("Something is wrong! Please try again!");
            });
        }
    });
