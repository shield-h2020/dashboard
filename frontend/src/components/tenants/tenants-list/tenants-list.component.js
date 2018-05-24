import template from './tenants-list.html';

const UI_STRINGS = {
  title: 'Secaas clients list',
  create: 'Create',
  modalCreateTitle: 'Create client',
  modalDeleteTitle: 'Delete client',
  confirmDelete: 'Are you sure you want to delete this client?',
  cancel: 'Cancel',
  delete: 'Delete',
};

const TABLE_HEADERS = {
  tenant_name: 'Name',
  _created: 'Created',
};

export const TenantsListComponent = {
  template,
  controller: class TenantsListComponent {
    constructor(TenantsService) {
      'ngInject';

      this.strings = UI_STRINGS;
      this.tenantsService = TenantsService;
      this.createOpen = false;
      this.deleteOpen = false;

      this.removeTenant = this.removeTenant.bind(this);
      this.updateTenant = this.updateTenant.bind(this);
      this.offset = 0;
      this.limit = 25;
      this.filters = {};
      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            func: this.updateTenant,
          },
          {
            label: 'remove',
            func: this.removeTenant,
          },
        ],
      };
    }

    $onInit() {
      this.tenantsService.getTenants({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items;
        });
    }

    toggleCreate() {
      this.createOpen = !this.createOpen;
    }

    toggleDelete() {
      this.deleteOpen = !this.deleteOpen;
    }

    createTenant() {
      this.toggleCreate();
    }

    updateTenant(tenant) {
      this.toggleCreate(tenant);
    }

    removeTenant(tenant) {
      this.toggleDelete(tenant);
    }
  },
};

export const TenantsListState = {
  parent: 'home',
  name: 'tenantslist',
  url: '/tenants',
  component: 'tenantsListView',
};

