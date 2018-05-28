import template from './editmodalbox.html';
import { APP_STRINGS } from '../../strings/ui-strings';
import { EDIT_MODAL_EVENT } from '../../strings/event-strings';

export const EditModalBoxComponent = {
  template,
  bindings: {
    value: '<',
    updateAction: '&',
  },
  controller: class EditModalBoxComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.isHidden = true;
      this.strings = {
        common: APP_STRINGS.common,
      };
    }

    $onInit() {
      this.scope.$on(EDIT_MODAL_EVENT.CAST.OPEN, (event, data) => {
        this.id = data.id;
        this.value = data.value;
        this.isHidden = false;
      });

      this.scope.$on(EDIT_MODAL_EVENT.CAST.CLOSE, () => {
        this.isHidden = true;
      });
    }

    action() {
      this.updateAction({
        $event: {
          id: this.id,
          value: this.value,
        },
      });
    }

    cancelAction() {
      this.isHidden = true;
    }
  },
};

export default EditModalBoxComponent;
