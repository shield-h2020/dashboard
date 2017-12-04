import template from './internal-error.html';
import styles from './internal-error.scss';

export const INTERNAL_ERROR_MODAL_EVENT = {
  EMIT: {
    OPEN: 'emitErrorModalOpen',
    CLOSE: 'emitErrorModalClose',
  },
  CAST: {
    OPEN: 'castErrorModalOpen',
    CLOSE: 'castErrorModalClose',
  },
};

const UI_STRINGS = {
  TITLE_ERROR: 'Internal SHIELD component error',
  TITLE_UNAVAILABLE: 'Internal SHIELD component unavailable',
  OK: 'Ok',
};

export const ErrorModalBoxComponent = {
  template,
  controller: class EditModalBoxComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.isHidden = true;
      this.strings = UI_STRINGS;
      this.styles = styles;
    }

    $onInit() {
      this.scope.$on(INTERNAL_ERROR_MODAL_EVENT.CAST.OPEN, (event, data) => {
        this.error = data;
        this.isHidden = false;
      });

      this.scope.$on(INTERNAL_ERROR_MODAL_EVENT.CAST.CLOSE, () => {
        this.isHidden = true;
      });
    }

    cancelAction() {
      this.isHidden = true;
    }
  },
};
