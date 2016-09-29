angular.module('app.route', [
    'ngRoute',
    'common.controllers',
    // 'store.controllers',
])
.config(['$routeProvider','PATH',
    function($routeProvider, PATH) {
        $routeProvider.
        when('/', {
            templateUrl: PATH + 'common/templates/home.html',
            controller: 'CtrlHome',
        }).
        otherwise({
            redirectTo: '/error/404/'
        });
    }
]);
