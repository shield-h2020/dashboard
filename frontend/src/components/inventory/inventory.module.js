import angular from 'angular';
import { InventoryComponent, inventoryState } from './inventory.component';
import { InventoryService } from './inventory.service';

export const InventoryModule = angular.module('inventory', ['ui.router'])
  .component('inventoryView', InventoryComponent)
  .service('InventoryService', InventoryService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(inventoryState);
  })
  .name;

export default InventoryModule;
