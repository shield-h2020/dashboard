import { API_ADDRESS, ACC_ID } from 'api/api-config';

const API_TENANTS = `${API_ADDRESS}/catalogue/tenants`;
const API_TENANT = `${API_TENANTS}/${ACC_ID}`;
const API_TENANT_IPS = `${API_ADDRESS}/tenant_ips`;
const API_TENANT_SCOPES = `${API_ADDRESS}/definitions/tenant_scopes`;

const STRINGS = {
  TENANT_ERROR: 'An error occurred',
  TENANTS_ERROR: 'An error occurred',
};

export class TenantsService {
  constructor($http, $q, toastr, AuthService) {
    'ngInject';

    this.q = $q;
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
      .catch(() => { this.toast.error(STRINGS.TENANT_ERROR); });
  }

  updateTenant({ tenant_id, tenant_name, description, scope_code }) {
    return this.http.put(API_TENANT.replace(ACC_ID, tenant_id),
      { tenant_name, description, scope_code })
      .catch(() => { this.toast.error(STRINGS.TENANT_ERROR); });
  }

  updateTenantAndIps({ tenant_id, tenant_name, _etag, description, scope_id, ip }) {
    return this.http.put(API_TENANT.replace(ACC_ID, tenant_id),
      { tenant_name, description, scope_id }, { headers: { 'if-match': _etag } })
      .then((response) => {
        if (ip.length) {
          return this.updateTenantIps(response.data.tenant_id, ip)
        }
        return this.q.resolve('');
      })
      .catch(() => { this.toast.error(STRINGS.TENANT_ERROR); });
  }

  createTenant({ tenant_name, description, scope_id }) {
    return this.http.post(API_TENANTS, { tenant_name, description, scope_id })
      .catch(() => { this.toast.error(STRINGS.TENANT_ERROR); });
  }

  createTenantAndIps({ tenant_name, description, scope_id, ip }) {
    return this.http.post(API_TENANTS, { tenant_name, description, scope_id })
      .then((response) => {
        if (ip.length) {
          return this.updateTenantIps(response.data.tenant_id, ip);
        }

        return this.q.resolve('');
      })
      .catch(() => { this.toast.error(STRINGS.TENANT_ERROR); });
  }

  updateTenantIps(tenantId, ip) {
    return this.http.post(API_TENANT_IPS, {
      ip,
      tenant_id: tenantId,
    })
    .catch(() => { this.toast.error(STRINGS.TENANT_ERROR); });
  }

  getTenantIps(tenantId) {
    return this.http.get(`${API_TENANT_IPS}/${tenantId}`)
      .then(response => response.data.ip)
      .catch(() => {
        this.toast.error(STRINGS.TENANT_ERROR);
        return this.q.reject('error');
      });
  }

  getScopeId(scopeCode) {
    return this.http.get(`${API_TENANT_SCOPES}/${scopeCode}`)
      .then(response => response.data._id);
  }
}

export default TenantsService;
