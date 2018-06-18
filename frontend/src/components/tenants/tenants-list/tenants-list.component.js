import { ipValidator } from '@/validators';
import template from './tenants-list.html';

const UI_STRINGS = {
  title: 'Secaas clients',
  tableTitle: 'Secaas clients list',
  create: 'Create',
  update: 'Update',
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
    constructor($q, TenantsService) {
      'ngInject';

      this.q = $q;
      this.strings = UI_STRINGS;
      this.tenantsService = TenantsService;
      this.createOpen = false;
      this.deleteOpen = false;

      this.removeTenant = this.removeTenant.bind(this);
      this.updateTenant = this.updateTenant.bind(this);
      this.ipValidator = ipValidator;
      this.offset = 0;
      this.limit = 25;
      this.filters = {};
      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'update',
            action: this.updateTenant,
          },
        ],
      };
    }

    $onInit() {
      this.getItems();
    }

    getItems() {
      this.tenantsService.getTenants({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items;
        });
    }

    /**
     * Create and update need a scope id instead of scope code. Also if update,
     * the header { headers: { 'if-match': etag } } etag should be in the list item.
     * since multiple promises need to be resolved, best aproach should be q.all
     */

    toggleCreate(tenant) {
      this.createOpen = !this.createOpen;
      if (this.createOpen) {
        this.setCurrentTenant(tenant);
      }
    }

    setCurrentTenant(tenant) {
      this.isCreate = !tenant;
      if (tenant) {
        this.currTenant = {
          ...tenant,
          scope_code: 'shield_scope_tenant',
        };
        this.tenantsService.getTenantIps(tenant.tenant_id)
          .then((ip) => {
            if (ip) this.currTenant.ip = [...ip];
          })
          .catch(() => { this.currTenant.ip = []; });
      } else {
        this.currTenant = {
          tenant_name: '',
          description: '',
          scope_code: 'shield_scope_tenant',
          ip: [],
        };
        this.tenantsService.getScopeId(this.currTenant.scope_code)
          .then((scopeId) => {
            if (scopeId) {
              this.currTenant.scope_id = scopeId;
            }
          });
      }
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

    changeCurrTenant(key, value) {
      this.currTenant[key] = Array.isArray(value) ? [...value] : value;
    }

    createOrUpdateTenant() {
      let httpPromise;
      if (this.isCreate) {
        httpPromise = this.tenantsService.createTenantAndIps(this.currTenant);
      } else {
        httpPromise = this.tenantsService.updateTenantAndIps(this.currTenant);
      }

      httpPromise.then(() => {
        this.toggleCreate();
        this.getItems();
      });
    }
  },
};

export const TenantsListState = {
  parent: 'home',
  name: 'tenantslist',
  url: '/tenants',
  component: 'tenantsListView',
};

