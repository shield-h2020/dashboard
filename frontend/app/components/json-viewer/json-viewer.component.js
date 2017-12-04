import template from './json-viewer.html';
import styles from './json-viewer.scss';

const UI_STRINGS = {
  CLOSE: 'Close',
};

export const JSON_VIEWER_EVENT = {
  EMIT: {
    OPEN: 'emitJsonViewerOpen',
    CLOSE: 'emitJsonViewerClose',
  },
  CAST: {
    OPEN: 'castJsonViewerOpen',
    CLOSE: 'castJsonViewerClose',
  },
};

export const JsonViewerComponent = {
  template,
  bindings: {
    title: '<',
    isOpen: '<',
  },
  controller: class JsonViewerComponent {
    constructor($scope) {
      'ngInject';

      this.isOpen = false;
      this.strings = UI_STRINGS;
      this.styles = styles;
      this.scope = $scope;
    }

    $onInit() {
      this.scope.$on(JSON_VIEWER_EVENT.CAST.OPEN, (event, data) => {
        this.text = JSON.stringify(data, null, 2);
        this.isOpen = true;
      });
    }

    openModal() {
      this.isOpen = true;
    }

    closeModal() {
      this.isOpen = false;
    }
  },
};
