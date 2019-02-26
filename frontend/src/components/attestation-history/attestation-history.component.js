import template from './attestation-history.html';
import styles from './attestation-history.scss';

const VIEW_STRING = {
  title: 'Attestation History',
  tableTitle: 'Attestation History',
  back: 'Back',
};

const TABLE_HEADERS_TM = {
  type: 'Type',
  node: 'Node',
  driver: 'Driver',
  trust: 'Trusted',
  status: 'Recommendation',
  time: 'Time',
};

const TABLE_HEADERS_VNSF = {
  vnsf_name: 'VNSF Name',
  trust: 'Trusted',
  status: 'Recommendation',
  time: 'Time',
};

export const AttestationHistoryComponent = {
  template,
  bindings: {
    tenant: '<',
  },
  controller: class AttestationHistoryComponent {
    constructor($stateParams, $state, $scope, AttestationHistoryService, AuthService) {
      'ngInject';

      this.viewStrings = VIEW_STRING;
      this.nodeName = $stateParams.node;
      this.scope = $scope;
      this.state = $state;
      this.type = $stateParams.type;
      this.styles = styles;
      this.attestationHistoryService = AttestationHistoryService;
      this.authService = AuthService;
      this.pagination = {
        page: 1,
        limit: 1,
        pageLimit: 10,
      };
    }

    $onInit() {
      this.scope.$on('MODAL_EVENT_BROADCAST', (event,data) => {
        if (data.message === 'apply') {
          this.getNotifications();
        }
      });
      this.items = [];
      this.scope.$on('ATTESTATION_UPDATE_DATA', (event, data) => {
        if (this.authService.isUserTenantAdmin()) {
          this.filters = { tenant_id: this.authService.getTenant(), 'vnsfs.vnsfd_id': this.nodeName };
          this.getNotifications();
        } else {
          this.selected_type = this.typeList[0].type_id;
          this.selected_name = this.typeList[0].type_name;

          this.items = [];
          this.typeList.forEach((element) => {
            if (element.type_id !== 0) {
              this.getNotifications();
            }
          });
        }
      });

      if (this.authService.isUserTenantAdmin()) {
        this.filters = { tenant_id: this.authService.getTenant(), 'vnsfs.vnsfd_id': this.nodeName };
        this.getNotifications();

        this.tableHeaders = {
          ...TABLE_HEADERS_VNSF,
          actions: [
            {
              label: 'View',
              action: this.toggleNotificationsModal.bind(this),
            },
          ],
        };
      } else {
        if (this.type === 'hosts') {
          this.filters = { 'hosts.node': this.nodeName };
          this.getNotifications();
        } else {
          this.filters = { 'sdn.node': this.nodeName };
          this.getNotifications();
        }
        this.tableHeaders = {
          ...TABLE_HEADERS_TM,
          actions: [
            {
              label: 'View',
              action: this.toggleNotificationsModal.bind(this),
            },
          ],
        };
      }
      this.loading = false;
    }

    toggleNotificationsModal(notif) {
      this.scope.$emit('ATTESTATION_NOTIF_EMIT', notif);
    }

    getNotifications() {
      let typeNotification;
      this.attestationHistoryService.getNotifications(this.pagination, this.filters)
        .then((result) => {
          if (this.selected_type !== 0) {
            this.items = [];
          }
          if (this.authService.isUserTenantAdmin()) {
            this.items = [];
            result.notifs.forEach((item) => {
              item.vnsfs.forEach((vnsfsitem) => {
                if (vnsfsitem.vnsfd_id === this.nodeName) {
                  this.items.push({
                    _id: item._id,
                    vnsf_id: vnsfsitem.vnsfr_id,
                    vnsf_name: vnsfsitem.vnsfd_id,
                    remediation: vnsfsitem.remediation,
                    trust: vnsfsitem.trust,
                    ns_id: vnsfsitem.ns_id,
                    time: item.time,
                    status: item.status,
                    tenant_id: item.tenant_id,
                    _etag: item._etag,
                  });
                }
              });
            });
          } else {
            result.notifs.forEach((item) => {
              typeNotification = item.type;
              if (this.selected_type === 0) {
                const itemsResult = item[typeNotification].map((typeitem) => {
                  return {
                    _id: item._id,
                    type: item.type,
                    driver: typeitem.driver,
                    node: typeitem.node,
                    extrainfo: typeitem.extra_info,
                    remediation: typeitem.remediation,
                    trust: typeitem.trust,
                    status: item.status,
                    time: item.time,
                  };
                });
                this.items = this.items.concat(itemsResult);
              } else {
                item[typeNotification].forEach((typeitem) => {
                  let timeValue = '';
                  if (typeitem.time) {
                    timeValue = typeitem.time;
                  } else {
                    timeValue = typeitem.extra_info.Time;
                  }
                  this.items.push({
                    _id: item._id,
                    type: item.type,
                    driver: typeitem.driver,
                    node: typeitem.node,
                    extrainfo: typeitem.extra_info,
                    remediation: typeitem.remediation,
                    trust: typeitem.trust,
                    status: item.status,
                    time: timeValue,
                    _etag: item._etag,
                  });
                });
              }
            });
          }
          this.pagination.total = (result && result.meta.total) || 0;
          this.paging = this.calcPageItems();
        });
    }

    changePage(amount) {
      const condition = amount > 0 ?
        this.items.length >= this.pagination.pageLimit : this.pagination.page > 1;
      if (condition) {
        this.pagination.page += amount;
        this.getNotifications();
      }
    }

    calcPageItems() {
      const { page, pageLimit } = this.pagination;
      const length = this.items.length || 10;

      const res = ((page * pageLimit) - (length < pageLimit ? pageLimit : length)) + 1;
      const res2 = (page * pageLimit) + (length < pageLimit ? -(pageLimit - length) : 0);

      return { min: res, max: res2 };
    }
  },
};

export const AttestationHistoryState = {
  parent: 'home',
  name: 'history',
  url: '/history/{node}/{type}',
  component: 'attestationHistoryView',
};
