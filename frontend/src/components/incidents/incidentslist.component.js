import template from './incidentslist.html';
import { INCIDENTS_MODAL_EVENT } from './incidents-modal/incidents-modal.component';

const UI_STRINGS = {
  title: 'Security Incidents',
  filters: {
    status: [
      {
        value: 'any',
        text: 'Any',
      },
      {
        value: 'Applied',
        text: 'Applied',
      }, {
        value: 'Not applied',
        text: 'Not applied',
      },
    ],
  },
  table: {
    title: 'Security Incidents list',
    headers: [
      { label: 'Detection Date', key: 'detection' },
      { label: 'Severity', key: 'severity' },
      { label: 'Status', key: 'status' },
      { label: 'Type of attack', key: 'attack' }],
    actions: {
      update: 'recommendation',
    },
  },
};

export const IncidentsListComponent = {
  template,
  controller: class IncidentsListComponent {
    constructor($state, $scope, toastr, IncidentsService) {
      'ngInject';

      this.strings = UI_STRINGS;
      this.state = $state;
      this.scope = $scope;
      this.toast = toastr;
      this.incidentsService = IncidentsService;
      this.isLoading = true;
      this.incidents = [];
      this.currentIncident = null;
      this.tableConf = {
        headers: [],
        searchable: true,
      };

      UI_STRINGS.table.headers.forEach((header) => {
        this.tableConf.headers.push({
          header: header.label,
          key: header.key,
        });
      });
      this.tableConf.hasEnable = {
        key: 'status',
        value: 'ENABLED',
      };
      this.tableConf.rowSizes = [10, 20, 30];
      this.modalOpen = false;
      this.tableSource = this.tableSource.bind(this);
    }

    $onInit() {
      this.socket = this.incidentsService.connectIncidentSocket();
      this.socket.onmessage = (message) => {
        const data = JSON.parse(message.data);
        const attackType = data.attack;
        this.toast.error(`Type of attack: ${attackType}`, 'A new security incident was detected', {
          onTap: () => this.openRecommendation(data),
          onHidden: () => { this.refreshTable = true; },
          closeButton: true,
        });
      };
    }

    tableSource(pagination, filters) {
      this.refreshTable = false;
      return this.incidentsService.getIncidents(pagination, filters);
    }

    openRecommendation(incident) {
      this.scope.$broadcast(INCIDENTS_MODAL_EVENT.BROADCAST.OPEN, { data: incident });
    }

    modalCloseHandler() {
      this.refreshTable = true;
    }

    onAction(incident, action) {
      switch (action) {
        case 'recommendation':
          this.openRecommendation(incident);
          break;
        default:
      }
    }
  },
};

export const IncidentsListState = {
  parent: 'home',
  name: 'incidentslist',
  url: '/incidentslist',
  component: 'incidentsListView',
};
