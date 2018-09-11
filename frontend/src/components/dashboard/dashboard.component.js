import template from './dashboard.html';
import { PIE_DATA_EVENT } from './dash-viewer/dash-event-strings';

const VIEW_STRING = {
  title: 'Le Dashboard',
};

export const DashboardComponent = {
    template,
    bindings: {
      tenant: '<',
    },
    controller: class DashboardComponent {
      constructor($stateParams, $state, $scope, DashboardService) {
        'ngInject';
        
        this.viewStrings = VIEW_STRING;
        this.dashboardService = DashboardService;
        this.scope = $scope;
      }

      $onInit() {
          
        this.dashboardService.getTotalAttacks()
          .then((data) => {

            this.scope.$emit(PIE_DATA_EVENT.EMIT, { data });

            this.dashboardService.getTotalAttacksByDay()
              .then((data2) => {
                console.log(data2);
                
              });
          });
      }



    },
};

export const DashboardState = {
    parent: 'home',
    name: 'dashboard',
    url: '/dashboard',
    component: 'dashboardView',
};