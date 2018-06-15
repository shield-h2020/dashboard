import { API_ADDRESS, SOCKET_ADDRESS, ACC_ID } from 'api/api-config';

const API_VNSF_NOTIFICATIONS = `${API_ADDRESS}/vnsf_notifications`;
const API_VNSF_NOTIFICATIONS_SOCKET = `${SOCKET_ADDRESS}/vnsf/notifications/${ACC_ID}`;

export class VnsfNotificationService {
  constructor($http, $q, toastr, AuthService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
  }

  getNotifications({ page = 1, limit = 25 }, filters = {}) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant(),
      });
    }

    return this.http.get(API_VNSF_NOTIFICATIONS, { params })
      .then(response => response.data._items);
  }

  connectNotificationsSocket(tenantId) {
    this.datastream = new WebSocket(API_VNSF_NOTIFICATIONS_SOCKET.replace(ACC_ID, tenantId));
    return this.datastream;
  }
}

export default VnsfNotificationService;
