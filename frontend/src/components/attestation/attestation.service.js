import { API_ADDRESS } from 'api/api-config';

const API_VNSF_NOTIFICATIONS = `${API_ADDRESS}/tm/vnsf/notifications`;
const API_TM_NOTIFICATIONS = `${API_ADDRESS}/tm/notifications`;

export class AttestationService {
  constructor($http, $q, toastr, AuthService, TenantsService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
    this.tenantsService = TenantsService;
  }

  getNotifications({ page = 1, limit = 25 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime(), sort: '[("time",-1)]'};
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    let api_address;
    if(this.authService.isUserTenantAdmin()){
      api_address = API_VNSF_NOTIFICATIONS;
    }
    else{
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

}

export default AttestationService;
