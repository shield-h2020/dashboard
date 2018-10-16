import template from './onboard-validations-list.html';
import styles from '../onboard-validation.scss';

const VIEW_STRINGS = {
  title: 'Validations list',
  cardTitle: 'Validations',
  type: [
    {
      text: 'All',
      value: 'all',
    },
    {
      text: 'vNSF',
      value: 'vNSF',
    },
    {
      text: 'NS',
      value: 'NS',
    },
  ],
  startDate: 'Start date',
  endDate: 'End date',
  deleteModalTitle: 'Delete Validation',
  deleteButton: 'Delete',
  cancelButton: 'Cancel',
  confirmDelete: 'Are you sure you want to delete the validation for the',
};

const TABLE_HEADERS = {
  type: 'Type',
  _id: 'Id',
  _updated: 'Date',
};

export const OnboardValidationsListComponent = {
  template,
  controller: class OnboardValidationsListComponent {
    constructor(OnboardValidationService, $state, toastr) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.onboardValidationService = OnboardValidationService;
      this.state = $state;
      this.toast = toastr;
      this.createOpen = false;
      this.deleteOpen = false;

      this.pagination = {
        page: 1,
        limit: 10,
      };
      this.isLoading = false;
      this.filters = {};
      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.viewValidation.bind(this),
          },
          {
            label: 'delete',
            action: this.toggleDeleteModal.bind(this),
          },
        ],
      };
    }

    $onInit() {
      this.getData();
    }

    getData() {
      this.isLoading = true;
      this.onboardValidationService.getValidations(this.pagination, this.filters)
        .then(({ items, meta }) => {
          this.items = OnboardValidationsListComponent.addExtraClasses(items);
          this.pagination.total = (meta && meta.total) || 0;
          this.paging = this.calcPageItems();
        })
        .finally(() => { this.isLoading = false; });
    }

    static addExtraClasses(items) {
      return items.map(item => ({
        ...item,
        status: '',
        cellClasses: {
          status: (item.result.error_count || item.result.warning_count) ?
            `glyphicon glyphicon-exclamation-sign ${item.result.error_count ? 'icon-red' : ''}
              ${!item.result.error_count && item.result.warning_count ? 'icon-yellow' : ''}` : '',
        },
      }));
    }

    viewValidation({ _id }) {
      this.state.go('validation', { id: _id });
    }

    setFilter(filter) {
      if (filter.key === 'startDate' || filter.key === 'endDate') {
        const query = filter.key === 'startDate' ? '$gte' : '$lte';
        if (!this.filters._updated) this.filters._updated = {};
        const date = new Date(filter.value);
        if (filter.key === 'endDate') {
          date.setSeconds(59);
        }
        this.filters._updated[query] = date.toUTCString();
      } else if (filter.key === 'type') {
        if (filter.value === 'all') {
          delete this.filters.type;
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
        this.items.length >= this.pagination.limit : this.pagination.page > 1;
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

    setStartDate() {
      this.startDate = new Date();
      this.startDate.setFullYear(this.startDate.getFullYear() - 1);

      return this.startDate.toString();
    }

    toggleDeleteModal(validation) {
      this.validation = validation;
      this.deleteModalOpen = !this.deleteModalOpen;
    }

    deleteValidation() {
      this.onboardValidationService.deleteValidation(this.validation)
        .then(() => {
          this.toast.success('Validation deleted successfully', 'Validation deletion');
          this.toggleDeleteModal();
          this.getData();
        });
    }
  },
};

export const validationsListState = {
  parent: 'home',
  name: 'validations',
  url: '/validations',
  component: 'validationsListView',
};

