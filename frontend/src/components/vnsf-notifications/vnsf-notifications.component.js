import template from './vnsf-notifications.html';

const VIEW_STRINGS = {
  title: 'vNSF Notifications',
  tableTitle: 'vNSF notifications list',
  confirmDelete: 'Are you sure you want to delete the notification ',
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
      this.viewStrings = VIEW_STRINGS;
      this.selectedNotif = null;
      this.isCreate = true;
      this.tableHeaders = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.toggleNotificationsModal.bind(this),
          },
          {
            label: 'delete',
            action: this.toggleDeleteModal.bind(this),
          },
        ],
      };
      // Table control
      this.pagination = {
        offset: 0,
        limit: 20,
      };
      this.filters = {};
      this.deleteModalOpen = false;
    }

    $onInit() {
      this.getNotifications();
    }

    toggleDeleteModal(notif) {
      this.selectedNotif = notif;
      this.deleteModalOpen = !this.deleteModalOpen;
    }

    deleteNotification() {
      this.vnsfNotificationService.deleteNotification(this.selectedNotif)
        .then(() => {
          this.toggleDeleteModal();
          this.getNotifications();
        });
    }

    toggleNotificationsModal(notif) {
      console.log(notif);
      if(notif.type === 'TRUST_MONITOR')
        this.scope.$emit('TM_NOTIF_EMIT', JSON.parse(notif.data));
      else
        this.scope.$emit('NSVF_NOTIF_EMIT', JSON.parse(notif.data));
    }

    static addExtraClasses(items) {
      return items.map(item => ({
        ...item,
        cellClasses: {
          tenant_name: item.tenant_name === 'not found' ? 'cell--unimportant' : '',
        },
      }));
    }

    getNotifications() {
      this.loading = true;
      this.items = [];
      this.vnsfNotificationService.getNotifications(this.pagination, this.filters)
        .then((items) => {
          this.items = UsersListComponent.addExtraClasses(items);
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
