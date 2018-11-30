import template from './table-custom-actions.html';
import styles from './table-custom-actions.scss';

export const TableCustomActionsComponent = {
  template,
  bindings: {
    items: '<',
    headers: '<',
    loading: '<',
    buttonclicked: '<'
  },
  controller: class TableCustomActionsComponent {
    constructor() {
      this.styles = styles;
      this.strings = {
        loading: 'Loading data, please wait…',
        noData: 'No data to display',
      };
    }

    specialCell(item) {
      if (item.status === 'error') return 'error';
      if (item.status === 'warn') return 'warn';

      return '';
    }
  },
};

export default TableCustomActionsComponent;
