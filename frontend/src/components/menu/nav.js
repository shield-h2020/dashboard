const TENANT_ADMIN = 'shield_tenant_admin';
const SUPER_ADMIN = 'admin';
const TENANT_USER = 'shield_tenant_user';
const DEVELOPER = 'shield_developer';

export const MENU_ENTRIES = [
  {
    text: 'Client options',
    roles: [TENANT_ADMIN, SUPER_ADMIN, TENANT_USER],
  },
  {
    text: 'User Management',
    route: 'userslist',
    roles: [TENANT_ADMIN, SUPER_ADMIN],
  },
  {
    text: 'Security Incidents',
    route: 'incidentslist',
    roles: [TENANT_ADMIN, SUPER_ADMIN, TENANT_USER],
  },
  {
    text: 'Global options',
  },
  {
    text: 'SecaaS Client Management',
    route: 'tenantslist',
    roles: [SUPER_ADMIN],
  },
  {
    text: 'VNSFs Store',
    route: 'vnsfslist',
    roles: [TENANT_ADMIN, SUPER_ADMIN, DEVELOPER],
  },
  {
    text: 'NS Catalogue',
    route: 'nscatalogue',
    roles: [TENANT_ADMIN, SUPER_ADMIN],
  },
  {
    text: 'NS Inventory',
    route: 'nsinventory',
    roles: [TENANT_ADMIN, TENANT_USER, SUPER_ADMIN],
  },
  {
    text: 'Onboard validation',
    route: 'validations',
    roles: [SUPER_ADMIN, DEVELOPER],
  },
];

export default MENU_ENTRIES;
