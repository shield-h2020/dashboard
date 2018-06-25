import template from './catalogue.html';
import styles from './catalogue.scss';

const VIEW_STRINGS = {
  title: 'NS catalogue',
  tableTitle: 'Catalogue',
  modalTitle: 'Details',
  modalTitle2: 'Descriptor',
  close: 'Close',
};

const TABLE_HEADERS = {
  custom_tags: 'Tags',
  _id: 'Id',
  _created: 'Created',
};

const MODAL_ENTRIES = {
  _id: 'Id',
  state: 'State',
};

export const CatalogueComponent = {
  template,
  controller: class CatalogueComponent {
    constructor(CatalogueService, AuthService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.modalEntries = MODAL_ENTRIES;
      this.catalogueService = CatalogueService;
      this.authService = AuthService;
      this.createOpen = false;
      this.deleteOpen = false;
      this.detailsOpen = false;
      this.offset = 1;
      this.limit = 25;
      this.isLoading = false;
      this.filters = {};
      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.toggleDetailsModal.bind(this),
          },
        ],
      };

      if (this.authService.isUserTenantAdmin()) {
        this.headers.actions = [
          ...this.headers.actions,
          {
            label: 'enroll',
            action: this.addToInventory.bind(this),
          },
          {
            label: 'withdraw',
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
            custom_tags: 'tbd' || item.custom_tags.join(', '),
          }));
        })
        .finally(() => { this.isLoading = false; });
    }

    addToInventory({ _id }) {
      this.catalogueService.addServiceToInventory(_id);
    }

    removeFromInventory({ _id, _etag }) {
      this.catalogueService.removeServiceFromInventory(_id, _etag);
    }

    toggleDetailsModal(ns) {
      this.ns = ns;
      this.detailsOpen = !this.detailsOpen;
    }
  },
};

export const catalogueState = {
  parent: 'home',
  name: 'nscatalogue',
  url: '/catalogue',
  component: 'catalogueView',
};

