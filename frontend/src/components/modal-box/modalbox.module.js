import angular from 'angular';
import { ModalBoxComponent } from './modalbox.component';
import { EditModalBoxComponent } from './editmodalbox.component';
import { ErrorModalBoxComponent } from './internal-error/internal-error.component';

export const ModalBoxModule = angular.module('modalbox', [])
  .component('snModal', ModalBoxComponent)
  .component('snEditModal', EditModalBoxComponent)
  .component('errorModal', ErrorModalBoxComponent)
  .name;

export default ModalBoxModule;
