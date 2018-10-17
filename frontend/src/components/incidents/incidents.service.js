import format from 'date-fns/format';
import { API_ADDRESS, SOCKET_ADDRESS, ACC_ID } from 'api/api-config';

const API_INCIDENTS = `${API_ADDRESS}/policies`;
const API_INCIDENT_SOCKET = `${SOCKET_ADDRESS}/policy/${ACC_ID}`;

/* global WebSocket */
export class IncidentsService {
  constructor($http, toastr, AuthService, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
    this.errorHandlerService = ErrorHandleService;
  }

  connectIncidentSocket(tenantId) {
    return new WebSocket(API_INCIDENT_SOCKET.replace(ACC_ID, tenantId));
  }

  getIncidents({ page = 1, limit = 25 }, filters) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime(), sort: '[("detection",-1)]' };

    if (Object.keys(filters).length !== 0) {
      params.where = JSON.stringify(filters);
    }
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant(),
      });
    }

    return this.http.get(API_INCIDENTS, { params })
      .then((response) => {
        const items = response.data._items.map(item =>
          ({
            ...item,
            detection: format(item.detection, 'DD/MM/YYYY - HH:mm'),
          }));

        return {
          items,
          meta: response.data._meta,
        };
      })
      .catch(this.errorHandlerService.handleHttpError);
  }

  getIncident(id) {
    return this.http.get(`${API_INCIDENTS}/${id}`)
      .then(response => response.data)
      .catch(this.errorHandlerService.handleHttpError);
  }

  recommendAction(id, etag) {
    return this.http.patch(`${API_INCIDENTS}/${id}`,
      { status: 'Applied' }, { headers: { 'if-match': etag } })
      .catch(this.errorHandlerService.handleHttpError);
  }
}

export default IncidentsService;
