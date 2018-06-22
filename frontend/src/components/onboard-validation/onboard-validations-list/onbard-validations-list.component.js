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
      this.isLoading = false;
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
      this.getData();
    }

    getData() {
      this.isLoading = true;
      this.onboardValidationService.getValidations({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = OnboardValidationsListComponent.addExtraClasses(items);
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

