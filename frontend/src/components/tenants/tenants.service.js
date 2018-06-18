import { API_ADDRESS, ACC_ID } from 'api/api-config';

const API_TENANTS = `${API_ADDRESS}/catalogue/tenants`;
const API_TENANT = `${API_TENANTS}/${ACC_ID}`;
const API_TENANT_IPS = `${API_ADDRESS}/tenant_ips`;
const API_TENANT_SCOPES = `${API_ADDRESS}/definitions/tenant_scopes`;

const STRINGS = {
  TENANT_ERROR: 'An error occurred',
  TENANTS_ERROR: 'An error occurred',
};

const TOAST_STRINGS = {
  UPDATE_SUCCESS_TENANT: {
    TITLE: 'Secaas client updated',
    MESSAGE: 'Client updated successfully',
  },
  CREATE_SUCCESS_TENANT: {
    TITLE: 'Secaas client created',
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
  }
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

  updateTenantAndIps({ tenant_id, tenant_name, _etag, description, scope_id, ip, prevIps }) {
    return this.http.put(API_TENANT.replace(ACC_ID, tenant_id),
      { tenant_name, description, scope_id }, { headers: { 'if-match': _etag } })
      .then(() => {
        this.toast.info(TOAST_STRINGS.UPDATE_SUCCESS_TENANT.MESSAGE,
          TOAST_STRINGS.UPDATE_SUCCESS_TENANT.TITLE);
        if (ip.length) {
          if (prevIps) {
            return this.updateTenantIps(tenant_id, ip);
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

  updateTenantIps(tenantId, ip) {
    return this.http.patch(`${API_TENANT_IPS}/${tenantId}`, {
      ip,
    })
    .catch(() => {
      this.toast.error(TOAST_STRINGS.UPDATE_ERROR_IP.MESSAGE,
        TOAST_STRINGS.UPDATE_ERROR_IP.TITLE);
    });
  }

  getTenantIps(tenantId) {
    return this.http.get(`${API_TENANT_IPS}/${tenantId}`)
      .then(response => response.data.ip)
      .catch((err) => {
        if (err.data._error.code !== 404) {
          this.toast.error(TOAST_STRINGS.GET_ERROR_IP.MESSAGE,
            TOAST_STRINGS.GET_ERROR_IP.TITLE);
        }

        return this.q.reject(err.data._error.code);
      });
  }

  getScopeId(scopeCode) {
    return this.http.get(`${API_TENANT_SCOPES}/${scopeCode}`)
      .then(response => response.data._id);
  }
}

export default TenantsService;
