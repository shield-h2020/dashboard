import { API_ADDRESS } from 'api/api-config';

const API_USERS = `${API_ADDRESS}/catalogue/users`;

export class UsersService {
  constructor($http, $httpParamSerializer, $q, toastr, AuthService, TenantsService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.httpParamSerializer = $httpParamSerializer;
    this.toast = toastr;
    this.authService = AuthService;
    this.tenantsService = TenantsService;
  }

  getUsers({ page = 1, limit = 25 }, filters = {}) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant(),
      });
    }
    return this.http.get(API_USERS, { params })
      .then(response => response.data._items);
  }

  createUser({ name, password, description, email, group_id }) {
    const params = {};
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant(),
      });
    }

    return this.http.post(API_USERS, {
      name,
      password,
      description,
      email,
      group_id,
    }, { params })
      .catch(() => { this.toast.error('An error occurred'); });
  }

  getRoles(tenantId = this.authService.getTenant()) {
    return this.tenantsService.getTenant(tenantId)
      .then(tenant => tenant.groups.map(group => ({
        text: group.group.description,
        value: group.group.group_id,
      })));
  }

  getTenantName(tenantId) {
    return this.tenantsService.getTenant(tenantId)
      .then(tenant => tenant.tenant_name);
  }

  getTenantInfo(tenantId = this.authService.getTenant()) {
    return this.tenantsService.getTenant(tenantId)
      .then(tenant => ({
        groups: tenant.groups.map(group => ({
          text: group.group.description,
          value: group.group.group_id,
        })),
        tenant_name: tenant.tenant_name,
      }));
  }
}

export default UsersService;
