import { API_ADDRESS } from 'api/api-config';
import { parseXML } from './utils/parser';

const API_VALIDATIONS = `${API_ADDRESS}/validations`;

export class OnboardValidationService {
  constructor($http, $q, toastr) {
    'ngInject';

    this.q = $q;
    this.http = $http;
    this.toast = toastr;
  }

  getValidations() {
    return this.http.get(API_VALIDATIONS)
      .then(response => response.data._items);
  }

  getValidation(validation) {
    const { topology: { graph } } = validation;
    let parsed = graph;
    if (graph) {
      parsed = graph.substr(1).substr(0, graph.length - 2);
    }

    return parseXML(parsed);
  }

  getResults(validation) {
    const { result } = validation;
    return new Promise((resolve, reject) => {
      resolve({
        errors: result.error_count,
        warnings: result.warning_count,
        issues: JSON.parse(result.issues),
      });
    });
  }
}

export default OnboardValidationService;
