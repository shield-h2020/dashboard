import angular from 'angular';
import { TableComponent } from './table.component';

export const TableModule = angular.module('table', [])
  .component('snTable', TableComponent)
  .name;

export default TableModule;
