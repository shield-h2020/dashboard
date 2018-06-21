import template from './home.html';
import { TENANT_ADMIN, TENANT_USER } from '@/strings/role-strings.js';

function templateNotification(data) {
  return `
    source: ${data.event['source-ip']}
    target: ${data.event['destination-ip']}
  `;
}

export const HomeComponent = {

  template,
  bindings: {
    userdata: '<',
  },
  controller: class HomeComponent {
    constructor($scope, toastr, VnsfNotificationService) {
      'ngInject';

      this.scope = $scope;
      this.toast = toastr;
      this.vnsfNotificationService = VnsfNotificationService;
    }

    $onInit() {
      if (this.userdata.roles.find(r => r.name === TENANT_ADMIN || r.name === TENANT_USER)) {
        this.vnsfNotificationService.connectNotificationsSocket(this.userdata.user.domain.id)
        .onmessage = (message) => {
          const data = JSON.parse(message.data);
          this.toast.error(templateNotification(data), data.event.classification, {
            onTap: () => this.openNotificationDetails(data),
            closeButton: true,
          });
        };
      }

      this.scope.$on('NSVF_NOTIF_EMIT', (event, data) => {
        this.openNotificationDetails(data);
      });
    }

    openNotificationDetails(data) {
      this.scope.$broadcast('NSVF_NOTIF_BROADCAST', data);
    }
  },
};

export default HomeComponent;

