import { API_ADDRESS } from 'api/api-config';

export class DashboardService {
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
}
export default DashboardService;