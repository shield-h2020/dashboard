import template from './tm-notifications-modal.html';
import styles from '../vnsf-notifications.scss';

const VIEW_STRINGS = {
  title: 'TM Notification',
  close: 'Close',
  'node': 'Node',
  'driver': 'Driver',
  'status': 'Status',
  'trust': 'Trust'
};

export const TmNotificationsModalComponent = {
  template,
  controller: class TmNotificationsModalComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.styles = styles;
      this.viewStrings = VIEW_STRINGS;
    }

    $onInit() {
      this.scope.$on('TM_NOTIF_BROADCAST', (event, data) => {
        console.log("something was received");
        //console.log(data);
        
        var firstLevelData = {};
        firstLevelData.node = data.hosts[0].node;
        firstLevelData.driver = data.hosts[0].driver;
        firstLevelData.status = data.hosts[0].status;
        firstLevelData.trust = data.hosts[0].trust;

        this.data = firstLevelData;
        this.extrainfo = data.hosts[0].extra_info;
        this.open = true;
      });
    }

    toggleModal() {
      this.open = !this.open;
    }

    prettyJSON(obj) {
      //console.log(obj);
      return JSON.stringify(obj, null, 2);
    }
  },
};

export default TmNotificationsModalComponent;
