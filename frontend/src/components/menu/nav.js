import { TENANT_ADMIN, SUPER_ADMIN, TENANT_USER, DEVELOPER, CYBER_AGENT } from '../../strings/role-strings';

export const MENU_ENTRIES = [
  /*{
    text: 'Client options',
    roles: [TENANT_ADMIN, SUPER_ADMIN, TENANT_USER],
  },*/
  {
    text: 'Threats',
    route: 'dashboard',
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
    text: 'Attestation',
    route: 'attestation',
    roles: [TENANT_ADMIN, SUPER_ADMIN],
  },
  {
    text: 'vNSF notifications',
    route: 'vnsfnotificationslist',
    roles: [TENANT_ADMIN, TENANT_USER, SUPER_ADMIN],
  },
  /* {
    text: 'Global options',
  } */
  {
    text: 'SecaaS Client Management',
    route: 'tenantslist',
    roles: [SUPER_ADMIN],
  },
  {
    text: 'vNSF Catalogue',
    route: 'vnsfslist',
    roles: [SUPER_ADMIN, DEVELOPER],
  },
  {
    text: 'NS Catalogue',
    route: 'nscatalogue',
    roles: [TENANT_ADMIN, SUPER_ADMIN],
  },
  {
    text: 'NS Inventory',
    route: 'nsinventory',
    roles: [TENANT_ADMIN],
  },
  {
    text: 'Billing',
    route: 'billing',
    roles: [TENANT_ADMIN, SUPER_ADMIN, DEVELOPER],
  },
  {
    text: 'Activity',
    route: 'activity',
    roles: [TENANT_ADMIN, SUPER_ADMIN, DEVELOPER],
  },
  {
    text: 'Onboard validations',
    route: 'validations',
    roles: [SUPER_ADMIN, DEVELOPER],
  },
  {
    text: 'CERT Dashboard',
    route: 'cert',
    roles: [SUPER_ADMIN, CYBER_AGENT],
  },
];

export default MENU_ENTRIES;
