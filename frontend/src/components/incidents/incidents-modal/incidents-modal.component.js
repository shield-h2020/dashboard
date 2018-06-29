import template from './incidents-modal.html';
import styles from './incidents-modal.scss';

const VIEW_STRINGS = {
  modalTitle: 'Incident Details',
  modalSubtitle: 'Recommendation action',
  apply: 'Apply',
  close: 'Close',
};

const MODAL_ENTRIES = {
  _id: 'Id',
  attack: 'Type of attack',
  detection: 'Detection Date',
  severity: 'Severity',
  status: 'Status',
};

export const INCIDENTS_MODAL_EVENT = {
  EMIT: {
    OPEN: 'emitIncidentsOpen',
    CLOSE: 'emitIncidentsClose',
  },
  BROADCAST: {
    OPEN: 'castIncidentsOpen',
    CLOSE: 'castIncidentsClose',
  },
};

export const IncidentsModalComponent = {
  template,
  bindings: {
    incident: '<',
    isOpen: '<',
    closeHandler: '&?',
  },
  controller: class IncidentsModalComponent {
    constructor($scope, IncidentsService, toastr) {
      'ngInject';

      this.isOpen = false;
      this.viewStrings = VIEW_STRINGS;
      this.modalEntries = MODAL_ENTRIES;
      this.styles = styles;
      this.scope = $scope;
      this.toast = toastr;
      this.incidentsService = IncidentsService;
    }

    $onInit() {
      this.scope.$on('INCIDENT_NOTIF_BROADCAST', (event, data) => {
        this.data = data;
        this.toggleIncidentModal();
      });
    }

    applyRecommendation() {
      const { _id, _etag } = this.data;
      this.incidentsService.recommendAction(_id, _etag)
        .then(() => {
          this.toast.success('', 'Your recommendation was sent to the Orchestrator', {
            onHidden: () => this.closeHandler && this.closeHandler(),
          });
          this.toggleIncidentModal();
        });
    }

    toggleIncidentModal() {
      this.isOpen = !this.isOpen;
    }
  },
};
