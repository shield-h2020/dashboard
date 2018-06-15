import template from './modalbox.html';
import { UI_STRINGS, ACCESSOR } from './modalbox.strings';
import { APP_STRINGS } from '../../strings/ui-strings';
import { MODAL_EVENT } from '../../strings/event-strings';

export const ModalBoxComponent = {

  template,
  bindings: {
    targetType: '@',
    onAction: '&',
  },
  controller: class ModalBoxComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.isHidden = true;
      this.strings = {
        common: APP_STRINGS.common,
      };
    }

    $onInit() {
      this.scope.$on(MODAL_EVENT.CAST.OPEN, (event, data) => {
        this.actionType = data.actionType;
        this.strings.box = Object.assign({}, UI_STRINGS[this.actionType]);
        this.strings.box.message = this.strings.box.message &&
          this.strings.box.message.replace(ACCESSOR, this.targetType);
        this.isHidden = false;
        this.target = data.target;
      });

      this.scope.$on(MODAL_EVENT.CAST.CLOSE, () => {
        this.isHidden = true;
      });
    }

    action() {
      this.onAction({
        $event: {
          target: this.target,
        },
      });
    }

    cancelAction() {
      this.isHidden = true;
    }
  },
};

export default ModalBoxComponent;
