import angular from 'angular';
import { AttestationState, AttestationComponent } from './attestation.component';
import { AttestationService } from './attestation.service';

export const AttestationModule = angular.module('attestation', ['ui.router'])
  .component('attestationView', AttestationComponent)
  .service('AttestationService', AttestationService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(AttestationState);
  })
  .name;

export default AttestationModule;
