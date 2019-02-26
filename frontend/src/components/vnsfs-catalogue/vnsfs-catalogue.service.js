// import format from 'date-fns/format';
import { STORE_ADDRESS, API_ADDRESS } from 'api/api-config';
import { VNSF_API, ACCESSORS } from '../../strings/api-strings';

const API_VNSF = `${STORE_ADDRESS}/vnsfs`;
const API_NSS = `${STORE_ADDRESS}/nss`;
const API_BILLING = `${API_ADDRESS}/billing/vnsf`;

export class VNSFService {
  constructor($http, toastr, $window, AuthService, $q, FileUploadService, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.q = $q;
    this.authService = AuthService;
    this.window = $window;
    this.errorHandleService = ErrorHandleService;
    this.toast = toastr;
    this.uploadService = FileUploadService;
  }

  getAllVNSFs({ page = 1, limit = 25 }, filters) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length !== 0) params.where = JSON.stringify(filters);

    return this.http.get(API_VNSF, {
      params,
      headers: {
        Authorization: undefined,
      },
    })
      .then((response) => {
        const { _items, _meta } = response.data;
        return {
          items: _items.map(item => ({
            ...item,
            vendor: item.manifest['manifest:vnsf'].properties.vendor,
            security: item.manifest[Object.keys(item.manifest)[0]].security_info,
          })),
          meta: _meta,
        };
      })
      .catch(this.errorHandleService.handleHttpError);
  }

  getVNSF(id) {
    const params = { nocache: (new Date()).getTime() };

    return this.http.get(VNSF_API.ONE.replace(ACCESSORS.id, id), {
      params,
    })
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  uploadVNSF(file) {
    return this.uploadService.uploadFile(API_VNSF, 'POST', file)
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  uploadNS(file) {
    return this.uploadService.uploadFile(API_NSS, 'POST', file)
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  deleteVnsf({ _id, _etag }) {
    return this.http.delete(`${API_VNSF}/${_id}`, { headers: { Authorization: undefined, 'If-Match': _etag } })
      .catch(this.errorHandleService.handleHttpError);
  }

  deleteNs({ _id, _etag }) {
    return this.http.delete(`${API_NSS}/${_id}`, { headers: { Authorization: undefined, 'If-Match': _etag } })
      .catch(this.errorHandleService.handleHttpError);
  }

  createBillingvNSF(tenant, id) {
    const currentSession = this.authService.getSessionInfo();
    const data = JSON.stringify({
      vnsf_id: id,
    });
    const params = {};
    params.where = JSON.stringify({
      tenant_id: tenant,
    });
    return this.http.post(API_BILLING, data, {
      params,
      headers: {
        Authorization: `Basic ${this.window.btoa(`${currentSession.token}:''`)}`,
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.data._items);
  }

  getBillingApplyFee(id) {
    const params = { nocache: (new Date()).getTime() };
    return this.http.get(`${API_BILLING}/${id}`, { params })
      .then(response => response.data);
  }

  setBillingApplyFee({ fee, vnsf_id, _etag }) {
    const data = JSON.stringify({ fee: fee });
    return this.http.patch(`${API_BILLING}/${vnsf_id}`,
      data,
      { headers: { 'If-Match': _etag } })
      .then(response => response.data);
  }
}

export default VNSFService;
