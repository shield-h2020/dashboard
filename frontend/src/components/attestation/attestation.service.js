import { API_ADDRESS } from 'api/api-config';

const API_VNSF_NOTIFICATIONS = `${API_ADDRESS}/tm/vnsf/notifications/distinct`;
const API_TM_NOTIFICATIONS = `${API_ADDRESS}/tm/notifications/distinct`;
const API_ATTEST = `${API_ADDRESS}/tm/attest`;
const API_ATTEST_ALL = `${API_ADDRESS}/tm/attest/all`;

export class AttestationService {
  constructor($http, $q, AuthService, TenantsService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.authService = AuthService;
    this.tenantsService = TenantsService;
  }

  getNotifications({ page = 1, limit = 25 }, filters = {}) {
    const params = { page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    let api_address;
    if (this.authService.isUserTenantAdmin()) {
      api_address = API_VNSF_NOTIFICATIONS;
    } else {
      api_address = API_TM_NOTIFICATIONS;
    }  
    return this.http.get(api_address, { params })
      .then((response) => {
        const notifs = response.data._items;

        return {
          notifs,
          meta: response.data._meta,
        };
      })
  }
  attestInfrastructure(filters = {}) {
    const api_address = API_ATTEST;
    return this.http.post(api_address, filters)
      .then((response) => {
       console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  attestAllInfrastructure() {
    let api_address = API_ATTEST_ALL;
    return this.http.post(api_address,{})
      .then((response) => {
        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

}

export default AttestationService;
