import angular from 'angular';
import { VnsfNotificationsComponent, vnsfNotificationListState } from './vnsf-notifications.component';
import { VnsfNotificationService } from './vnsfnotification.service';
import { VnsfNotificationsModalComponent } from './vnsf-notifications-modal/vnsf-notifications-modal.component';

export const VnsfNotificationsModule = angular.module('vnsfsnotifications', ['ui.router'])
  .component('vnsfNotificationsListView', VnsfNotificationsComponent)
  .component('vnsfNotificationsModal', VnsfNotificationsModalComponent)
  .service('VnsfNotificationService', VnsfNotificationService)
  .config(($stateProvider) => {
    'ngInject';

    $stateProvider.state(vnsfNotificationListState);
  })
  .name;

export default VnsfNotificationsModule;
