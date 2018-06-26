import template from './inventory.html';
import styles from './inventory.scss';

const VIEW_STRINGS = {
  title: 'NS inventory',
  tableTitle: 'Inventory',
  modalTitle: 'NS Details',
  close: 'Close',
};

const TABLE_HEADERS = {
  capabilities: 'Capabilities',
  ref_id: 'Id',
  _created: 'Created',
};

const MODAL_ENTRIES = {
  _id: 'Id',
  custom_tags: 'Custom_tags',
  _created: 'Created',
}

export const InventoryComponent = {
  template,
  controller: class InventoryComponent {
    constructor(InventoryService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.modalEntries = MODAL_ENTRIES;
      this.styles = styles;
      this.inventoryService = InventoryService;
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
            action: this.toggleNSDetails.bind(this),
          },
        ],
      };
      this.modalOpen = false;
    }

    $onInit() {
      this.isLoading = true;
      this.inventoryService.getInventoryServices({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items.map(item => ({
            ...item,
            capabilities: item.manifest['manifest:ns'].properties.capabilities.join(', '),
          }));
        })
        .finally(() => { this.isLoading = false; });
    }

    toggleNSDetails(ns) {
      this.ns = ns;
      this.modalOpen = !this.modalOpen;
    }
  },
};

export const inventoryState = {
  parent: 'home',
  name: 'nsinventory',
  url: '/inventory',
  component: 'inventoryView',
};

