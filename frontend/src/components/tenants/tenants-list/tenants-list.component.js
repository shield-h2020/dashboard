import { ipValidator } from '@/validators';
import template from './tenants-list.html';

const UI_STRINGS = {
  title: 'Secaas clients',
  tableTitle: 'Secaas clients list',
  create: 'Create',
  update: 'Update',
  modalCreateTitle: 'Create client',
  modalDeleteTitle: 'Delete client',
  confirmDelete: 'Are you sure you want to delete the client',
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
    constructor($q, TenantsService, AuthService, toastr) {
      'ngInject';

      this.q = $q;
      this.strings = UI_STRINGS;
      this.tenantsService = TenantsService;
      this.authService = AuthService;
      this.toast = toastr;
      this.createOpen = false;
      this.deleteOpen = false;

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

      if (this.authService.isUserPlatformAdmin()) {
        this.headers.actions.push({
          label: 'delete',
          action: this.toggleDeleteModal.bind(this),
        });
      }
    }

    $onInit() {
      this.getData();
    }

    getData() {
      this.tenantsService.getTenants({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items;
        });
    }

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
          prevIps: true,
          scope_code: 'shield_scope_tenant',
        };
        this.tenantsService.getTenantIps(tenant.tenant_id)
          .then((data) => {
            if (data) {
              this.currTenant.ip = [...data.ip];
              this.currTenant.ipEtag = data.etag;
            }
          })
          .catch((err) => {
            if (err === 404) {
              this.currTenant.prevIps = false;
            }
            this.currTenant.ip = [];
          });
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

    toggleDeleteModal(tenant) {
      this.currTenant = tenant;
      this.deleteOpen = !this.deleteOpen;
    }

    createTenant() {
      this.toggleCreate();
    }

    updateTenant(tenant) {
      this.toggleCreate(tenant);
    }

    deleteTenant() {
      this.tenantsService.deleteTenant(this.currTenant)
        .then(() => {
          this.toast.success('Client deleted successfully', 'Client delete');
          this.toggleDeleteModal();
          this.getData();
        });
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

