import { identity } from 'angular';

/* global FormData */
export class FileUploadService {
  constructor($http, $q, toastr) {
    'ngInject';

    this.http = $http;
    this.q = $q;
    this.toast = toastr;
  }

  uploadFile(url, method, file) {
    const formData = new FormData();
    formData.append('package', file);
    return this.http({
      url,
      method,
      data: formData,
      transformRequest: identity,
      headers: { 'Content-Type': undefined },
    });
  }
}

export default FileUploadService;
