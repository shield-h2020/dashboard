import template from './home.html';
import { TENANT_ADMIN, TENANT_USER } from '@/strings/role-strings.js';

function templateNotification(data) {
  return `
    source: ${data.event['source-ip']}
    target: ${data.event['destination-ip']}
  `;
}

function templateTMNotification(data) {
  return `
    node: ${data.hosts[0]['node']}
    trust: ${data.hosts[0]['trust']}
  `;
}

export const HomeComponent = {

  template,
  bindings: {
    userdata: '<',
  },
  controller: class HomeComponent {
    constructor($scope, toastr, VnsfNotificationService, IncidentsService) {
      'ngInject';

      this.scope = $scope;
      this.toast = toastr;
      this.vnsfNotificationService = VnsfNotificationService;
      this.incidentsService = IncidentsService;
      this.tmSocketAtmp = 0;
      this.vnsfSocketAtmp = 0;
    }

    $onInit() {
      if (this.userdata.roles.find(r => r.name === TENANT_ADMIN || r.name === TENANT_USER)) {
        
        this.initVNSFSocket();
        this.initTMSocket();
      }

      this.incidentsService.connectIncidentSocket()
        .onmessage = (message) => {
          const data = JSON.parse(message.data);
          const { attack } = data;
          this.toast.error(`Type of attack: ${attack}`, 'A new security incident was detected', {
            onTap: () => this.openRecommendation(data),
            closeButton: true,
          });
        };

      this.scope.$on('NSVF_NOTIF_EMIT', (event, data) => {
        this.openNotificationDetails(data);
      });

      this.scope.$on('INCIDENT_NOTIF_EMIT', (event, data) => {
        this.openRecommendation(data);
      });
      
      this.scope.$on('TM_NOTIF_EMIT', (event, data) => {
        this.openTMNotificationDetails(data);
      });
    }
    initVNSFSocket() {
      var vnsfSocket = this.vnsfNotificationService.connectNotificationsSocket(this.userdata.user.domain.id);
      vnsfSocket.onopen = (e) => {this.vnsfSocketAtmp = 0;};
      vnsfSocket.onmessage = (message) => {
        //console.log("Broadcasting");
        const data = JSON.parse(message.data);
        this.toast.error(templateNotification(data), data.event.classification, {
          onTap: () => this.openNotificationDetails(data),
          closeButton: true,
        });
        this.scope.$broadcast('VNSF_UPDATE_BROADCAST');
      };
      vnsfSocket.onclose = (e) => {
        if(this.vnsfSocketAtmp < 3) {
          //window.alert("Ai vai");
          this.vnsfSocketAtmp++;
          setTimeout(this.initVNSFSocket(), 1000);
        }
      };
    }
    initTMSocket() {

      var tmSocket = this.vnsfNotificationService.connectTMNotificationsSocket(this.userdata.user.domain.id);
      tmSocket.onopen = (e) => {this.tmSocketAtmp = 0;};
      tmSocket.onmessage = (message) => {
        const data = JSON.parse(message.data);
        //console.log(data);
        this.toast.error(templateTMNotification(data), 'TM Notification', {
          onTap: () => this.openTMNotificationDetails(data),
          closeButton: true,
        });
        
        this.scope.$broadcast('TM_UPDATE_BROADCAST');
      };
      tmSocket.onclose = (e) => {
        if(this.tmSocketAtmp < 3) {
          //window.alert("Ai vai");
          this.tmSocketAtmp++;
          setTimeout(this.initTMSocket(), 1000);
        }
      };
    }

    openNotificationDetails(data) {
      this.scope.$broadcast('NSVF_NOTIF_BROADCAST', data);
    }

    openRecommendation(data) {
      this.scope.$broadcast('INCIDENT_NOTIF_BROADCAST', data);
    }

    openTMNotificationDetails(data) {
      this.scope.$broadcast('TM_NOTIF_BROADCAST', data);
    } 
  },
};

export default HomeComponent;

