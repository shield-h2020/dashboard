import template from './file-uploader.html';
import styles from './file-uploader.scss';

const VIEW_STRINGS = {
  loading: 'Onboarding, please wait...',
  withFiles: 'Select Other File',
  noFiles: 'Select File',
}

export const FileUploaderComponent = {
  template,
  bindings: {
    onChange: '<',
  },
  controller: class FileUploaderComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.styles = styles;
      this.viewStrings = VIEW_STRINGS;
      this.scope.files = [];
    }

    $onInit() {
      this.scope.$watchCollection('files', (value) => {
        this.onChange({ $event: { value } });
      });
    }

  },
};

export default FileUploaderComponent;
