const ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',
  TENANT_ADMIN: 'TENANT_ADMIN',
  BASIC: 'BASIC',
};

export class DataService {
  constructor() {
    this.roles = ROLES;
    this.users = [
      {
        id: 1,
        name: 'Ricardo Preto',
        username: 'rpreto',
        password: '123qwe',
        tenant: 1,
        role: ROLES.TENANT_ADMIN,
      },
      {
        id: 2,
        name: 'Telmo Alves',
        username: 'tmalves',
        password: '123qwe',
        tenant: 1,
        role: ROLES.BASIC,
      },
      {
        id: 3,
        name: 'Filipe Ferreira',
        username: 'fcferreira',
        password: '123qwe',
        tenant: 1,
        role: ROLES.BASIC,
      },
      {
        name: 'Pedro Diogo',
        username: 'pdiogo',
        password: '123qwe',
        tenant: 2,
        role: ROLES.BASIC,
      },
      {
        id: 4,
        name: 'Pedro Lobo',
        username: 'plobo',
        password: '123qwe',
        tenant: 2,
        role: ROLES.BASIC,
      },
      {
        id: 5,
        name: 'SHIELD',
        username: 'shield',
        password: '123qwe',
        tenant: 3,
        role: ROLES.SUPER_ADMIN,
      },
    ];

    this.tenants = [
      {
        id: 1,
        name: 'Ubiwhere',
        desc: '',
      },
      {
        id: 2,
        name: 'Playnify',
        desc: '',
      },
      {
        id: 3,
        name: 'SHIELD',
        desc: '',
      },
    ];

    this.getRoles = this.getRoles.bind(this);
    this.getTenants = this.getTenants.bind(this);
    this.getUsers = this.getUsers.bind(this);
    this.addUser = this.addUser.bind(this);
  }

  getRoles() {
    return this.roles;
  }

  getTenants() {
    return this.tenants;
  }

  getUsers() {
    return this.users;
  }

  updateUser(user) {
    const found = this.getUser(user.id);
    if (found) {
      const idx = this.users.indexOf(found);
      this.users[idx] = { ...user };
    }
  }

  addUser(user) {
    this.users.push(user);
  }

  removeUser(id) {
    try {
      const user = this.getUser(id);
      const idx = this.users.indexOf(user);
      this.users.splice(idx, 1);
    } catch (err) {

    }
  }

  getUser(id) {
    const found = this.users.find(user => user.id === id);
    if (found) {
      return found;
    }

    throw Error('Not found');
  }
}

export default DataService;
