angular.module('app').controller('AppSidenavRightCtrl', function($scope, $auth, $state, $mdSidenav, $rootScope) {
    $scope.logout = function() {
        $rootScope.loggedin = false;
        $auth.logout();
        $mdSidenav('right').toggle();
        $state.go('app2.ui-products');
    }
}); 