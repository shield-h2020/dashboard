import template from './table.html';
import styles from './table.scss';

export const TableComponent = {
  template,
  bindings: {
    items: '<',
    headers: '<',
    loading: '<',
  },
  controller: class TableComponent {
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

export default TableComponent;
