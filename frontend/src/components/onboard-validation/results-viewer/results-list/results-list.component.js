import template from './results-list.html';
// import { GRAPH_EVENT } from '../../../services/event-strings';

export const ResultsListComponent = {
  template,
  bindings: {
    fwgraphs: '<',
    type: '<',
    items: '<',
  },
  controller: class ResultsListComponent {
    constructor($scope, $filter) {
      'ngInject';

      this.scope = $scope;
      this.filter = $filter('fwgFilter');
      this.isCollapsed = true;
      this.filteredItems = [];
    }

    $onInit() {
/*       this.scope.$on(GRAPH_EVENT.CAST, () => {
        this.filteredItems = [...this.filter(this.items, this.fwgraphs)];
      }); */
    }

    $onChanges(changesObj) {
      if (changesObj.items && changesObj.items.currentValue.length) {
        this.items = [...changesObj.items.currentValue];
        this.filteredItems = [...this.items];
      } else if (changesObj.items && !changesObj.items.currentValue.length) {
        this.items = [];
        this.filteredItems = [];
      }
    }

    toggleListCollapse() {
      this.isCollapsed = !this.isCollapsed;
    }
  },
};

export default ResultsListComponent;
