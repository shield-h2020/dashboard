import template from './uploadbox.html';
import { UI_STRINGS, ACCESSOR } from './uploadbox.strings';
import { UPLOAD_MODAL_EVENT } from '../../strings/event-strings';
import styles from './uploadbox.scss';

export const UploadBoxComponent = {
  template,
  bindings: {
    service: '<',
    onSubmit: '&',
  },
  controller: class UploadBoxComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.strings = Object.assign({}, UI_STRINGS);
      this.styles = styles;
      this.isHidden = true;
      this.fileType = '';
      this.enableButton = false;
      this.fileSize = 0;
      this.scope.files = [];
      this.isLoading = false;
    }

    $onInit() {
      this.scope.$on(UPLOAD_MODAL_EVENT.CAST.OPEN, (event, data) => {
        this.fileType = data.fileType;
        this.fileSize = data.fileSize;
        this.uploadTitle = data.uploadTitle;
        this.isHidden = false;
        this.strings.info = this.strings.info.replace(ACCESSOR, this.fileType);
        this.filename = this.strings.info;
      });

      this.scope.$on(UPLOAD_MODAL_EVENT.CAST.CLOSE, () => {
        this.isHidden = true;
      });

      this.scope.$on(UPLOAD_MODAL_EVENT.CAST.LOADING, () => {
        this.isLoading = false;
      });

      this.scope.$watchCollection('files', (value) => {
        this.enableButton = (value.length > 0);
        if (value.length > 0) {
          this.filename = value[0].name;
        }
      });
    }

    submit() {
      this.isLoading = true;
      this.onSubmit({
        $event: {
          file: this.scope.files[0],
        },
      });
    }

    cancelAction() {
      this.isHidden = true;
      this.strings.info = UI_STRINGS.info;
    }
  },
};

export default UploadBoxComponent;
