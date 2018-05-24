import angular from 'angular';
import { TenantsListComponent, TenantsListState } from './tenants-list/tenants-list.component';
import { TenantsService } from './tenants.service';

export const TenantsModule = angular.module('tenants', ['ui.router'])
  .component('tenantsListView', TenantsListComponent)
  .service('TenantsService', TenantsService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(TenantsListState);
  })
  .name;

export default TenantsModule;
