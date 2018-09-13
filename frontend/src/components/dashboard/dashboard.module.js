import angular from 'angular';
import { DashboardComponent, DashboardState } from './dashboard.component';
import { DashboardService } from './dashboard.service';
import { DashViewerModule } from './dash-viewer/dash-viewer.module';

export const DashboardModule = angular.module('dashboard', ['ui.router', DashViewerModule])
  .component('dashboardView', DashboardComponent)
  .service('DashboardService', DashboardService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(DashboardState);
  })
  .name;

export default DashboardModule;
