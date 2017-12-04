
export const searchinput = {
  placeholder: 'Start typing to search…',
};

export const APP_STRINGS = {
  common: {
    save: 'Save',
    saving: 'Saving',
    create: 'Create',
    creating: 'Creating',
    cancel: 'Cancel',
    back: 'Back',
    delete: 'Delete',
    update: 'Update',
    disable: 'Disable',
    enable: 'Enable',
  },
  components: {
    search: 'Start typing to search...',
    toastr: {
      success: 'was successful',
      warning: '',
      alert: 'has failed',
      info: '',
    },
  },
  login: {
    username: 'username',
    password: 'password',
    tenant: 'tenant',
    login: 'login',
    error: 'Incorrect username, password or tenant name. ' +
      'Please review your information and try again.',
  },
  menu: {
    labels: {
      global: 'Global options',
    },
    user: {
      main: ['Dashboard', 'NS\'s / E2E\'s'],
    },
    admin: {
      main: ['Dashboard', 'NS\'s / E2E\'s', 'Users'],
      global: ['Tenants', 'Catalogue', 'TAL Scripts', 'Intelligence', 'Monitor', 'Topology'],
      catalogue: ['SDN Apps', 'VNF Apps', 'PNF Apps'],
    },
  },
  views: {
    topology: {
      title: 'Network Topology',
    },
    userslist: {
      title: 'Users',
      select: [
        {
          value: '10',
          label: 'Show 10 items',
        },
        {
          value: '20',
          label: 'Show 20 items',
        },
      ],
      table: {
        title: 'users list',
        headers: ['Id', 'Username', 'Role', 'Status'],
        actions: {
          edit: 'Edit',
          enable: 'Enable',
          disable: 'Disable',
        },
      },
      button: 'Add new user',
    },
    useredit: {
      title: 'Edit user',
      subtitles: ['General information', 'Account information'],
      inputs: {
        username: 'Username *',
        password: 'Password',
        passwordconf: 'Password confirmation',
        role: 'Role *',
        status: 'Status *',
        description: 'Description',
      },
    },
    tenantslist: {
      title: 'Tenants',
      select: [
        {
          value: '10',
          label: 'Show 10 items',
        },
        {
          value: '20',
          label: 'Show 20 items',
        },
      ],
      table: {
        title: 'Tenants list',
        headers: ['Id', 'Name', 'Description'],
        actions: {
          edit: 'Edit',
        },
      },
      button: 'Add new tenant',
    },
    tenantedit: {
      title: 'Edit tenant',
      subtitles: ['General information'],
      inputs: {
        name: 'Tenant name *',
        description: 'Tenant description',
      },
    },
  },
};

export default APP_STRINGS;
