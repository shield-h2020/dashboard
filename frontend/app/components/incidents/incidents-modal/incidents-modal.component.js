import template from './incidents-modal.html';
import styles from './incidents-modal.scss';

const UI_STRINGS = {
  CLOSE: 'Back',
  APPLY: 'Apply Recommendation',
  TITLE: 'General information',
  SUBTITLE: 'Recommended action',
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
      this.STRINGS = UI_STRINGS;
      this.styles = styles;
      this.scope = $scope;
      this.toast = toastr;
      this.incidentsService = IncidentsService;
    }

    $onInit() {
      this.scope.$on(INCIDENTS_MODAL_EVENT.BROADCAST.OPEN, (event, data) => {
        this.isOpen = true;
        this.incident = data.data;
      });
    }

    applyRecommendation() {
      this.closeModal();
      this.incidentsService.recommendAction(this.incident._id, this.incident._etag)
      .then(() => this.toast.success('', 'Your recommendation was sent to the Orchestrator', {
        onHidden: () => this.closeHandler && this.closeHandler()
      }));
    }

    openModal() {
      this.isOpen = true;
    }

    closeModal() {
      this.isOpen = false;
    }
  },
};
