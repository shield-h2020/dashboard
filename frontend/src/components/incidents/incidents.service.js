import format from 'date-fns/format';
import { INCIDENTS_API, INCIDENTS_SOCKET_API, ACCESSORS } from '../../strings/api-strings';

/* global WebSocket */
export class IncidentsService {
  constructor($http, toastr) {
    'ngInject';

    this.http = $http;
    this.toast = toastr;
    this.datastream = null;
  }

  connectIncidentSocket() {
    this.datastream = new WebSocket(INCIDENTS_SOCKET_API.CONNECT);

    return this.datastream;
  }

  getAllIncidents({ page = 1, limit = 25 }, filters) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length !== 0) params.where = JSON.stringify(filters);

    return this.http.get(INCIDENTS_API.ALL, { params })
      .then((response) => {
        const items = response.data._items.map((item) => {
          const it = { ...item };
          it.detection = format(item.detection, 'DD/MM/YYYY - HH:mm');

          return it;
        });

        return {
          items,
          meta: response.data._meta,
        };
      })
      .catch(() => {
        this.toast.error('An error occurred');
      });
  }

  getIncident(id) {
    return this.http.get(INCIDENTS_API.ONE.replace(ACCESSORS.id, id))
      .then(response => response.data)
      .catch(() => {
        this.toast.error('An error occurred');
      });
  }

  recommendAction(id, etag) {
    return this.http.patch(INCIDENTS_API.ONE.replace(ACCESSORS.id, id),
      { status: 'Applied' }, { headers: { 'if-match': etag } })
      .catch((response) => {
        if (response && response.data) {
          this.toast.error(response.data._error.message, 'An error occurred');
        } else {
          this.toast.error('An error occurred');
        }

        return this.q.reject(response);
      });
  }
  }

export default IncidentsService;
