import angular from 'angular';
import { IncidentsListComponent, IncidentsListState } from './incidents-list.component';
import { IncidentsModalComponent } from './incidents-modal/incidents-modal.component';
import { IncidentsService } from './incidents.service';
import prettyXml from 'angular-pretty-xml';

export const IncidentsModule = angular.module('incidents', ['ui.router', 'prettyXml'])
  .component('incidentsListView', IncidentsListComponent)
  .component('incidentsModal', IncidentsModalComponent)
  .service('IncidentsService', IncidentsService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(IncidentsListState);
  })
    .name;

export default IncidentsModule;
