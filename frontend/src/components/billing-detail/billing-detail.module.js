import angular from 'angular';
import { BillingDetailComponent, BillingDetailState } from './billing-detail.component';
import { BillingDetailService } from './billing-detail.service';

export const BillingDetailModule = angular.module('billing-detail', ['ui.router'])
  .component('billingDetailView', BillingDetailComponent)
  .service('BillingDetailService', BillingDetailService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(BillingDetailState);
  })
  .name;

export default BillingDetailModule;
