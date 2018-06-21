import template from './catalogue.html';

const UI_STRINGS = {
  title: 'NS catalogue',
  tableTitle: 'Catalogue',
};

const TABLE_HEADERS = {
  custom_tags: 'Tags',
  ref_id: 'Id',
  _created: 'Created',
};

export const CatalogueComponent = {
  template,
  controller: class CatalogueComponent {
    constructor(CatalogueService, AuthService) {
      'ngInject';

      this.strings = UI_STRINGS;
      this.catalogueService = CatalogueService;
      this.authService = AuthService;
      this.createOpen = false;
      this.deleteOpen = false;

      this.offset = 0;
      this.limit = 25;
      this.isLoading = false;
      this.filters = {};
      this.headers = { ...TABLE_HEADERS };

      if (this.authService.isUserTenantAdmin()) {
        this.headers.actions = [
          {
            label: 'enroll',
            action: this.addToInventory.bind(this),
          },
          {
            label: 'unroll',
            action: this.removeFromInventory.bind(this),
          },
        ];
      }
    }

    $onInit() {
      this.isLoading = true;
      this.catalogueService.getCatalogueServices({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items.map(item => ({
            ...item,
            custom_tags: item.custom_tags.join(', '),
          }));
        })
        .finally(() => { this.isLoading = false; });
    }

    addToInventory({ _id }) {
      this.catalogueService.addServiceToInventory(_id);
    }

    removeFromInventory({ _id }) {
      this.catalogueService.removeServiceFromInventory(_id);
    }
  },
};

export const catalogueState = {
  parent: 'home',
  name: 'nscatalogue',
  url: '/catalogue',
  component: 'catalogueView',
};

