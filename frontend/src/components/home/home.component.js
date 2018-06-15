import template from './home.html';

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
      this.vnsfNotificationService.connectNotificationsSocket(this.userdata.user.domain.id)
        .onmessage = (message) => {
          const data = JSON.parse(message.data);
          this.toast.error(templateNotification(data), data.event.classification, {
            onTap: () => this.openNotificationDetails(data),
            closeButton: true,
          });
        };
    }

    openNotificationDetails(data) {
      this.scope.$broadcast('NSVF_NOTIF_BROADCAST', data);
    }
  },
};

export default HomeComponent;

