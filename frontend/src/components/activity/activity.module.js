import angular from 'angular';
import { ActivityComponent, activityState } from './activity.component';
import { ActivityService } from './activity.service';

export const ActivityModule = angular.module('activity', ['ui.router'])
  .component('activityView', ActivityComponent)
  .service('ActivityService', ActivityService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider
      .state(activityState);
  })
  .name;

export default ActivityModule;
