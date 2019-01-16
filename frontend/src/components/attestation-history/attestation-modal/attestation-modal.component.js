import template from './attestation-modal.html';
import styles from '../../attestation/attestation.scss';

const VIEW_STRINGS = {
  titleModal: 'Attestation Notification',
  cancel: 'Cancel',
  apply: 'Apply',
  node: 'Node',
  status: 'Status',
  driver: 'Driver',
  trust: 'Trusted',
  time: 'Time',
  vnsf_id: 'VNSF ID',
  vnsf_name: 'VNSF Name',
  ns_id: 'NS ID',

};

export const AttestationModalComponent = {
  template,
  controller: class AttestationModalComponent {
    constructor($scope, AuthService, toastr, AttestationHistoryService) {
      'ngInject';

      this.scope = $scope;
      this.authService = AuthService;
      this.attestationHistoryService = AttestationHistoryService;
      this.styles = styles;
      this.viewStrings = VIEW_STRINGS;
      this.toast = toastr;
      this.disabledAplly = true;
    }

    $onInit() {
      this.scope.$on('ATTESTATION_NOTIF_BROADCAST', (event, data) => {
        const firstLevelData = {};

        if (data.type === 'sdn') {
          firstLevelData.node = data.node;
          firstLevelData.driver = data.driver;
          firstLevelData.trust = data.trust;
          firstLevelData.status = data.status;
          firstLevelData.time = data.time;

          this.remediation = data.extrainfo.Remediation;
          this.extrainfo = Object.assign({}, data.extrainfo);
          delete this.extrainfo.Remediation;
        } else if (data.type === 'hosts') {
          firstLevelData.node = data.node;
          firstLevelData.status = data.status;
          firstLevelData.driver = data.driver;
          firstLevelData.trust = data.trust;
          firstLevelData.status = data.status;
          firstLevelData.time = data.time;

          this.extrainfo = data.extrainfo;
          this.remediation = data.remediation;
        } else {
          firstLevelData.vnsf_id = data.vnsf_id;
          firstLevelData.vnsf_name = data.vnsf_name;
          firstLevelData.trust = data.trust;
          firstLevelData.status = data.status;
          firstLevelData.ns_id = data.ns_id;
          firstLevelData.time = data.time;

          this.remediation = data.remediation;
        }

        this.optionsRemediation = [];
        if (this.authService.isUserTenantAdmin()) {
          Object.keys(data.remediation).forEach((key) => {
            if (data.remediation[key] === true && key.toLocaleLowerCase() !== 'terminate') {
              this.optionsRemediation.push({ text: key, value: key });
            }
          });
        } else if (data.type === 'sdn') {
          Object.keys(data.extrainfo.Remediation).forEach((key) => {
            if (data.extrainfo.Remediation[key] === true && key.toLocaleLowerCase() !== 'terminate') {
              this.optionsRemediation.push({ text: key, value: key });
            }
          });
        } else {
          Object.keys(data.remediation).forEach((key) => {
            if (data.remediation[key] === true && key.toLocaleLowerCase() !== 'terminate') {
              this.optionsRemediation.push({ text: key, value: key });
            }
          });
        }
        if (this.optionsRemediation.length > 0) {
          this.applyRemediationDropdown = true;
        } else {
          this.applyRemediationDropdown = false;
        }
        this.data = firstLevelData;
        this.nodeData = data;
        this.open = true;
      });
    }

    toggleModal() {
      this.scope.emitEvent = () => {
        this.scope.$broadcast('modalEvent', 'close');
      };
      this.open = !this.open;
      this.scope.$emit('MODAL_EVENT_EMIT', { message: 'cancel' });
    }

    applyRemediation() {
      let id = null;
      let data = null;
      let etag = null;
      if (this.selectedRemediation === undefined) {
        this.selectedRemediation = this.optionsRemediation[0].value;
      }
      if (this.authService.isUserTenantAdmin()) {
        id = this.nodeData._id;
        etag = this.nodeData._etag;
        data = {
          vnsfs: [
            {
              remediation: { },
            },
          ],
        };
        data.vnsfs[0].remediation[`${this.selectedRemediation}`] = true;
      } else if (this.nodeData.type === 'sdn') {
        id = this.nodeData._id;
        etag = this.nodeData._etag;
        data = {
          sdn: [
            {
              node: this.nodeData.node,
              remediation: { },
            },
          ],
        };
        data.sdn[0].remediation[`${this.selectedRemediation}`] = true;
      } else {
        id = this.nodeData._id;
        etag = this.nodeData._etag;
        data = {
          hosts: [
            {
              node: this.nodeData.node,
              remediation: { },
            },
          ],
        };
        data.hosts[0].remediation[`${this.selectedRemediation}`] = true;
      }
      this.attestationHistoryService.getRemediation(id, data, etag)
      .then(() => {
        this.status = 'ok';
        this.toast.success('Remediation has trigger successfully', 'Remediation Trigger Successfully');
      })
      .catch(() => {
        this.status = 'error';
        this.toast.error('Remediation has not trigger successfully', 'Remediation Error');
      });
      this.open = !this.open;
      this.scope.$emit('MODAL_EVENT_EMIT', { message: 'apply', status: this.status });
    }

    setRemediation(val) {
      this.selectedRemediation = val;
    }
  },

};

export default AttestationModalComponent;
