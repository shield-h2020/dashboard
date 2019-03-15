import { API_ADDRESS, STORE_ADDRESS, ACC_ID } from 'api/api-config';

const API_CATALOGUE = `${STORE_ADDRESS}/nss`;
const API_INVENTORY = `${API_ADDRESS}/inventory/nss`;
const API_INVENTORY_ONE = `${API_INVENTORY}/${ACC_ID}`;
const API_BILLING = `${API_ADDRESS}/billing/ns`;

export class CatalogueService {
  constructor($http, AuthService, toastr, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.authService = AuthService;
    this.errorHandlerService = ErrorHandleService;
    this.toast = toastr;
  }

  getCatalogueServices({ page = 0, limit = 10 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_CATALOGUE, {
      params,
      headers: { Authorization: undefined } })
      .then(response => response.data._items);
  }

  addServiceToInventory(id) {
    const params = {};
    params.where = JSON.stringify({
      tenant_id: this.authService.getTenant(),
    });

    return this.http.post(API_INVENTORY, {
      ns_id: id,
      status: 'available',
    }, { params })
      .then(() => {
        this.toast.success('Service added to client\'s inventory');
      })
      .catch(this.errorHandlerService.handleHttpError);
  }

  getBillingFeeService(nsId) {
    const params = { nocache: (new Date()).getTime() };
    return this.http.get(`${API_BILLING}/${nsId}`, { params }, {
      headers: { Authorization: undefined } })
      .then(response => response.data);
  }

  simulateBillingFee(simulation) {
    const data = JSON.stringify({ ns_id: simulation.nsId, fee: simulation.fee });
    return this.http.post(`${API_BILLING}/simulate`, data)
      .then(response => response.data);
  }

  applyFeeBilling({ fee, nsId, etag }) {
    const currentSession = this.authService.getSessionInfo();
    const data = JSON.stringify({ fee: fee });
    return this.http.patch(`${API_BILLING}/${nsId}`, data,
      { headers: {
        Authorization: `Basic ${this.window.btoa(`${currentSession.token}:''`)}`,
        'Content-Type': 'application/json',
        'If-Match': etag,
      },
      })
      .then(response => response.data);
  }

  createBillingService(id) {
    return this.http.post(API_BILLING, { ns_id: id })
      .then(response => response.data._items);
  }
}

export default CatalogueService;
