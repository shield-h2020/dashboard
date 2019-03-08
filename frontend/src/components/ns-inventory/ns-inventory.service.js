import {
  API_ADDRESS,
  STORE_ADDRESS,
  ACC_ID,
  SOCKET_ADDRESS
} from "api/api-config";

const API_INVENTORY = `${API_ADDRESS}/inventory/nss`;
const API_CATALOGUE = `${STORE_ADDRESS}/nss/${ACC_ID}`;
const API_NS = `${API_ADDRESS}/nss`;
const API_NSINVENTORY_SOCKET = `${SOCKET_ADDRESS}/vnsfo/notifications/${ACC_ID}`;

export class InventoryService {
  constructor($http, $q, toastr, AuthService, ErrorHandleService) {
    "ngInject";

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
    this.authService = AuthService;
    this.errorHandlerService = ErrorHandleService;
  }

  getInventoryServices({ page = 0, limit = 25 }, filters = {}) {
    const params = { max_results: limit, page, nocache: new Date().getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);
    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant()
      });
    }
    const nsPromises = [];
    const result = {};
    return this.http
      .get(API_INVENTORY, { params })
      .then((response) => {
        for (let i = 0; i < response.data._items.length; i += 1) {
          nsPromises.push(
            this.getCatalogueService(response.data._items[i].ns_id)
              .then((item) => {
                const { _etag, ns_id, ...tagless } = item;
                return {
                  ...response.data._items[i],
                  ...tagless,
                  _id: response.data._items[i]._id,
                };
              })
              .catch(() => this.q.resolve(null)),
          );
          nsPromises.meta = response.data._meta;
        }
        return this.q.all(nsPromises).then((values) =>{ 
          result.items = values;
          result.meta = response.data._meta;
          return result;
        });
      })
      .catch(this.errorHandlerService.handleHttpError);
  }

  removeServiceFromInventory(id, etag) {
    const params = {};
    params.where = JSON.stringify({
      tenant_id: this.authService.getTenant()
    });

    return this.http
      .delete(`${API_INVENTORY}/${id}`, {
        params,
        headers: { "if-match": etag }
      })
      .catch(this.errorHandlerService.handleHttpError);
  }

  instantiateService(id, etag) {
    const params = { nocache: new Date().getTime() };

    if (!this.authService.isUserPlatformAdmin()) {
      params.where = JSON.stringify({
        tenant_id: this.authService.getTenant()
      });
    }

    return this.http
      .patch(
        `${API_NS}/instantiate/${id}`,
        {},
        { params, headers: { "if-match": etag } }
      )
      .catch(this.errorHandlerService.handleHttpError);
  }

  terminateService(id, etag) {
    const params = {};
    params.where = JSON.stringify({
      tenant_id: this.authService.getTenant()
    });

    return this.http
      .patch(
        `${API_NS}/terminate/${id}`,
        {},
        { params, headers: { "if-match": etag } }
      )
      .catch(this.errorHandlerService.handleHttpError);
  }

  async getCatalogueService(id) {
    const params = { nocache: new Date().getTime() };

    return this.http
      .get(API_CATALOGUE.replace(ACC_ID, id), {
        params,
        headers: { Authorization: undefined }
      })
      .then(response => response.data);
  }

  connectNSInventorySocket(tenantId) {
    return new WebSocket(API_NSINVENTORY_SOCKET.replace(ACC_ID, tenantId));
  }
}

export default InventoryService;
