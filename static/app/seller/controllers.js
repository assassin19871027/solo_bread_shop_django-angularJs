angular.module('seller.controllers', ['buy.services'])
    .controller('CtrlSellerDetail', ['$scope', 'Seller', '$rootScope',
        function($scope, Seller, $rootScope) {
            $scope.seller = Seller.query({ pk: 1 });
        }
    ])
    .controller('LoginCtrl', function($scope, $location, $auth, toastr) {
        $scope.authenticate = function(provider) {
            $auth.authenticate(provider)
                .then(function() {
                    toastr.success('You have successfully signed in with ' + provider + '!');
                    $location.path('/app2/seller/profile');
                })
                .catch(function(error) {
                    if (error.message) {
                        // Satellizer promise reject error.
                        toastr.error(error.message);
                    } else if (error.data) {
                        // HTTP response error from server
                        toastr.error(error.data.message, error.status);
                    } else {
                        toastr.error(error);
                    }
                });
        };
    });

angular.module('app')
    .controller('CtrlSellerAvailability', function($scope, Product, $rootScope, cart, StripeCheckout, $log, toastr) {
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
    });