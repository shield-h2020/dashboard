import template from './inventory.html';

const UI_STRINGS = {
  title: 'NS inventory',
  tableTitle: 'Inventory',
};

const TABLE_HEADERS = {
  custom_tags: 'Tags',
  ref_id: 'Id',
  _created: 'Created',
};

export const InventoryComponent = {
  template,
  controller: class InventoryComponent {
    constructor(InventoryService) {
      'ngInject';

      this.strings = UI_STRINGS;
      this.inventoryService = InventoryService;
      this.createOpen = false;
      this.deleteOpen = false;

      this.offset = 0;
      this.limit = 25;
      this.isLoading = false;
      this.filters = {};
      this.headers = { ...TABLE_HEADERS };
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
            custom_tags: item.custom_tags.join(', '),
          }));
        })
        .finally(() => { this.isLoading = false; });
    }
  },
};

export const inventoryState = {
  parent: 'home',
  name: 'nsinventory',
  url: '/inventory',
  component: 'inventoryView',
};

