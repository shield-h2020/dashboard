// import format from 'date-fns/format';
import { STORE_ADDRESS } from 'api/api-config';
import { VNSF_API, ACCESSORS } from '../../strings/api-strings';

const API_VNSF = `${STORE_ADDRESS}/vnsfs`;

export class VNSFService {
  constructor($http, toastr, $q, FileUploadService, ErrorHandleService) {
    'ngInject';

    this.http = $http;
    this.q = $q;
    this.errorHandleService = ErrorHandleService;
    this.toast = toastr;
    this.uploadService = FileUploadService;
  }

  getAllVNSFs({ page = 1, limit = 25 }, filters) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length !== 0) params.where = JSON.stringify(filters);

    return this.http.get(API_VNSF, {
      params,
      headers: {
        Authorization: undefined,
      } })
        .then((response) => {
          const { _items, _meta } = response.data;
          return {
            items: _items.map(item => ({
              ...item,
              vendor: item.manifest['manifest:vnsf'].properties.vendor,
              security: item.manifest[Object.keys(item.manifest)[0]].security_info,
            })),
            meta: _meta,
          };
        })
        .catch(this.errorHandleService.handleHttpError);
  }

  getVNSF(id) {
    return this.http.get(VNSF_API.ONE.replace(ACCESSORS.id, id))
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  uploadVNSF(file) {
    return this.uploadService.uploadFile(VNSF_API.ONE_UPLOAD, 'POST', file)
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

export default VNSFService;
