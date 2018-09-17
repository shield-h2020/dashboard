import { API_ADDRESS, SOCKET_ADDRESS, ACC_ID } from 'api/api-config';

const API_VNSF_NOTIFICATIONS = `${API_ADDRESS}/notifications`;
const API_VNSF_NOTIFICATIONS_SOCKET = `${SOCKET_ADDRESS}/vnsf/notifications/${ACC_ID}`;
const API_TM_NOTIFICATIONS_SOCKET = `${SOCKET_ADDRESS}/tm/notifications/${ACC_ID}`;

export class VnsfNotificationService {
  constructor($http, $q, toastr, AuthService, TenantsService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
    this.tenantsService = TenantsService;
  }

  getNotifications({ page = 1, limit = 25 }, filters = {}) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant(),
      });
    }

    const vnsfPromises = [];
    return this.http.get(API_VNSF_NOTIFICATIONS, { params })
      .then((response) => {
        const notifs = response.data._items;
        for (let i = 0, len = notifs.length; i < len; i += 1) {
          vnsfPromises.push(this.tenantsService.getTenant(notifs[i].tenant_id)
          .catch(() =>
            ({
              ...notifs[i],
              tenant_name: 'not found',
            }))
          .then(tenant => ({
            ...notifs[i],
            tenant_name: tenant.tenant_name,
          })));
        }

        return this.q.all(vnsfPromises)
          .then(values => values);
      });
  }

  connectNotificationsSocket(tenantId) {
    this.datastream = new WebSocket(API_VNSF_NOTIFICATIONS_SOCKET.replace(ACC_ID, tenantId));
    return this.datastream;
  }

  connectTMNotificationsSocket(tenantId) {
    this.datastreamTM = new WebSocket(API_TM_NOTIFICATIONS_SOCKET.replace(ACC_ID, tenantId));
    return this.datastreamTM;
  }
}

export default VnsfNotificationService;
