import template from './incidents-list.html';
import styles from './incidents.scss';

const VIEW_STRINGS = {
  title: 'Security Incidents',
  tableTitle: 'Security incidents list',
  modalTitle: 'Incident Details',
  modalSubtitle: 'Recommendation action',
  apply: 'Apply',
  close: 'Close',
  startDate: 'Start date:',
  endDate: 'End date:',
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
};

const TABLE_HEADERS = {
  attack: 'Type of attack',
  detection: 'Detection Date',
  severity: 'Severity',
  status: 'Status',
};

const MODAL_ENTRIES = {
  _id: 'Id',
  attack: 'Type of attack',
  detection: 'Detection Date',
  severity: 'Severity',
  status: 'Status',
};

export const IncidentsListComponent = {
  template,
  controller: class IncidentsListComponent {
    constructor(IncidentsService) {
      'ngInject';

      this.incidentsService = IncidentsService;
      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.pagination = {
        page: 1,
        limit: 10,
      };
      this.filters = {};
      this.isLoading = false;
      this.tableHeaders = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.toggleIncidentModal.bind(this),
          },
        ],
      };
      this.modalEntries = MODAL_ENTRIES;
      this.incident = null;
      this.getData = debounce(this.getData, 100, true, this);
    }

    $onInit() {
      this.getData();
    }

    getData() {
      this.isLoading = true;
      this.incidentsService.getIncidents(this.pagination, this.filters)
        .then((data) => {
          this.items = [...data.items];
          this.pagination.total = (data && data.meta.total) || 0;
          this.paging = this.calcPageItems();
          this.isLoading = false;
        });
    }

    setFilter(filter) {
      if (filter.key === 'startDate' || filter.key === 'endDate') {
        const query = filter.key === 'startDate' ? '$gte' : '$lte';
        if (!this.filters.detection) this.filters.detection = {};
        const date = new Date(filter.value);
        if (filter.key === 'endDate') {
          date.setSeconds(59);
        }
        this.filters.detection[query] = date.toUTCString();
      } else if (filter.key === 'status') {
        if (filter.value === 'any') {
          delete this.filters.status;
        } else {
          this.filters[filter.key] = filter.value;
        }
      } else {
        this.filters[filter.key] = filter.value;
      }

      this.getData();
    }

    changePage(amount) {
      const condition = amount > 0 ?
        this.items.length >= this.pagination.limit : this.pagination.page > 0;
      if (condition) {
        this.pagination.page += amount;
        this.getData();
      }
    }

    calcPageItems() {
      const { page, limit } = this.pagination;
      const length = this.items.length || 10;

      const res = ((page * limit) - (length < limit ? limit : length)) + 1;
      const res2 = (page * limit) + (length < limit ? -(limit - length) : 0);

      return { min: res, max: res2 };
    }

    toggleIncidentModal(incident) {
      this.incident = incident;
      this.modalOpen = !this.modalOpen;
    }

    applyRecommendation() {
      this.incidentsService.recommendAction(this.incident._id, this.incident._etag)
      .then(() => {
        this.toast.success('', 'Your recommendation was sent to the Orchestrator', {
          onHidden: () => this.closeHandler && this.closeHandler(),
        });
        this.toggleIncidentModal();
      });
    }

    setStartDate() {
      this.startDate = new Date();
      this.startDate.setFullYear(this.startDate.getFullYear() - 1);

      return this.startDate.toString();
    }
  },
};

export const IncidentsListState = {
  parent: 'home',
  name: 'incidentslist',
  url: '/incidentslist',
  component: 'incidentsListView',
};

function debounce(func, wait, immediate, context = this, ...args) {
  let timeout;
  return () => {
    const later = () => {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}
