import template from './vnsf-notifications-modal.html';
import styles from '../vnsf-notifications.scss';

const VIEW_STRINGS = {
  title: 'VNSF Notification',
  close: 'Close',
  classification: 'Classification',
  'classification-id': 'Classification Id',
  'destination-ip': 'Destination IP',
  'dport-icode': 'Dport Icode',
  'event-id': 'Event Id',
  'event-microsecond': 'Event(microsecond)',
  'event-second': 'Event(second)',
  protocol: 'Protocol',
  'signature-id': 'Signature Id',
  'source-ip': 'Source IP',
  'sport-itype': 'Sport iType',
};

export const VnsfNotificationsModalComponent = {
  template,
  controller: class VnsfNotificationsModalComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.styles = styles;
      this.viewStrings = VIEW_STRINGS;
    }

    $onInit() {
      this.scope.$on('NSVF_NOTIF_BROADCAST', (event, data) => {
        this.data = data.event;
        this.open = true;
      });
    }

    toggleModal() {
      this.open = !this.open;
    }
  },
};

export default VnsfNotificationsModalComponent;
