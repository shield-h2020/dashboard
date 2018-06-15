import { API_ADDRESS, ACC_ID } from 'api/api-config';

const TENANTS_BASE = `${API_ADDRESS}/tenants`;
const TENANTS_API = {
  ALL: TENANTS_BASE,
  ONE: `${TENANTS_BASE}/${ACC_ID}`,
};

const API_TENANTS = `${API_ADDRESS}/catalogue/tenants`;
const API_TENANT = `${API_TENANTS}/${ACC_ID}`;

const STRINGS = {
  TENANT_ERROR: 'An error occurred',
  TENANTS_ERROR: 'An error occurred',
};

export class TenantsService {
  constructor($http, toastr, AuthService) {
    'ngInject';

    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
  }

  getTenants({ page, limit } = { page: 0, limit: 25 }, filters = {}) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_TENANTS, { params })
      .then(response => response.data._items);
  }

  getTenant(id) {
    return this.http.get(API_TENANT.replace(ACC_ID, id))
      .then(response => response.data)
      .catch(() => { this.toast.error(STRINGS.USER_ERROR); });
  }
}

export default TenantsService;
