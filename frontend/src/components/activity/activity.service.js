import { API_ADDRESS } from 'api/api-config';

const API_ACTIVITY = `${API_ADDRESS}/activity`;

export class ActivityService {
  constructor($http, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.errorHandlerService = ErrorHandleService;
  }

  getActivitys({ page = 0, limit = 10 }, filters = {}) {
    const params = {
      max_results: limit,
      page,
      nocache: (new Date()).getTime(),
      short: '[{timestamp, -1}]',
    };

    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_ACTIVITY, { params }, {
      headers: { Authorization: undefined } })
      .then(response => response.data);
  }
}

export default ActivityService;
