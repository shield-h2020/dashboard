import angular from 'angular';
import { NSListComponent, nsListState } from './nslist.component';
import { NSService } from './ns.service';

export const NSModule = angular.module('ns', ['ui.router'])
  .component('nssListView', NSListComponent)
  .service('NSService', NSService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(nsListState);
  })
    .name;

export default NSModule;
