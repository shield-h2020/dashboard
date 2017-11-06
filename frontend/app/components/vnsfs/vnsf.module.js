import angular from 'angular';
import { VNSFListComponent, vnsfListState } from './vnsflist.component';
import { VNSFService } from './vnsf.service';

export const VNSFModule = angular.module('vnsf', ['ui.router'])
  .component('vnsfsListView', VNSFListComponent)
  .service('VNSFService', VNSFService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(vnsfListState);
  })
    .name;

export default VNSFModule;
