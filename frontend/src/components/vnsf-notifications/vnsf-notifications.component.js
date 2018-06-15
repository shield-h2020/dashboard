import template from './vnsf-notifications.html';

const UI_STRINGS = {
  title: 'VNSF Notifications',
  tableTitle: 'VNSF notifications list',
};

const TABLE_HEADERS = {
  _id: 'Id',
  tenant: 'Tenant',
  type: 'Type',
};

export const VnsfNotificationsComponent = {
  template,
  bindings: {
    tenant: '<',
  },
  controller: class UsersListComponent {
    constructor(VnsfNotificationService) {
      'ngInject';

      this.vnsfNotificationService = VnsfNotificationService;
      this.viewStrings = UI_STRINGS;
      this.selectedUser = null;
      this.isCreate = true;
      this.tableHeaders = {
        ...TABLE_HEADERS,
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
