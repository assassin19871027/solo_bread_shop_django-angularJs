angular.module('seller.controllers', ['buy.services'])
    .controller('CtrlSellerDetail', ['$scope', 'Seller', '$rootScope',
        function($scope, Seller, $rootScope) {
            $scope.seller = Seller.query({ pk: 1 });
        }
    ])
    .controller('LoginCtrl', function($scope, $location, $auth) {
        $scope.authenticate = function(provider) {
            $auth.authenticate(provider)
                .then(function() {
                    // toastr.success('You have successfully signed in with ' + provider + '!');
                    $location.path('/');
                })
                .catch(function(error) {
                    if (error.message) {
                        // Satellizer promise reject error.
                        // toastr.error(error.message);
                    } else if (error.data) {
                        // HTTP response error from server
                        // toastr.error(error.data.message, error.status);
                    } else {
                        // toastr.error(error);
                    }
                });
        };
    });
