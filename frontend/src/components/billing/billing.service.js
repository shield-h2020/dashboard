import { API_ADDRESS } from 'api/api-config';

const API_BILLING_NS = `${API_ADDRESS}/billing/ns/summary`;
const API_BILLING_VNSF = `${API_ADDRESS}/billing/vnsf/summary`;
const API_BILLING = `${API_ADDRESS}/billing/summary`;

export class BillingService {
  constructor($http, AuthService, toastr, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.authService = AuthService;
    this.errorHandlerService = ErrorHandleService;
    this.toast = toastr;
  }

  getBillingSummaryNS({ page = 0, limit = 10 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    return this.http.get(API_BILLING_NS, { params })
      .then(response => response.data._items);
  }

  getBillingSummaryVNSF({ page = 0, limit = 10 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    return this.http.get(`${API_BILLING_VNSF}`, { params })
    .then(response => response.data._items);
  }

  getBillingSummary({ page = 0, limit = 10 }) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    return this.http.get(`${API_BILLING}`, { params })
    .then(response => response.data._items);
  }
}

export default BillingService;
