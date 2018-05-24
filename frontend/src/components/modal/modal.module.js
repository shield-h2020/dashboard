import angular from 'angular';
import { ModalComponent } from './modal.component';

export const ModalModule = angular.module('modal', [])
  .component('snModal', ModalComponent)
  .name;

export default ModalModule;
