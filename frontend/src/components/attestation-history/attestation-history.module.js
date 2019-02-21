import angular from 'angular';
import { AttestationHistoryState, AttestationHistoryComponent } from './attestation-history.component';
import { AttestationModalComponent } from './attestation-modal/attestation-modal.component';
import { AttestationHistoryService } from './attestation-history.service';

export const AttestationHistoryModule = angular.module('attestation-history', ['ui.router'])
  .component('attestationHistoryView', AttestationHistoryComponent)
  .component('attestationModal', AttestationModalComponent)
  .service('AttestationHistoryService', AttestationHistoryService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(AttestationHistoryState);
  })
  .name;

export default AttestationHistoryModule;
