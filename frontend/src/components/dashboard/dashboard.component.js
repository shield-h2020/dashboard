import template from './dashboard.html';

const VIEW_STRING = {
  title: 'Le Dashboard',
};

export const DashboardComponent = {
    template,
    bindings: {
      tenant: '<',
    },
    controller: class DashboardComponent {
      constructor($stateParams, $state, $scope) {
        'ngInject';
        
        this.viewStrings = VIEW_STRING;
      }

      $onInit() {
          
      }
    },
};


export const DashboardState = {
    parent: 'home',
    name: 'dashboard',
    url: '/dashboard',
    component: 'dashboardView',
};