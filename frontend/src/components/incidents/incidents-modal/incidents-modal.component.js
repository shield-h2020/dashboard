import template from "./incidents-modal.html";
import styles from "./incidents-modal.scss";

const VIEW_STRINGS = {
  modalTitle: "Incident Details",
  modalSubtitle: "Recommendation action",
  apply: "Apply",
  close: "Close"
};

const MODAL_ENTRIES = {
  _id: "Id",
  attack: "Type of incident",
  detection: "Detection Date",
  severity: "Severity",
  status: "Status"
};

export const INCIDENTS_MODAL_EVENT = {
  EMIT: {
    OPEN: "emitIncidentsOpen",
    CLOSE: "emitIncidentsClose"
  },
  BROADCAST: {
    OPEN: "castIncidentsOpen",
    CLOSE: "castIncidentsClose"
  }
};

export const IncidentsModalComponent = {
  template,
  bindings: {
    incident: "<",
    isOpen: "<",
    closeHandler: "&?"
  },
  controller: class IncidentsModalComponent {
    constructor($scope, IncidentsService) {
      "ngInject";

      this.isOpen = false;
      this.viewStrings = VIEW_STRINGS;
      this.modalEntries = MODAL_ENTRIES;
      this.styles = styles;
      this.scope = $scope;
      this.incidentsService = IncidentsService;
    }

    $onInit() {
      this.scope.$on("INCIDENT_NOTIF_BROADCAST", (event, data) => {
        this.data = data;
        this.toggleIncidentModal();
      });
    }

    toggleIncidentModal() {
      this.isOpen = !this.isOpen;
    }
  }
};
