import angular from 'angular';
import { ModalDirective } from './modal.directive';

export const ModalModule = angular.module('modal', [])
  .directive('snModal', ['$compile', ModalDirective])
  .name;

export default ModalModule;
