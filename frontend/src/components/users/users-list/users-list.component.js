import template from './users-list.html';

const VIEW_STRINGS = {
  title: 'Users',
  tableTitle: 'Users list',
  modalCreateTitle: 'Create user',
  modalUpdateTitle: 'User information',
  modalDeleteTitle: 'Delete user',
  confirmDelete: 'Are you sure you want to delete the user ',
  create: 'Create',
  update: 'Update',
  cancel: 'Cancel',
  delete: 'Delete',
};

const TABLE_HEADERS = {
  name: 'Name',
  tenant_name: 'SecaaS client',
  roles: 'Role',

  // secaaas_client,
  // roles
  // remove: email
};

export const UsersListComponent = {
  template,
  bindings: {
    tenant: '<',
  },
  controller: class UsersListComponent {
    constructor($scope, toastr, UsersService, TenantsService, AuthService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.toast = toastr;
      this.scope = $scope;
      this.usersService = UsersService;
      this.tenantsService = TenantsService;
      this.authService = AuthService;
      this.createOpen = false;
      this.deleteOpen = false;
      this.toggleCreate = this.toggleCreate.bind(this);
      this.selectedUser = null;
      this.isCreate = true;
      this.tableHeaders = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'update',
            action: this.toggleCreate,
          },
          {
            label: 'delete',
            action: this.toggleDeleteModal.bind(this),
          },
        ],
      };
      // Table control
      this.pagination = {
        offset: 0,
        limit: 20,
      };
      this.filters = {};
    }

    $onInit() {
      this.isPlatformAdmin = this.authService.isUserPlatformAdmin();
      this.getData();
    }

    toggleCreate(user) {
      this.createOpen = !this.createOpen;
      if(!this.createOpen)
        return;
      
      if (user) {
        this.newUser = { ...user };
        this.newUser.password = '';
        this.newUser.tenant = this.newUser.tenant_name;
        this.roles = this.newUser.groups;
        this.isCreate = false;
      } else {
        /* When we add support for user addition by super admin, we
        will have to edit this logic. We first have to check if i'm a 
        super admin or not. If not, the following logic is up to date.
        If i am a super admin, we have to unlock tenant dropdown with
        a list of available tenants, and on change of this dropdown
        we have to update available roles.
        get tenant list:
        http://{{ dashboard_api}}/catalogue/tenants
        get tenant roles: 
        http://{{ dashboard_api}}/catalogue/tenants/674568b4584c43d19f441b996f0ce3cc
        */
        this.usersService.getRoles()
        .then((items) => {
          this.roles = items;
          this.isCreate = true;
          this.newUser = {
            name: '',
            role: '',
            tenant: this.tenant,
            password: '',
          };
        })
        .catch(() => {
          console.log("Error getting users");
        });
      }
    }

    toggleDeleteModal(user) {
      this.selectedUser = user;
      this.deleteOpen = !this.deleteOpen;
    }

    setNewUser(property, val) {
      this.newUser[property] = val;
    }

    createOrUpdateUser() {
      if (this.isCreate) {
        this.createUser();
      } else {
        this.updateUser();
      }
    }

    createUser() {
      if (this.newUser) {
        this.usersService.createUser(this.newUser)
        .then(() => {
          this.getData();
          this.toggleCreate();
          this.newUser = null;
        });
      }
    }

    updateUser() {
      this.usersService.updateUser(this.newUser)
        .then(() => {
          this.getData();
          this.toggleCreate();
          this.newUser = null;
        });
    }

    deleteUser() {
      this.usersService.deleteUser(this.selectedUser)
        .then(() => {
          this.toast.success('Client deleted successfully', 'Client delete');
          this.toggleDeleteModal();
          this.getData();
        });
    }

    getTenantInfo({ tenant_id }) {
      this.usersService.getTenantInfo(tenant_id)
        .then((info) => {
          this.newUser.tenant = info.tenant_name;
          this.roles = info.groups;
        });
    }

    getData() {
      this.loading = true;
      this.users = [];
      this.usersService.getUsersWithTenant(this.pagination, this.filters)
        .then((items) => {
          this.users = items;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    }
  },
};

export const UsersListState = {
  parent: 'home',
  name: 'userslist',
  url: '/users',
  component: 'usersListView',
  resolve: {
    tenant: ['AuthService', AuthService => AuthService.getTenantName()],
  },
};

