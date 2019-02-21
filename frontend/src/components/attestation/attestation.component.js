import template from './attestation.html';
import styles from './attestation.scss';

const VIEW_STRING = {
  title: 'Attestation',
  tableTitle: 'Attestation',
  attestationAll: 'Attest NFV Infrastructure',
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

export const AttestationComponent = {
  template,
  bindings: {
    tenant: '<',
  },
  controller: class AttestationComponent {
    constructor($stateParams, $state, toastr, $scope, AttestationService, AuthService) {
      'ngInject';

      this.viewStrings = VIEW_STRING;
      this.scope = $scope;
      this.state = $state;
      this.styles = styles;
      this.toast = toastr;
      this.attestationService = AttestationService;
      this.authService = AuthService;
      this.pagination = {
        page: 1,
        limit: 1,
        pageLimit: 10,
      };
    }

    $onInit() {
      this.items = [];
      this.scope.$on('ATTESTATION_UPDATE_DATA', () => {
        if (this.authService.isUserTenantAdmin()) {
          this.typeList = [{ type_name: 'vnsfs', type_id: 1 }];
          this.selected_type = this.typeList[0].type_id;
          this.filters = { tenant_id: this.authService.getTenant() };
          this.getNotifications();
        } else {
          this.selected_type = this.typeList[0].type_id;
          this.selected_name = this.typeList[0].type_name;

          this.items = [];
          this.typeList.forEach((element) => {
            if (element.type_id !== 0) {
              this.filters = { type: element.type_name };
              this.getNotifications();
            }
          });
        }
      });

      if (this.authService.isUserTenantAdmin()) {
        this.typeList = [{ type_name: 'vnsfs', type_id: 1 }];
        this.selected_type = this.typeList[0].type_id;
        this.filters = { tenant_id: this.authService.getTenant() };
        this.getNotifications();

        this.tableHeaders = {

          ...TABLE_HEADERS_VNSF,
          actions: [
            {
              label: 'View History',
              action: this.redirectToHistory.bind(this),
            },
          ],
        };
      } else {
        this.typeList = [{ type_name: 'any', type_id: 0 }, { type_name: 'sdn', type_id: 1 }, { type_name: 'hosts', type_id: 2 }];
        this.selected_type = this.typeList[0].type_id;
        this.selected_name = this.typeList[0].type_name;

        this.typeList.forEach((element) => {
          if (element.type_id !== 0) {
            this.filters = { type: element.type_name };
            this.getNotifications();
          }
        });

        this.tableHeaders = {
          ...TABLE_HEADERS_TM,
          actions: [
            {
              label: 'View History',
              action: this.redirectToHistory.bind(this),
            },
            {
              label: 'Attest',
              action: this.attestNode.bind(this),
            },
          ],
        };
      }
      this.loading = false;
    }

    redirectToHistory(node) {
      let nodeName = null;
      let nodeType = null;
      if (this.authService.isUserTenantAdmin()) {
        nodeName = node.vnsf_name;
        nodeType = null;
      } else {
        nodeName = node.node;
        nodeType = node.type;
      }
      this.state.go('history', { node: nodeName, type: nodeType });
    }

    onTypeChange(typeEvent) {
      for (let i = 0; i < this.typeList.length; i += 1) {
        if (typeEvent === this.typeList[i].type_id && typeEvent !== 0) {
          this.selected_type = this.typeList[i].type_id;
          this.selected_name = this.typeList[i].type_name;
          this.filters = { type: this.selected_name };
          this.getNotifications();
          break;
        } else if (typeEvent === this.typeList[i].type_id && typeEvent === 0) {
          this.items = [];
          this.typeList.forEach((element) => {
            if (element.type_id !== 0) {
              this.filters = { type: element.type_name };
              this.getNotifications();
            }
          });
          break;
        }
      }
    }

    getNotifications() {
      let typeNotification = null;
      this.attestationService.getNotifications(this.pagination, this.filters)
        .then((result) => {
          if (this.selected_type !== 0) {
            this.items = [];
          }
          if (this.authService.isUserTenantAdmin()) {
            this.items = [];
            result.notifs.forEach((item) => {
              item.vnsfs.forEach((vnsfsitem) => {
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
                });
              });
            });
          } else {
            result.notifs.map((item) => {
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
                  }
                });
                this.items = this.items.concat(itemsResult);
              } else {
                item[typeNotification].forEach((typeitem) => {
                  var timeValue = '';
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
                  })
                })
              }
            });
          }
          
          this.pagination.total = (result && result.meta.total) || 0;
          this.paging = this.calcPageItems();
        });
    }

    attestNode(node) {
      // this.loading = true;
      if (this.authService.isUserTenantAdmin()) {
        this.filters = { node_id: node.vnsf_name };
      } else {
        this.filters = { node_id: node.node };
      }
      this.attestationService.attestInfrastructure(this.filters)
      .then(() => {
        this.toast.success('Node attestation in progress', 'Node attestation');
      });
    }

    attestationAll() {
      this.attestationService.attestAllInfrastructure(this.filters)
      .then(() => {
        this.toast.success('NFV Infrastructure attestation in progress', 'NFV Infrastructure');
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

export const AttestationState = {
  parent: 'home',
  name: 'attestation',
  url: '/attestation',
  component: 'attestationView',
};
