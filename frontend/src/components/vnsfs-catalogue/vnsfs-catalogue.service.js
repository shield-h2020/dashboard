// import format from 'date-fns/format';
import { STORE_ADDRESS } from 'api/api-config';
import { VNSF_API, ACCESSORS } from '../../strings/api-strings';

const API_VNSF = `${STORE_ADDRESS}/vnsfs`;
const API_NSS = `${STORE_ADDRESS}/nss`;

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
    const params = { max_results: limit, page, nocache: (new Date()).getTime() };
    if (Object.keys(filters).length !== 0) params.where = JSON.stringify(filters);

    return this.http.get(API_VNSF, {
      params,
      headers: {
        Authorization: undefined,
      }
    })
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
    const params = { nocache: (new Date()).getTime() };

    return this.http.get(VNSF_API.ONE.replace(ACCESSORS.id, id), {
      params
    })
      .then(response => response.data)
      .catch(this.errorHandleService.handleHttpError);
  }

  uploadVNSF(file) {
    return this.uploadService.uploadFile(API_VNSF, 'POST', file)
      .catch(this.errorHandleService.handleHttpError);
  }

  uploadNS(file) {
    return this.uploadService.uploadFile(API_NSS, 'POST', file)
      .catch(this.errorHandleService.handleHttpError);
  }

  deleteVnsf({ _id, _etag }) {
    return this.http.delete(`${API_VNSF}/${_id}`, { headers: { Authorization: undefined, 'If-Match': _etag } })
      .catch(this.errorHandleService.handleHttpError);
  }

  deleteNs({ _id, _etag }) {
    return this.http.delete(`${API_NSS}/${_id}`, { headers: { Authorization: undefined, 'If-Match': _etag } })
      .catch(this.errorHandleService.handleHttpError);
  }
}

export default VNSFService;
