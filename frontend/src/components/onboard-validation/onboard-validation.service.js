import { STORE_ADDRESS } from 'api/api-config';
import { parseXML, syncParseXML } from './utils/parser';

const API_VALIDATIONS = `${STORE_ADDRESS}/validation`;

export class OnboardValidationService {
  constructor($http, $q, toastr, ErrorHandleService) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
    this.errorHandlerService = ErrorHandleService;
  }

  getValidations({ page = 0, limit = 10 }, filters = {}) {
    const params = { max_results: limit, page };
    if (Object.keys(filters).length) params.where = JSON.stringify(filters);

    return this.http.get(API_VALIDATIONS, {
      params,
      headers: { Authorization: undefined },
    })
      .then(response => ({
        items: response.data._items,
        meta: response.data._meta,
      }));
  }

  getValidationById(id) {
    return this.http.get(`${API_VALIDATIONS}/${id}`, { headers: { Authorization: undefined } })
      .then((response) => {
        const { topology: { graph }, result } = response.data;

        return {
          graph: syncParseXML(graph),
          errors: result.error_count,
          warnings: result.warning_count,
          issues: result.issues.length ? result.issues : [],
        };
      })
      .catch(this.errorHandlerService.handleHttpError);
  }
}

export default OnboardValidationService;
