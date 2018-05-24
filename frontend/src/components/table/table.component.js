import template from './table.html';
import { UI_STRINGS, TOKEN } from './table.strings';

import styles from './table.scss';

function debounce(func, wait, immediate, context = this, ...args) {
  let timeout;
  return () => {
    const later = () => {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

export const TableComponent = {

  template,
  bindings: {
    config: '<',
    actions: '<?',
    actionsCallback: '&',
    needsRefresh: '<?',
    hasDate: '<',
    pagination: '<',
    filterInputs: '<',
    autoCall: '<',
  },
  controller: class TableComponent {
    constructor() {
      this.isLoading = false;
      this.strings = UI_STRINGS;
      this.items = [];
      this.select = [];
      this.filters = {};
      this.styles = styles;
      this.fetchNewData = debounce(this.fetchNewData, 100, true, this);
    }

    $onInit() {
      if (!this.pagination) {
        this.pagination = {
          page: 1,
          limit: 10,
        };
      }
      this.readConfig();
      if (this.autoCall) {
        this.fetchNewData();
      }

      this.calcPageItems();
    }

    fetchNewData() {
      this.isLoading = true;
      this.items = [];
      const { source } = this.config;
      if (source) {
        source({ pagination: this.pagination, filters: this.filters })
        .then((data) => {
          this.getData(data && data.items);
          this.pagination.total = (data && data.meta.total) || 0;
        });
      }
    }

    changePage(amount) {
      const condition = amount > 0 ?
        this.items.length >= this.pagination.limit : this.pagination.page > 0;
      if (condition) {
        this.pagination.page += amount;
        this.fetchNewData();
      }
    }

    $onChanges(changesObj) {
      if (changesObj.needsRefresh && changesObj.needsRefresh.currentValue) {
        this.fetchNewData();
      }
    }

    setPagination(meta) {
      this.pagination.total = meta.total;
    }

    changePagination(value) {
      this.pagination.limit = value;
      this.fetchNewData();
    }

    getData(data) {
      if (!data || !Array.isArray(data)) {
        this.isLoading = false;
        this.items = null;
      } else {
        this.isLoading = false;
        this.items.push(...data);
        this.paging = this.calcPageItems();
      }
    }

    calcPageItems() {
      const { page, limit } = this.pagination;
      const length = this.items.length || 10;

      const res = ((page * limit) - (length < limit ? limit : length)) + 1;
      const res2 = (page * limit) + (length < limit ? -(limit - length) : 0);

      return { min: res, max: res2 };
    }

    setFilter(filter) {
      if (filter.key === 'startDate' || filter.key === 'endDate') {
        const query = filter.key === 'startDate' ? '$gte' : '$lte';
        if (!this.filters.detection) this.filters.detection = {};
        const date = new Date(filter.value);
        if (filter.key === 'endDate') {
          date.setSeconds(59);
        }
        this.filters.detection[query] = date.toUTCString();
      } else if (filter.key === 'status') {
        if (filter.value === 'any') {
          delete this.filters.status;
        } else {
          this.filters[filter.key] = filter.value;
        }
      } else {
        this.filters[filter.key] = filter.value;
      }

      this.fetchNewData();
    }

    removeFilter(key) {
      delete this.filters[key];
    }

    setStartDate() {
      this.startDate = new Date();
      this.startDate.setFullYear(this.startDate.getFullYear() - 1);

      return this.startDate.toString();
    }

    readConfig() {
      this.headers = this.config.headers.map(conf => conf.header);
      this.keys = this.config.headers.map(conf => conf.key);
      if (this.config.rowSizes) {
        this.buildSelect();
      }
    }

    action(actionLabel, item) {
      this.actionsCallback({
        $event: {
          value: {
            item,
            action: actionLabel,
          },
        },
      });
    }

    buildSelect() {
      this.config.rowSizes.forEach((size) => {
        this.select.push(
          {
            value: size,
            text: this.strings.select.replace(TOKEN, size),
          });
      });
    }
  },
};

export default TableComponent;
