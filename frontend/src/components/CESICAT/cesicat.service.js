
import { API_ADDRESS } from 'api/api-config';

const API_CESICAT = `${API_ADDRESS}/attack/statistics`;
const API_CESICAT_ATTACK = `${API_ADDRESS}/attack/registry`;

export class CESICATService {
  constructor($http, AuthService, toastr, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.authService = AuthService;
    this.errorHandlerService = ErrorHandleService;
    this.toast = toastr;
  }

  getStatics(filters = {}) {
    const params = {
      nocache: (new Date()).getTime(),
      short: '[{timestamp, -1}]',
    };

    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_CESICAT, {
      params })
      .then(response => response.data);
  }

  getAttackRegistry(filters = {}) {
    const params = {
      nocache: (new Date()).getTime(),
      sort: '[{detection_timestamp, -1}]',
    };

    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_CESICAT_ATTACK, {
      params })
      .then(response => response.data);
  }
}

export default CESICATService;
