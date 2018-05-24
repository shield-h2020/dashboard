import template from './menu-card.html';
// import { HIGHLIGHT_EVENT } from '../../../services/event-strings';

export const MenuCardComponent = {

  template,
  bindings: {
    item: '<',
  },
  controller: class MenuCardComponent {
    constructor($scope) {
      'ngInject';

      this.scope = $scope;
      this.collapsed = true;
    }

    $onInit() {
      const { event_code, event_id, header, source_id } = this.item
      this.parsedItem = {
        eventCode: event_code,
        eventId: event_id,
        header,
        sourceId: source_id,
      };
    }

/*     highlightElement(id, hlight) {
      this.scope.$emit(HIGHLIGHT_EVENT.EMIT, { id, hlight });
    } */
  },
};

export default MenuCardComponent;
