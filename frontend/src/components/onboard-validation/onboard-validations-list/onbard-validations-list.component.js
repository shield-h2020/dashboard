import template from './onboard-validations-list.html';

const VIEW_STRINGS = {
  title: 'Validations list',
  cardTitle: 'Validations',
};

const TABLE_HEADERS = {
  _id: 'Id',
  _created: 'Created',
  status: 'Status',
};

export const OnboardValidationsListComponent = {
  template,
  controller: class OnboardValidationsListComponent {
    constructor(OnboardValidationService, $state) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.onboardValidationService = OnboardValidationService;
      this.state = $state;
      this.createOpen = false;
      this.deleteOpen = false;

      this.offset = 0;
      this.limit = 25;
      this.filters = {};
      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.viewValidation.bind(this),
          },
        ],
      };
    }

    $onInit() {
      this.onboardValidationService.getValidations({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items.map(item => ({
            ...item,
            status: this.setStatus(item),
          }));
        });
    }

    setStatus(validation) {
      const { result: { error_count, warning_count } } = validation;

      if (error_count) return 'error';
      if (warning_count) return 'warn';
      return '';
    }

    viewValidation(validation) {
      this.state.go('validation', { validation });
    }
  },
};

export const validationsListState = {
  parent: 'home',
  name: 'validations',
  url: '/validations',
  component: 'validationsListView',
};

