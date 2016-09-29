angular.module('common.controllers', [ 'ngCookies'])
.controller('CtrlHome', ['$scope', '$rootScope','$http', '$cookies',
'$location', '$route', '$window',
    function($scope, $rootScope, $http, $cookies, $location, $route, $window) {

        $rootScope.title = 'The First Page';

    }
]);
