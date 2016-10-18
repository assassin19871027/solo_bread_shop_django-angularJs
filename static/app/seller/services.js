angular.module('seller.services', ['ngResource'])
    .factory('Seller', ['$resource', 
        function ($resource) {
            return $resource('/bakers/:pk/:action/', {}, {
                query: {method: 'GET', params: {action: null}, responseType: 'json'},
                save: {method: 'POST'},
                update: {method: 'PATCH'},
                remove: {method: 'DELETE'},
            });
        }])