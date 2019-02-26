import angular from 'angular';
import { BillingComponent, BillingState } from './billing.component';
import { BillingService } from './billing.service';

export const BillingModule = angular.module('billing', ['ui.router'])
  .component('billingView', BillingComponent)
  .service('BillingService', BillingService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(BillingState);
  })
  .name;

export default BillingModule;
