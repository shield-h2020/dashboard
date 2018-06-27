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
  email: 'Email',
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
      if (user) {
        this.newUser = { ...user };
        this.isCreate = false;
      } else {
        this.isCreate = true;
        this.newUser = {
          name: '',
          role: '',
          tenant: this.tenant,
          password: '',
        };
      }
      if (this.createOpen) {
        this.getTenantInfo(this.newUser);
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
      this.usersService.getUsers(this.pagination, this.filters)
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

