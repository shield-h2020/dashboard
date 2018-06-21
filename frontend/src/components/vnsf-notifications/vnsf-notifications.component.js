import template from './vnsf-notifications.html';

const UI_STRINGS = {
  title: 'vNSF Notifications',
  tableTitle: 'vNSF notifications list',
};

const TABLE_HEADERS = {
  _id: 'Id',
  tenant_name: 'Client',
  type: 'Type',
};

export const VnsfNotificationsComponent = {
  template,
  bindings: {
    tenant: '<',
  },
  controller: class UsersListComponent {
    constructor($scope, VnsfNotificationService) {
      'ngInject';

      this.scope = $scope;
      this.vnsfNotificationService = VnsfNotificationService;
      this.viewStrings = UI_STRINGS;
      this.selectedUser = null;
      this.isCreate = true;
      this.tableHeaders = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.toggleNotificationsModal.bind(this),
          },
        ],
      };
      // Table control
      this.pagination = {
        offset: 0,
        limit: 20,
      };
      this.filters = {};
    }

    $onInit() {
      this.getNotifications();
    }

    toggleNotificationsModal(notif) {
      this.scope.$emit('NSVF_NOTIF_EMIT', JSON.parse(notif.data));
    }

    getNotifications() {
      this.loading = true;
      this.items = [];
      this.vnsfNotificationService.getNotifications(this.pagination, this.filters)
        .then((items) => {
          this.items = items;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    }
  },
};

export const vnsfNotificationListState = {
  parent: 'home',
  name: 'vnsfnotificationslist',
  url: '/vnsfnotifications',
  component: 'vnsfNotificationsListView',
  resolve: {
    tenant: ['AuthService', AuthService => AuthService.getTenantName()],
  },
};
