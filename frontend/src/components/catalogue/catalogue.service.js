import { API_ADDRESS, STORE_ADDRESS, ACC_ID } from 'api/api-config';

const API_CATALOGUE = `${STORE_ADDRESS}/nss`;
const API_INVENTORY = `${API_ADDRESS}/inventory/nss`;
const API_INVENTORY_ONE = `${API_INVENTORY}/${ACC_ID}`;

export class CatalogueService {
  constructor($http, AuthService, toastr, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.authService = AuthService;
    this.errorHandlerService = ErrorHandleService;
    this.toast = toastr;
  }

  getCatalogueServices({ page = 0, limit = 10 }, filters = {}) {
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_CATALOGUE, {
      params,
      headers: { Authorization: undefined } })
      .then(response => response.data._items);
  }

  addServiceToInventory(id) {
    const params = {};
    params.where = JSON.stringify({
      tenant_id: this.authService.getTenant(),
    });

    return this.http.post(API_INVENTORY, {
      ns_id: id,
      status: 'available',
    }, { params })
      .then(() => {
        this.toast.success('Service added to tenant\'s inventory');
      })
      .catch(this.errorHandlerService.handleHttpError);
  }

  removeServiceFromInventory(id, etag) {
    const params = {};
    params.where = JSON.stringify({
      tenant_id: this.authService.getTenant(),
    });

    return this.http.delete(API_INVENTORY_ONE.replace(ACC_ID, id),
      { params, headers: { 'if-match': etag } })
      .then(() => {
        this.toast.success('Service was removed from tenant\'s inventory');
      })
      .catch(this.errorHandlerService.handleHttpError);
  }
}

export default CatalogueService;
