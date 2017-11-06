import { PORT, SOCKET_PORT, STORE_PORT } from '../api-access-strings.js'

/*
* The HOST URL is picked up according to the environment defined at build time.
* If a development build is made the HOST is given by variable replacement.
* Else the HOST is read from the window's location.
*/
const BACKEND_HOST = window.location.hostname;
const ADDRESS = __API_URL__ || BACKEND_HOST;
const SOCKET_URL = BACKEND_HOST;
const STORE_URL = BACKEND_HOST;

const baseUrl = `http://${ADDRESS}`;
const socketsUrl = `ws://${SOCKET_URL}`;
const storeUrl = `http://${STORE_URL}`;

const strings = {
  common: '/nbi/identity/api',
  auth: '/nbi/auth/api/login/',
  catalogue: '/nbi/catalogue/api',
  roles: '/roles/',
  tenants: '/tenants/',
  users: '/users/',
  packages: '/packages/',
  apps: {
    enable: '/enable',
    disable: '/disable',
    monitoring: '/app-monitoring',
    configuration: '/app-configuration',
    description: '/app-description',
    info: '/app-info',
  },
};
const topologyEndpoint = '/topology/subscribe';

export const APP_ADDRESSES = {
  authAddress: `${baseUrl}:${PORT}`,
  baseAddress: `${baseUrl}:${PORT}`,
  cataAddress: `${baseUrl}:${PORT}`,
  sockAddress: `${socketsUrl}:${SOCKET_PORT}`,
  storeAddress: `${storeUrl}:${STORE_PORT}`,
};

export const ACCESSORS = {
  id: '{#id}',
  nId: '{##id}',
};

export const API_STRINGS = {
  auth: {
    base: strings.auth,
  },
  roles: {
    all: strings.common + strings.roles,
    one: `${strings.common}${strings.roles}${ACCESSORS.id}`,
  },
  users: {
    all: `${strings.common}${strings.tenants}${ACCESSORS.id}${strings.users}`,
    one: `${strings.common}${strings.tenants}${ACCESSORS.id}${strings.users}${ACCESSORS.nId}`,
  },
  tenants: {
    all: strings.common + strings.tenants,
    one: `${strings.common}${strings.tenants}${ACCESSORS.id}`,
  },
  catalogue: {
    all: strings.catalogue + strings.packages,
    one: `${strings.catalogue}${strings.packages}${ACCESSORS.id}`,
    oneDisable: `${strings.catalogue}${strings.packages}${ACCESSORS.id}${strings.apps.disable}`,
    oneEnable: `${strings.catalogue}${strings.packages}${ACCESSORS.id}${strings.apps.enable}`,
    oneMonitor: `${strings.catalogue}${strings.packages}${ACCESSORS.id}${strings.apps.monitoring}`,
    oneConfig: `${strings.catalogue}${strings.packages}${ACCESSORS.id}${strings.apps.configuration}`,
    oneDesc: `${strings.catalogue}${strings.packages}${ACCESSORS.id}${strings.apps.description}`,
    oneInfo: `${strings.catalogue}${strings.packages}${ACCESSORS.id}${strings.apps.info}`,
  },
  topology: `${topologyEndpoint}`,
};

const INCIDENTS_BASE = `${APP_ADDRESSES.baseAddress}/policies`;
export const INCIDENTS_API = {
  ALL: INCIDENTS_BASE,
  ONE: `${INCIDENTS_BASE}/{#id}`,
};

const INCIDENTS_SOCKET_BASE = `${APP_ADDRESSES.sockAddress}/policy`;
export const INCIDENTS_SOCKET_API = {
  CONNECT: INCIDENTS_SOCKET_BASE,
};

const VNSF_BASE = `${APP_ADDRESSES.storeAddress}/vnsfs`;
export const VNSF_API = {
  ALL: VNSF_BASE,
  ONE: `${VNSF_BASE}/{#id}`,
  ONE_UPLOAD: `${VNSF_BASE}`,
};

export default API_STRINGS;
