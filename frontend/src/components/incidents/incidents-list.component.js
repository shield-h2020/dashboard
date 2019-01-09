import moment from 'moment';
import template from './incidents-list.html';
import styles from './incidents.scss';


const VIEW_STRINGS = {
  title: 'Security Incidents',
  tableTitle: 'Security incidents list',
  modalTitle: 'Incident Details',
  modalSubtitle: 'Recommendation action',
  apply: 'Apply',
  close: 'Close',
  startDate: 'Start:',
  endDate: 'End:',
  status: [
    {
      value: 'any',
      text: 'Any',
    },
    {
      value: 'Applied',
      text: 'Applied',
    },
    {
      value: 'Not applied',
      text: 'Not applied',
    },
  ],
};

const TABLE_HEADERS = {
  attack: 'Incident',
  detection: 'Date',
  severity: 'Severity',
  status: 'Recommendation',
};

const MODAL_ENTRIES = {
  _id: 'Id',
  attack: 'Incident',
  detection: 'Date',
  severity: 'Severity',
  status: 'Recommendation',
};

export const IncidentsListComponent = {
  template,
  controller: class IncidentsListComponent {
    constructor($scope, IncidentsService, toastr) {
      'ngInject';

      this.incidentsService = IncidentsService;
      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.scope = $scope;
      this.selected_period = 0;
      this.showDatePicker = false;
      this.pagination = {
        page: 1,
        limit: 10,
      };
      this.toast = toastr;
      this.filters = {};
      this.isLoading = false;
      this.tableHeaders = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'View',
            action: this.toggleIncidentModal.bind(this),
          },
        ],
      };
      this.modalEntries = MODAL_ENTRIES;
      this.incident = null;
      this.setPeriod();
      this.selectedStatus = 'any';
      this.getData = debounce(this.getData, 100, true, this);
    }

    $onInit() {
      this.getData();

      this.scope.$on('INCIDENT_UPDATE_DATA', () => {
        this.getData();
      });
    }

    getData() {
      this.isLoading = true;
      this.incidentsService
        .getIncidents(this.pagination, this.filters)
        .then((data) => {
          this.items = [...data.items];
          this.pagination.total = (data && data.meta.total) || 0;
          this.paging = this.calcPageItems();
          this.isLoading = false;
        });
    }

    setPeriod() {
      switch (this.selected_period) {
        case '0':
          this.filters = {};
          this.showDatePicker = false;
          break;
        case '1':
          this.scope.sdate = moment()
            .startOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          this.setFilter({ key: 'startDate', value: this.scope.sdate });

          this.scope.edate = moment()
            .format('YYYY-MM-DDTHH:mm:ss');
          this.setFilter({ key: 'endDate', value: this.scope.edate });

          this.showDatePicker = true;
          break;
        default:
          break;
      }

      this.getData();
    }

    setFilter(filter) {
      if (filter.key === 'startDate' || filter.key === 'endDate') {
        const query = filter.key === 'startDate' ? '$gte' : '$lte';
        if (!this.filters.detection) {
          this.filters.detection = {};
        }

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
        this.selectedStatus = filter.value;
      } else {
        this.filters[filter.key] = filter.value;
      }
      this.getData();
    }

    changePage(amount) {
      const condition =
        amount > 0
          ? this.items.length >= this.pagination.limit
          : this.pagination.page > 1;
      if (condition) {
        this.pagination.page += amount;
        this.getData();
      }
    }

    calcPageItems() {
      const { page, limit } = this.pagination;
      const length = this.items.length || 10;

      const res = page * limit - (length < limit ? limit : length) + 1;
      const res2 = page * limit + (length < limit ? -(limit - length) : 0);

      return { min: res, max: res2 };
    }

    toggleIncidentModal(incident) {
      this.incident = incident;
      this.modalOpen = !this.modalOpen;
    }

    applyRecommendation() {
      this.incidentsService
        .recommendAction(this.incident._id, this.incident._etag)
        .then(() => {
          this.toast.success(
            'Your recommendation was sent to the Orchestrator',
            'Apply recommendation',
            {
              onHidden: () => this.closeHandler && this.closeHandler(),
            },
          );
          this.toggleIncidentModal();
          this.getData();
        });
    }

    setStartDate() {
      this.startDate = this.scope.sdate;

      return this.startDate.toString();
    }

    setEndDate() {
      this.endDate = this.scope.edate;

      return this.endDate.toString();
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
