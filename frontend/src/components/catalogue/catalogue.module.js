import angular from 'angular';
import { CatalogueComponent, catalogueState } from './catalogue.component';
import { CatalogueService } from './catalogue.service';

export const CatalogueModule = angular.module('catalogue', ['ui.router'])
  .component('catalogueView', CatalogueComponent)
  .service('CatalogueService', CatalogueService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(catalogueState);
  })
  .name;

export default CatalogueModule;
