import angular from 'angular';
import { TableCustomActionsComponent } from './table-custom-actions.component';
import { ColorCellDirective } from '../table2/color-cell.directive';

export const TableCustomActionsModule = angular.module('tablecustomactions', [])
  .component('tableCustomActions', TableCustomActionsComponent)
  .directive('colorCell', ['$timeout', '$compile', ColorCellDirective])
  .name;

export default TableCustomActionsModule;
