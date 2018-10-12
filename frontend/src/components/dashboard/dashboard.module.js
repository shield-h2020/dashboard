import angular from 'angular';
import { DashboardComponent, DashboardState } from './dashboard.component';
import { DashboardService } from './dashboard.service';
import { DonutLabelsChartDirective } from '../charts/donut-labels-chart.directive';
import { LinesChartDirective } from '../charts/lines-chart.directive';
import { BarChartDirective } from '../charts/bar-chart.directive';

export const DashboardModule = angular.module('dashboard', ['ui.router'])
  .component('dashboardView', DashboardComponent)
  .service('DashboardService', DashboardService)
  .directive('linesChart', ['$timeout', '$compile', LinesChartDirective])
  .directive('donutLabelsChart', ['$timeout', '$compile', DonutLabelsChartDirective])
  .directive('barChart', ['$timeout', '$compile', BarChartDirective])
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(DashboardState);
  })
  .name;

export default DashboardModule;
