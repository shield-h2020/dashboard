const ERROR_TITLE = 'An error occurred';
const SUCCESS_TITLE = 'Successful operation';

export class ErrorHandleService {
  constructor(toastr, $q) {
    'ngInject';

    this.q = $q;
    this.toast = toastr;

    this.handleHttpError = this.handleHttpError.bind(this);
    this.handleHttpSuccess = this.handleHttpSuccess.bind(this);
  }

  handleHttpError(error) {
    let err;
    if (error.data) {
      err = error.data._error.message;
    } else {
      err = error;
    }

    if (error.data && error.data._error.code === 404) {
      err = 'Data not found';
    }

    this.toast.error(err, ERROR_TITLE);
    return this.q.reject(err);
  }

  handleHttpSuccess(response) {
    this.toast.success('', SUCCESS_TITLE);
    return this.q.resolve(response);
  }
}

export default ErrorHandleService;
