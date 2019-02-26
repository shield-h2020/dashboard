import template from './vnsf-notifications.html';
import styles from './vnsf-notifications.scss';

const VIEW_STRINGS = {
  title: 'vNSF Notifications',
  tableTitle: 'vNSF notifications list',
  confirmDelete: 'Are you sure you want to delete the notification ',
};

const TABLE_HEADERS = {
  type: 'Type',
  tenant_name: 'Client',
  classification: 'Classification',
  _created: 'Date',
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
      this.styles = styles;

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
        page: 1,
        offset: 0,
        limit: 10,
      };
      this.filters = {};
      this.deleteModalOpen = false;
    }

    $onInit() {
      this.scope.$on('TM_UPDATE_BROADCAST', () => {
        this.getNotifications();
      });
      this.scope.$on('VNSF_UPDATE_BROADCAST', () => {
        this.getNotifications();
      });

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
      if (notif.type === 'TRUST_MONITOR') {
        this.scope.$emit('TM_NOTIF_EMIT', JSON.parse(notif.data));
      } else {
        this.scope.$emit('NSVF_NOTIF_EMIT', JSON.parse(notif.data));
      }
    }

    static addExtraClasses(items) {
      return items.values.map(item => ({
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
          this.pagination.total = (items && items.meta.total) || 0;
          this.paging = this.calcPageItems();
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    }

    changePage(amount) {
      const condition = amount > 0 ?
        this.items.length >= this.pagination.limit : this.pagination.page > 1;
      if (condition) {
        this.pagination.page += amount;
        this.getNotifications();
      }
    }

    calcPageItems() {
      const { page, limit } = this.pagination;
      const length = this.items.length || 10;

      const res = ((page * limit) - (length < limit ? limit : length)) + 1;
      const res2 = (page * limit) + (length < limit ? -(limit - length) : 0);

      return { min: res, max: res2 };
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
