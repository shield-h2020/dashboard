import { API_ADDRESS, ACC_ID } from 'api/api-config';

const API_TENANTS = `${API_ADDRESS}/catalogue/tenants`;
const API_TENANT = `${API_TENANTS}/${ACC_ID}`;
const API_TENANT_IPS = `${API_ADDRESS}/tenant_ips`;
const API_TENANT_SCOPES = `${API_ADDRESS}/definitions/tenant_scopes`;
const API_TENANT_GROUPS = `${API_ADDRESS}/definitions/tenant_groups`;
const API_TENANT_SCOPE_GROUPS = `${API_ADDRESS}/definitions/tenant_scope_groups`;
const API_USERS = `${API_ADDRESS}/catalogue/users`;

const STRINGS = {
  TENANT_ERROR: 'An error occurred',
  TENANTS_ERROR: 'An error occurred',
};

const TOAST_STRINGS = {
  UPDATE_SUCCESS_TENANT: {
    TITLE: 'SecaaS client updated',
    MESSAGE: 'Client updated successfully',
  },
  CREATE_SUCCESS_TENANT: {
    TITLE: 'SecaaS client created',
    MESSAGE: 'Client created successfully',
  },
  CREATE_SUCCESS_IP: {
    TITLE: 'Client IP association created',
    MESSAGE: 'Association created successfully',
  },
  UPDATE_SUCCESS_IP: {
    TITLE: 'Client IP association updated',
    MESSAGE: 'Association updated successfully',
  },
  CREATE_ERROR_IP: {
    TITLE: 'Client IP association creation failed',
    MESSAGE: 'Client IP association creation error',
  },
  UPDATE_ERROR_IP: {
    TITLE: 'Client IP association update failed',
    MESSAGE: 'Client IP association update error',
  },
  GET_ERROR_IP: {
    TITLE: 'Client IP association retrieval failed',
    MESSAGE: 'Client IP association retrieval error',
  },
};

export class TenantsService {
  constructor($http, $q, toastr, AuthService, ErrorHandleService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
    this.errorHandleService = ErrorHandleService;
  }

  getTenants({ page, limit } = { page: 0, limit: 25 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };

    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_TENANTS, { params })
      .then(response => response.data._items);
  }

  getTenant(id) {
    const params = { nocache: (new Date()).getTime() };

    return this.http.get(API_TENANT.replace(ACC_ID, id), { params })
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  deleteTenant({ tenant_id, _etag }) {
    return this.http.delete(API_TENANT.replace(ACC_ID, tenant_id), {
      headers: { 'if-match': _etag }
    });
  }

  updateTenantAndIps({
    tenant_id,
    tenant_name,
    _etag,
    description,
    scope_id,
    ip,
    prevIps,
    ipEtag,
    groups,
  }) {
    return this.http.put(API_TENANT.replace(ACC_ID, tenant_id),
      { tenant_name, description, scope_id, groups }, { headers: { 'if-match': _etag } })
      .then(() => {
        this.toast.info(TOAST_STRINGS.UPDATE_SUCCESS_TENANT.MESSAGE,
          TOAST_STRINGS.UPDATE_SUCCESS_TENANT.TITLE);
        if (ip.length) {
          if (prevIps) {
            return this.updateTenantIps(tenant_id, ip, ipEtag);
          }
          return this.createTenantIps(tenant_id, ip);
        }
        return this.q.resolve('');
      })
      .catch(() => {
        this.toast.error(STRINGS.TENANT_ERROR);
        return this.q.resolve('');
      });
  }

  createTenantAndIps({ tenant_name, description, scope_id, ip }) {
    return this.http.post(API_TENANTS, { tenant_name, description, scope_id })
      .then((response) => {
        this.toast.success(TOAST_STRINGS.CREATE_SUCCESS_TENANT.MESSAGE,
          TOAST_STRINGS.CREATE_SUCCESS_TENANT.TITLE);
        if (ip.length) {
          return this.createTenantIps(response.data.tenant_id, ip);
        }

        return this.q.resolve('');
      })
      .catch(() => { this.toast.error(STRINGS.TENANT_ERROR); });
  }

  createTenantIps(tenantId, ip) {
    return this.http.post(API_TENANT_IPS, {
      ip,
      tenant_id: tenantId,
    })
      .catch(() => {
        this.toast.error(TOAST_STRINGS.CREATE_ERROR_IP.MESSAGE,
          TOAST_STRINGS.CREATE_ERROR_IP.TITLE);
      });
  }

  updateTenantIps(tenantId, ip, etag) {
    return this.http.patch(`${API_TENANT_IPS}/${tenantId}`, {
      ip,
    }, { headers: { 'if-match': etag } })
      .catch(() => {
        this.toast.error(TOAST_STRINGS.UPDATE_ERROR_IP.MESSAGE,
          TOAST_STRINGS.UPDATE_ERROR_IP.TITLE);
      });
  }

  getTenantIps(tenantId) {
    const params = { nocache: (new Date()).getTime() };

    return this.http.get(`${API_TENANT_IPS}/${tenantId}`, { params })
      .then(response => ({ ip: response.data.ip, etag: response.data._etag }))
      .catch(response => {

        if (response.status != 404)
          this.errorHandleService.handleHttpError(response);
      });
  }

  getScopeId(scopeCode) {
    const params = { nocache: (new Date()).getTime() };

    return this.http.get(`${API_TENANT_SCOPES}/${scopeCode}`, { params })
      .then(response => response.data._id);
  }

  getAllScope() {
    const params = {
      nocache: (new Date()).getTime(),
      where: {
        'code': {
           '$in': [
             'shield_scope_tenant',
             'shield_scope_developer',
             'shield_scope_cyberagent',
           ]
        }, 
      },
     };
    return this.http.get(API_TENANT_SCOPES, { params })
      .then(response => response.data._items);
  }

  createTenant(data) {
    const body = {
      tenant_name: data.tenant_name,
      description: data.client_description,
      scope_id: data.tenant.scope_id,
    };
    const params = { nocache: (new Date()).getTime() };

    return this.http.post(`${API_TENANTS}`, body, { params })
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  getTenantScopeGroups(filters = {}) {
    const params = { nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(`${API_TENANT_SCOPE_GROUPS}`, { params })
      .then(response => response.data._items)
      .catch(this.errorHandleService.handleHttpError);
  }

  getTenantGroups(id) {
    const params = { nocache: (new Date()).getTime() };

    return this.http.get(`${API_TENANT_GROUPS}/${id}`, { params })
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  createUser({ name, password, description, email, group_id }, tenantId) {
    const params = {};
      params.where = JSON.stringify({
        tenant_id: tenantId,
      });
    return this.http.post(API_USERS, {
      name,
      password,
      description,
      email,
      group_id,
    }, { params })
      .catch(this.errorHandleService.handleHttpError);
  }
}

export default TenantsService;
