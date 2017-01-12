angular.module('seller.controllers', ['seller.services', 'rzModule'])
    .controller('CtrlSellerDetail', function($scope, Seller, $state, $rootScope, $stateParams) {
        $scope.seller = Seller.query({ pk: $stateParams.pk });
    })
    .controller('LoginCtrl', function($scope, $location, $auth, toastr, $rootScope) {
        $scope.authenticate = function(provider) {
            $auth.authenticate(provider)
            .then(function() {
                $rootScope.loggedin = true;
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
    })
    .controller('CtrlSeller', function($scope, Seller, $http, $state, toastr) {

        $scope.seller = {}

        $scope.$on('flow::fileAdded', function (event, $flow, flowFile) {
            $scope.seller.logo = flowFile.name;
        });

        $scope.post_seller = function(seller) {
            //$scope.seller.availability = $scope.encode_availability();
            console.log($scope.seller);
            console.log("ok data");
            Seller.save($scope.seller, function(success) {
                toastr.success('The seller is saved successfully!');
                $state.go('app2.seller-profile');
            },
            function(error) {
                toastr.error('Something is wrong!');
            });
        }
    });


angular.module('app')
    .controller('CtrlSellerAvailability', function($scope,Seller, Product, $rootScope, cart, StripeCheckout, $log, toastr) {
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
