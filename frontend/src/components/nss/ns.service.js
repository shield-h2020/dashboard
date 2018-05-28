// import format from 'date-fns/format';
import { NS_API, ACCESSORS } from '../../strings/api-strings';

export class NSService {
  constructor($http, toastr, $q, FileUploadService) {
    'ngInject';

    this.http = $http;
    this.q = $q;
    this.toast = toastr;
    this.uploadService = FileUploadService;
  }

  getAllNSs({ page = 1, limit = 25 }, filters) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length !== 0) params.where = JSON.stringify(filters);

    return this.http.get(NS_API.ALL, { params })
        .then((response) => {
          // const items = response.data._items.map((item) => {
          //   const it = { ...item };
          //   it.detection = format(item.detection, 'DD/MM/YYYY - HH:mm');

          //   return it;
          // });
          const { _items: items, _meta: meta } = response.data;

          return {
            items: items.map(item => ({
              ...item,
            })),
            meta,
          };
        })
        .catch((error) => {
          this.toast.error(`An error occurred - ${error}`);
        });
  }

  getNS(id) {
    return this.http.get(NS_API.ONE.replace(ACCESSORS.id, id))
        .then(response => response.data)
        .catch(() => {
          this.toast.error('An error occurred');
        });
  }

  uploadNS(file) {
    return this.uploadService.uploadFile(NS_API.ONE_UPLOAD, 'POST', file)
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

export default NSService;
