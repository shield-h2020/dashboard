import { API_ADDRESS, STORE_ADDRESS, ACC_ID } from 'api/api-config';

const API_INVENTORY = `${API_ADDRESS}/inventory/nss`;
const API_CATALOGUE = `${STORE_ADDRESS}/nss/${ACC_ID}`;
// /id?where={tenant_id: ''}
export class InventoryService {
  constructor($http, $q, toastr, AuthService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
  }

  getInventoryServices({ page = 0, limit = 25 }, filters = {}) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant(),
      });
    }

    const nsPromises = [];
    return this.http.get(API_INVENTORY, { params })
      .then((response) => {
        for (let i = 0; i < response.data._items.length; i += 1) {
          nsPromises.push(this.getCatalogueService(response.data._items[i].ns_id)
            .then(item => item));
        }
        return this.q.all(nsPromises)
          .then(values => values);
      });
  }

  async getCatalogueService(id) {
    const params = {};
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant(),
      });
    }
    return this.http.get(API_CATALOGUE.replace(ACC_ID, id), { params, headers: { Authorization: undefined } })
      .then(response => response.data);
  }
}

export default InventoryService;
