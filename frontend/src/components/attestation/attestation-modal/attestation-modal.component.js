import template from './attestation-modal.html';
import styles from '../attestation.scss';

const VIEW_STRINGS = {
  title: 'Attestation Notification',
  cancel: 'Cancel',
  apply: 'Apply',
  node: 'Node',
  status: 'Status',
  driver: 'Driver',
  trust: 'Trusted',
  time: 'Time',
  vnsf_id: "VNSF ID",
  vnsf_name: "VNSF Name",
  ns_id: "NS ID"

};

export const AttestationModalComponent = {
  template,
  controller: class AttestationModalComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.styles = styles;
      this.viewStrings = VIEW_STRINGS;
    }

    $onInit() {
      this.scope.$on('ATTESTATION_NOTIF_BROADCAST', (event, data) => {
        var firstLevelData = {};

        if (data.type == 'sdn') {
          firstLevelData.node = data.node;
          firstLevelData.driver = data.driver;
          firstLevelData.trust = data.trust;
          firstLevelData.time = data.time;

          this.remediation = data.extrainfo.Remediation;
          this.extrainfo = Object.assign({}, data.extrainfo);
          delete this.extrainfo["Remediation"];
        }
        else if (data.type == 'hosts') {
          firstLevelData.node = data.node;
          firstLevelData.status = data.status;
          firstLevelData.driver = data.driver;
          firstLevelData.trust = data.trust;
          firstLevelData.time = data.time;

          this.extrainfo = data.extrainfo;
          this.remediation = data.remediation;
        }
        else {
          firstLevelData.vnsf_id = data.vnsf_id;
          firstLevelData.vnsf_name = data.vnsf_name;
          firstLevelData.trust = data.trust;
          firstLevelData.ns_id = data.ns_id;
          firstLevelData.time = data.time;

          this.remediation = data.remediation;
        }

        this.data = firstLevelData;
        this.open = true;
      });
    }

    toggleModal() {
      this.open = !this.open;
    }

    applyRemediation() {
      this.open = !this.open;
    }

    prettyJSON(obj) {
      //console.log(obj);
      return JSON.stringify(obj, null, 2);
    }
  },
};

export default AttestationModalComponent;
