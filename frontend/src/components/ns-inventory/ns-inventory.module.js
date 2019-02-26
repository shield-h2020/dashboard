import angular from 'angular';
import { InventoryComponent, inventoryState } from './ns-inventory.component';
import { InventoryService } from './ns-inventory.service';

export const NsInventoryModule = angular
  .module('inventory', ['ui.router'])
  .component('inventoryView', InventoryComponent)
  .service('InventoryService', InventoryService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(inventoryState);
  })
  .name;

export default NsInventoryModule;
