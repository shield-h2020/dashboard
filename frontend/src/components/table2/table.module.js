import angular from 'angular';
import { TableComponent } from './table.component';
import { ColorCellDirective } from './color-cell.directive';

export const TableModule = angular.module('table2', [])
  .component('sTable', TableComponent)
  .directive('colorCell', ['$timeout', '$compile', ColorCellDirective])
  .name;

export default TableModule;
