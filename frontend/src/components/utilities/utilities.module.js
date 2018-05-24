import angular from 'angular';
import { AutoResizerDirective } from './auto-resizer.directive';
import { CollapsibleDirective } from './collapsible.directive';

export const UtilitiesModule = angular.module('utilities', [])
  .directive('autoResizer', ['$window', AutoResizerDirective])
  .directive('collapsible', CollapsibleDirective)
  .name;

export default UtilitiesModule;
