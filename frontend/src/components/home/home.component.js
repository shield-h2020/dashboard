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
    constructor($scope, $state, toastr, VnsfNotificationService, IncidentsService) {
      'ngInject';

      this.scope = $scope;
      this.toast = toastr;
      this.state = $state;
      this.vnsfNotificationService = VnsfNotificationService;
      this.incidentsService = IncidentsService;
      this.tmSocketAtmp = 0;
      this.tmAdminSocketAtmp = 0;
      this.vnsfSocketAtmp = 0;
      this.incidentsSocketAtmp = 0;
      this.incidentsfSocket;
      this.vnsfSocket;
      this.tmAdminSocket;
      this.tmSocket;

    }

    $onInit() {
      if (this.userdata.roles.find(r => r.name === TENANT_ADMIN || r.name === TENANT_USER)) {
        this.initVNSFSocket();
        this.initTMSocket();
        this.initIncidentSocket();
      }
      else{
        this.initTMAdminSocket();
      }

      this.scope.$on('NSVF_NOTIF_EMIT', (event, data) => {
        this.openNotificationDetails(data);
      });

      this.scope.$on('INCIDENT_NOTIF_EMIT', (event, data) => {
        this.openRecommendation(data);
      });
      
      this.scope.$on('TM_NOTIF_EMIT', (event, data) => {
        this.openTMNotificationDetails(data);
      });

      this.scope.$on('ATTESTATION_NOTIF_EMIT', (event, data) => {
        this.openAttestationNotificationDetails(data);
      });
      this.scope.$on('MODAL_EVENT_EMIT', (event, data) => {
        this.modalEvent(data);
      });
    }

    $onDestroy() {
      if (this.userdata.roles.find(r => r.name === TENANT_ADMIN || r.name === TENANT_USER)) {
        this.incidentsSocketAtmp = 3;
        this.incidentsfSocket.close();

        this.vnsfSocketAtmp=3;
        this.vnsfSocket.close();

        this.tmSocketAtmp=3;
        this.tmSocket.close();

      }
      else{
        this.tmAdminSocketAtmp=3;
        this.tmAdminSocket.close();
      }
    }

    initIncidentSocket(){
      this.incidentsfSocket = this.incidentsService.connectIncidentSocket(this.userdata.user.domain.id);
      this.incidentsfSocket.onopen = (e) => {this.incidentsSocketAtmp = 0;};
      this.incidentsfSocket.onmessage = (message) => {
        const data = JSON.parse(message.data);
        const { attack } = data;
        this.toast.info(`Type of attack: ${attack}`, 'A new security incident was detected', {
          onTap: () => this.openRecommendation(data),
          onShown: () => {this.scope.$broadcast('INCIDENT_UPDATE_DATA');},
          closeButton: true,
        });
      };
      this.incidentsfSocket.onclose = (e) => {
        if(this.incidentsSocketAtmp < 3) {
          this.incidentsSocketAtmp++;
          setTimeout(this.initIncidentSocket(), 1000);
        }
      };
    }

    initVNSFSocket() {
      this.vnsfSocket = this.vnsfNotificationService.connectNotificationsSocket(this.userdata.user.domain.id);
      this.vnsfSocket.onopen = (e) => {this.vnsfSocketAtmp = 0;};
      this.vnsfSocket.onmessage = (message) => {
        //console.log("Broadcasting");
        const data = JSON.parse(message.data);
        this.toast.info(templateNotification(data), data.event.classification, {
          onTap: () => this.openNotificationDetails(data),
          closeButton: true,
        });
        this.scope.$broadcast('VNSF_UPDATE_BROADCAST');
      };
      this.vnsfSocket.onclose = (e) => {
        if(this.vnsfSocketAtmp < 3) {
          this.vnsfSocketAtmp++;
          setTimeout(this.initVNSFSocket(), 1000);
        }
      };
    }

    initTMAdminSocket(){
      this.tmAdminSocket = this.vnsfNotificationService.connectTMAdminNotificationsSocket();
      this.tmAdminSocket.onopen = (e) => {this.tmAdminSocketAtmp = 0;};
      this.tmAdminSocket.onmessage = (message) => {
        this.toast.info(message.data, 'TM Notification', {
          onTap: () => {this.state.go('attestation', { prevRoute: this.state.current.name })},
          onShown: () => {this.scope.$broadcast('ATTESTATION_UPDATE_DATA');},
          closeButton: true,
        });
        
        this.scope.$broadcast('TM_UPDATE_BROADCAST');
      };
      this.tmAdminSocket.onclose = (e) => {
        if(this.tmAdminSocketAtmp < 3) {
          this.tmAdminSocketAtmp++;
          setTimeout(this.initTMAdminSocket(), 1000);
        }
      };
    }

    initTMSocket() {

      this.tmSocket = this.vnsfNotificationService.connectTMNotificationsSocket(this.userdata.user.domain.id);
      this.tmSocket.onopen = (e) => {this.tmSocketAtmp = 0;};
      this.tmSocket.onmessage = (message) => {
        this.toast.info(message.data, 'TM Notification', {
          onTap: () => {this.state.go('attestation', { prevRoute: this.state.current.name })},
          onShown: () => {this.scope.$broadcast('ATTESTATION_UPDATE_DATA');},
          closeButton: true,
        });
        
        this.scope.$broadcast('TM_UPDATE_BROADCAST');
      };
      this.tmSocket.onclose = (e) => {
        if(this.tmSocketAtmp < 3) {
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

    openAttestationNotificationDetails(data) {
      this.scope.$broadcast('ATTESTATION_NOTIF_BROADCAST', data);
    }
    modalEvent(data) {
      this.scope.$broadcast('MODAL_EVENT_BROADCAST', data);
    }
  },
};

export default HomeComponent;

