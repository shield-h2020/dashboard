import { API_ADDRESS } from 'api/api-config';

const API_USERS = `${API_ADDRESS}/catalogue/users`;

export class UsersService {
  constructor($http, $httpParamSerializer, $q, toastr, AuthService, TenantsService, ErrorHandleService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.httpParamSerializer = $httpParamSerializer;
    this.toast = toastr;
    this.authService = AuthService;
    this.tenantsService = TenantsService;
    this.errorHandleService = ErrorHandleService;
  }

  getUsers({ page = 1, limit = 25 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
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
      .catch(this.errorHandleService.handleHttpError);
  }

  updateUser({ user_id, name, password, tenant_id, description, email, group_id, _etag }) {
    return this.http.put(`${API_USERS}/${user_id}`, {
      name,
      password,
      tenant_id,
      description,
      email,
      group_id,
    }, { headers: { 'if-match': _etag } })
      .then(this.errorHandleService.handleHttpSuccess)
      .catch(this.errorHandleService.handleHttpError);
  }

  deleteUser({ user_id, _etag }) {
    return this.http.delete(`${API_USERS}/${user_id}`, {
      headers: { 'if-match': _etag } })
      .then(this.errorHandleService.handleHttpSuccess)
      .catch(this.errorHandleService.handleHttpError);
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
