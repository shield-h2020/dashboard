import template from './users-list.html';

const UI_STRINGS = {
  title: 'Users',
  tableTitle: 'Users list',
  modalCreateTitle: 'Create user',
  modalDeleteTitle: 'Delete user',
  confirmDelete: 'Are you sure you want to delete this user?',
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
    constructor($scope, UsersService, TenantsService, AuthService) {
      'ngInject';

      this.strings = UI_STRINGS;
      this.scope = $scope;
      this.usersService = UsersService;
      this.tenantsService = TenantsService;
      this.authService = AuthService;
      this.createOpen = false;
      this.deleteOpen = false;
      this.toggleDelete = this.toggleDelete.bind(this);
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
            action: this.toggleDelete,
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
      this.getUsers();
      if (!this.isPlatformAdmin) {
        this.getRoles();
      }
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
    }

    toggleDelete(user) {
      this.deleteOpen = !this.deleteOpen;
      if (user) {
        this.selectedUser = user;
      }
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
          this.getUsers();
          this.toggleCreate();
          this.newUser = null;
        });
      }
    }

    updateUser() {
      this.usersService.updateUser(this.newUser)
        .then(() => {
          this.getUsers();
          this.toggleCreate();
          this.newUser = null;
        });
    }

    removeUser() {
      this.usersService.deleteUser(this.selectedUser)
        .then(() => {
          this.toggleDelete();
        });
    }

    getRoles() {
      this.usersService.getRoles()
        .then((roles) => {
          this.roles = roles;
        });
    }

    getUsers() {
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

