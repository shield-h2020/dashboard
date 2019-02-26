import { API_ADDRESS } from 'api/api-config';

const API_BILLING_NS = `${API_ADDRESS}/billing/ns/usage`;
const API_BILLING_VNSF = `${API_ADDRESS}/billing/vnsf/usage`;

export class BillingDetailService {
  constructor($http, AuthService, toastr, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.authService = AuthService;
    this.errorHandlerService = ErrorHandleService;
    this.toast = toastr;
  }

  getBillingUsageNS({ page = 0, limit = 10 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_BILLING_NS, {
      params })
      .then(response => response.data);
  }

  getBillingUsageVNSF({ page = 0, limit = 10 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_BILLING_VNSF, {
      params })
      .then(response => response.data);
  }

}

export default BillingDetailService;
