
const ERROR_TITLE = 'An error occurred';

export class ErrorHandleService {
  constructor(toastr, $q) {
    'ngInject';

    this.q = $q;
    this.toast = toastr;

    this.handleHttpError = this.handleHttpError.bind(this);
  }

  handleHttpError(error) {
    let err;
    if (error.data) {
      err = error.data._error.message;
    } else {
      err = error;
    }

    this.toast.error(err, ERROR_TITLE);
    return this.q.reject(err);
  }
}

export default ErrorHandleService;
