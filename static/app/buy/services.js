angular.module('buy.services', ['ngResource'])
    .factory('Product', ['$resource', 
        function ($resource) {
            return $resource('/products/:pk/:action/', {}, {
                query: {method: 'GET', params: {action: null}, responseType: 'json'},
                save: {method: 'POST'},
                update: {method: 'PATCH'},
                remove: {method: 'DELETE'},
                detail: {method: 'GET', params: {action: null}, responseType: 'json'},
            });
        }])