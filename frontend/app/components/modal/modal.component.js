import template from './modal.html';
import styles from './modal.scss';

const UI_STRINGS = {
  buttons: {
    cancel: 'Close',
  },
};

export const ModalComponent = {

  template,
  transclude: true,
  bindings: {
    modalOpen: '<',
    modalHandler: '&',
    title: '@?',
    modalData: '<?',
  },
  controller: class ModalComponent {
    constructor($scope, $element, $transclude) {
      'ngInject';

      this.scope = $scope;
      this.transclude = $transclude;
      this.element = $element;
      this.styles = styles;
      this.strings = UI_STRINGS;
    }

    $onInit() {
      this.transclude(this.scope, (clone) => { this.element.find('article').append(clone); });
    }

    toggleModal() {
      this.modalHandler({ $event: { value: !this.modalOpen } });
    }

    prettyJSON(obj) {
      return JSON.stringify(obj, null, 2);
    }
  },

};

export default ModalComponent;
