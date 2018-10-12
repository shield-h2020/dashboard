import template from './attestation.html';

const VIEW_STRING = {
  title: 'Attestation',
  tableTitle: 'Attestation'
};

const TABLE_HEADERS_TM = {
  type: 'Type',
  node: 'Node',
  trust: 'Trusted',
  driver: 'Driver',
  time: 'Time'
};

const TABLE_HEADERS_VNSF = {
  "vnsf_name": "VNSF Name",
  trust: 'Trusted',
  time: 'Time'
};

export const AttestationComponent = {
  template,
  bindings: {
    tenant: '<'
  },
  controller: class AttestationComponent {
    constructor($stateParams, $state, $scope, AttestationService, AuthService) {
      'ngInject';
      this.viewStrings = VIEW_STRING;
      this.scope = $scope;
      this.attestationService = AttestationService;
      this.authService = AuthService;
    }

    $onInit() {
      this.items = [];
      this.scope.$on('ATTESTATION_UPDATE_DATA', (event, data) => {
        if (this.authService.isUserTenantAdmin()) {
          this.typeList = [{ 'type_name': 'vnsfs', 'type_id': 1 }];
          this.selected_type = this.typeList[0].type_id;
          this.filters = { "tenant_id": this.authService.getTenant() };
          this.getNotifications();
        }
        else {
          this.selected_type = this.typeList[0].type_id;
          this.selected_name = this.typeList[0].type_name;

          this.items = [];
          this.typeList.forEach(element => {
            if (element.type_id != 0) {
              this.filters = { "type": element.type_name };
              this.getNotifications();
            }
          });

        }
      });

      if (this.authService.isUserTenantAdmin()) {
        this.typeList = [{ 'type_name': 'vnsfs', 'type_id': 1 }];
        this.selected_type = this.typeList[0].type_id;
        this.filters = { "tenant_id": this.authService.getTenant() };
        this.getNotifications();

        this.tableHeaders = {
          ...TABLE_HEADERS_VNSF,
          actions: [
            {
              label: 'view',
              action: this.toggleNotificationsModal.bind(this),
            }
          ],
        };
      }
      else {
        this.typeList = [{ 'type_name': 'any', 'type_id': 0 }, { 'type_name': 'sdn', 'type_id': 1 }, { 'type_name': 'hosts', 'type_id': 2 }];
        this.selected_type = this.typeList[0].type_id;
        this.selected_name = this.typeList[0].type_name;

        this.typeList.forEach(element => {
          if (element.type_id != 0) {
            this.filters = { "type": element.type_name };
            this.getNotifications();
          }
        });

        this.tableHeaders = {
          ...TABLE_HEADERS_TM,
          actions: [
            {
              label: 'view',
              action: this.toggleNotificationsModal.bind(this),
            }
          ],
        };
      }
      this.loading = false;

    }

    toggleNotificationsModal(notif) {
      this.scope.$emit('ATTESTATION_NOTIF_EMIT', notif);
    }

    onTypeChange(typeEvent) {
      for (var i = 0; i < this.typeList.length; i++) {
        if (typeEvent == this.typeList[i].type_id && typeEvent != 0) {
          this.selected_type = this.typeList[i].type_id;
          this.selected_name = this.typeList[i].type_name;
          this.filters = { "type": this.selected_name };
          this.getNotifications();
          break;
        }
        else if (typeEvent == this.typeList[i].type_id && typeEvent == 0) {
          this.items = [];
          this.typeList.forEach(element => {
            if (element.type_id != 0) {
              this.filters = { "type": element.type_name };
              this.getNotifications();
            }
          });
          break;
        }
      }

    }

    getNotifications() {
      var typeNotification;
      this.attestationService.getNotifications({ page: 1, limit: 1 }, this.filters)
        .then(result => {
          if (this.authService.isUserTenantAdmin()) {
            result.map(item => {
              this.items = item.vnsfs.map(vnsfsitem => {
                return {
                  "_id": item._id,
                  "vnsf_id": vnsfsitem.vnsf_id,
                  "vnsf_name": vnsfsitem.vnsfd_name,
                  "remediation": vnsfsitem.remediation,
                  "trust": vnsfsitem.trust,
                  "ns_id": vnsfsitem.ns_id,
                  "time": item.time,
                  "tenant_id": item.tenant_id
                }
              })
            });
          }
          else {
            result.map(item => {
              typeNotification = item.type;
              if (this.selected_type == 0) {
                let itemsResult = item[typeNotification].map(typeitem => {
                  var timeValue = '';
                  if (typeitem.time) {
                    timeValue = typeitem.time;
                  }
                  else {
                    timeValue = typeitem.extra_info.Time;
                  }
                  return {
                    "_id": item._id,
                    "type": item.type,
                    "driver": typeitem.driver,
                    "node": typeitem.node,
                    "extrainfo": typeitem.extra_info,
                    "remediation": typeitem.remediation,
                    "trust": typeitem.trust,
                    "status": typeitem.status,
                    "time": timeValue
                  }
                });
                this.items = this.items.concat(itemsResult);
              }
              else {
                this.items = item[typeNotification].map(typeitem => {
                  var timeValue = '';
                  if (typeitem.time) {
                    timeValue = typeitem.time;
                  }
                  else {
                    timeValue = typeitem.extra_info.Time;
                  }
                  return {
                    "_id": item._id,
                    "type": item.type,
                    "driver": typeitem.driver,
                    "node": typeitem.node,
                    "extrainfo": typeitem.extra_info,
                    "remediation": typeitem.remediation,
                    "trust": typeitem.trust,
                    "status": typeitem.status,
                    "time": timeValue
                  }
                })
              }

            });
          }
        });
    }
  }
};

export const AttestationState = {
  parent: 'home',
  name: 'attestation',
  url: '/attestation',
  component: 'attestationView',
};
