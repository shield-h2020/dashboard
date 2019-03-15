import { ipValidator } from '@/validators';
import template from './tenants-list.html';
import styles from '../tenants.scss';

const VIEW_STRINGS = {
  title: 'SecaaS clients',
  tableTitle: 'SecaaS clients list',
  create: 'Create',
  update: 'Update',
  modalCreateTitle: 'Create client',
  modalUpdateTitle: 'Update client',
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
      this.viewStrings = VIEW_STRINGS;
      this.tenantsService = TenantsService;
      this.authService = AuthService;
      this.toast = toastr;
      this.createOpen = false;
      this.deleteOpen = false;
      this.updateTenantForm = false;
      this.createTenantForm = false;
      this.disabledCreate = false;
      this.styles = styles;

      this.updateTenant = this.updateTenant.bind(this);
      this.ipValidator = ipValidator;
      this.offset = 0;
      this.limit = 25;
      this.filters = {};
      this.dropdown_tenant_scope = [];
      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'update',
            action: this.updateTenant,
          },
        ],
      };
      this.isCreate = true;
      this.isCreateIps = false;

      if (this.authService.isUserPlatformAdmin()) {
        this.headers.actions.push({
          label: 'delete',
          action: this.toggleDeleteModal.bind(this),
        });
      }
    }

    $onInit() {
      this.getData();
      this.getAllScope();
    }

    getData() {
      this.filters = {};
      this.tenantsService.getTenants({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items;
        });
    }

    getAllScope() {
      this.tenantsService.getAllScope()
        .then(data =>
          data.forEach((item) => 
            this.dropdown_tenant_scope.push({          
              description: item.name,
              scope_id: item._id,
              scope_code: item.code,
            }),
          ),
        );
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
            } else {
              this.currTenant.ip = [];
              this.currTenant.ipEtag = null;
              this.currTenant.prevIps = false;
            }
          });
      } else {
        this.currTenant = {
          tenant_name: '',
          client_description: '',
          tenant: null,
          name: '',
          email: '',
          client: '',
          password: '',
          description: '',
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
      this.updateTenantForm = false;
      this.toggleCreate();
    }

    updateTenant(tenant) {
      this.updateTenantForm = true;
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
        this.disabledCreate = true;
        //httpPromise = this.tenantsService.createTenantAndIps(this.currTenant);
        this.tenantsService.createTenant(this.currTenant)
          .then(data => this.newTenantInfo = data)
          .finally(() => this.getGroupId(this.newTenantInfo));
      } else {
        if(this.isCreateIps) {
          httpPromise = this.tenantsService.updateTenantAndCreateIps(this.currTenant);
        } else {
          httpPromise = this.tenantsService.updateTenantAndIps(this.currTenant);
        } 
      }
      if (!this.isCreate) {
        httpPromise.then(() => {
          this.toggleCreate();
          this.getData();
        });
      }
    }

    getGroupId() {
      const arrayofGroups = [];
      this.filters = { scope_id: this.currTenant.tenant.scope_id };
      this.tenantsService.getTenantScopeGroups(this.filters)
        .then(data => 
          data.forEach(data => data.groups.forEach(
            group => arrayofGroups.push(group),
          )),
        )
        .finally(() => this.findTenantGroup(arrayofGroups));
    }

    findTenantGroup(groups) {
      const tenantGroups = [];
      for (const group of groups) {
        this.tenantsService.getTenantGroups(group)
          .then((data) => {
            tenantGroups.push({ code: data.code, tenant_id: data._id })
          });
      }
      setTimeout(() => {
        this.getTenantInfo(tenantGroups);
      }, 2000);
    }

    getTenantInfo(tenantGroups) {
      // Get Comparation
      const code = this.currTenant.tenant.scope_code;
      let find = null;
      switch (code) {
        case 'shield_scope_tenant':
          find = tenantGroups.find(tenant => tenant.code === 'shield-client-admins');
          break;
        case 'shield_scope_developer':
          find = tenantGroups.find(tenant => tenant.code === 'shield-developers');
          break;
        case 'shield_scope_cyberagent':
          find = tenantGroups.find(tenant => tenant.code === 'shield-cyberagents');
          break;
        default:
          find; 
          break;
      }
      if (find) {
        let findGroup = null;
        this.filters = { tenant_id: this.newTenantInfo.tenant_id };
        this.tenantsService.getTenants({}, this.filters)
          .then(data => 
            data.forEach((tenant) => 
            findGroup = tenant.groups.find(item => item.group.name === find.code)
            )
          )
          .finally(() => {
            this.createUser(findGroup.group.group_id);
          });
      }
    }

    createUser(groupId) {
      const { name, password, description, email } = this.currTenant;
      const user = {
        name: name,
        password: password,
        description: description,
        email: email,
        group_id: groupId,
      };
      this.tenantsService.createUser(user, this.newTenantInfo.tenant_id)
        .then(() => {
          this.disabledCreate = false;
          this.toggleCreate();
          this.getData();
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

