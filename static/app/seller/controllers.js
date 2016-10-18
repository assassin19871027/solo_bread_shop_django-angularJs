angular.module('seller.controllers', ['buy.services'])
.controller('CtrlSellerDetail', ['$scope', 'Seller', '$rootScope',
    function($scope, Seller, $rootScope) {
        $scope.seller = Seller.query({pk: 1});
    }
]);
