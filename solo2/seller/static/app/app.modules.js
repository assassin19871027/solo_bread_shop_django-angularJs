var app = angular.module('app.main', [
    'ngAnimate',
    'ngSanitize',
    'ngAria',
    'ngCookies',
    'ngTouch',
    'ui.bootstrap',
    // 'asyncload.services',
    // 'pascalprecht.translate',
    'constants',
    'app.route',
    // 'auth.services',
    // 'navbar',
    // 'footer',
    // 'alert',
    // 'selfie',
    // 'grid',
    // 'common.directives',
]);
app.run(function($rootScope) {
    $rootScope.site = 'Solo2';
    $rootScope.PATH = 'app/';
    $rootScope.alerts = [];
    $rootScope.app = {
        navbarHeaderColor: 'bg-black',
        navbarCollapseColor: 'bg-white-only',
        asideColor: 'bg-black',
        headerFixed: true,
        asideFixed: false,
        asideFolded: false,
        asideDock: false,
        hideAside: false,
        container: false
    };
});
