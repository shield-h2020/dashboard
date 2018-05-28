import angular from 'angular';
import { OnboardValidationComponent, validationState } from './onboard-validation.component';
import { OnboardValidationsListComponent, validationsListState } from './onboard-validations-list/onbard-validations-list.component';
import { OnboardValidationService } from './onboard-validation.service';
import { ViewerModule } from './viewer/viewer.module';
import { ResultsViewerModule } from './results-viewer/results-viewer.module';

export const OnboardValidationModule = angular.module('onboardValidation', ['ui.router', ViewerModule, ResultsViewerModule])
  .component('validationView', OnboardValidationComponent)
  .component('validationsListView', OnboardValidationsListComponent)
  .service('OnboardValidationService', OnboardValidationService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(validationsListState);
    $stateProvider.state(validationState);
  })
  .name;

export default OnboardValidationModule;
