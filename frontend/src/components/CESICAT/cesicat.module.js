import angular from 'angular';
import { CESICATComponent, CESICATState } from './cesicat.component';
import { CESICATService } from './cesicat.service';
import { lineChartDataMaliciousDirective } from '../charts/line-chart-malicious.directive';
import { DoubleLinesChartDirective } from '../charts/double-line-chart.directive';

export const CESICATModule = angular.module('cesicat', ['ui.router'])
  .component('cesicatView', CESICATComponent)
  .service('CESICATService', CESICATService)
  .directive('linesChartMalicious', ['$timeout', '$compile', lineChartDataMaliciousDirective])
  .directive('doubleLineChart', ['$timeout', '$compile', DoubleLinesChartDirective])
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(CESICATState);
  })
  .name;

export default CESICATModule;
