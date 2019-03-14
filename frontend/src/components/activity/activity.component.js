import { UPLOAD_MODAL_EVENT } from '@/strings/event-strings';
import template from './activity.html';
import styles from './activity.scss';
import moment from 'moment';

const VIEW_STRINGS = {
  title: 'Activivty',
  tableTitle: 'Activivty',
};

const TABLE_HEADERS = {
  date: 'Date',
  tenant_name: 'Client',
  user_name: 'User',
  log: 'Log',
};

export const ActivityComponent = {
  template,
  controller: class ActivityComponent {
    constructor($scope, toastr, ActivityService, AuthService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.scope = $scope;
      this.toast = toastr;
      this.activityService = ActivityService;
      this.authService = AuthService;
      this.customStart = null;
      this.customEnd = null;
      this.pagination = {
        page: 1,
        limit: 10,
        totalItems: null,
      };
      this.isLoading = false;
      this.filters = {};
      if (this.authService.isUserPlatformAdmin()) {
        this.headers = { ...TABLE_HEADERS };
      } else {
        delete TABLE_HEADERS.tenant_name;
        this.headers = { ...TABLE_HEADERS };
      }
    }

    $onInit() {
      this.setPeriod();

      this.setFilter = (eData) => {
        if (eData.key === 'startDate') {
          this.customStart = eData.value;
        }
        if (eData.key === 'endDate') {
          this.customEnd = eData.value;
        }
        this.scope.startDate = moment(this.customStart).format('YYYY-MM-DDTHH:mm:ss');
        this.scope.endDate = moment(this.customEnd).format('YYYY-MM-DDTHH:mm:ss');

        this.refreshPage();
      };
    }

    getData() {
      this.items = [];
      this.isLoading = true;
      this.filters = {
        timestamp: {
          $gte: moment(this.scope.start).unix(),
          $lte: moment(this.scope.end).unix(),
        },
      };

      if (this.authService.isUserPlatformAdmin()) {
        this.activityService.getActivitys(this.pagination, this.filters)
          .then((items) => {
            items._items.forEach(item => this.items.push({
              log: item.message,
              date: `${moment.unix(item.timestamp).format('YYYY-MM-DDTHH:mm:ss')}Z`,
              user_name: item.user_name,
              tenant_name: item.tenant_name,
            }),
            );
            this.pagination.totalItems = items ? items._meta.total : 0;
            this.paging = this.calcPageItems();
          })
          .finally(() => { this.isLoading = false; });
      } else {
        this.filters.tenant_id = this.authService.getTenant();
        this.activityService.getActivitys(this.pagination, this.filters)
          .then((items) => {
            items._items.forEach(item => this.items.push({
              log: item.message,
              date: `${moment.unix(item.timestamp).format('YYYY-MM-DDTHH:mm:ss')}Z`,
              user_name: item.user_name,
            }),
            );
            this.pagination.totalItems = items ? items._meta.total : 0;
            this.paging = this.calcPageItems();
          })
          .finally(() => { this.isLoading = false; });
      }
    }

    changePage(amount) {
      const { page, totalItems, limit } = this.pagination;
      const numberOfPages = Math.ceil(totalItems / limit);
      const condition = amount > 0 ?
       page + 1 <= numberOfPages : this.pagination.page > 1;
      if (condition) {
        this.pagination.page += amount;
        this.getData();
      }
    }

    calcPageItems() {
      const { page, totalItems, limit } = this.pagination;

      const numberOfPages = Math.ceil(totalItems / limit);
      return { page, totalPage: numberOfPages, total: totalItems };
    }

    setPeriod() {
      this.scope.startDate = moment()
      .startOf('day')
      .format('YYYY-MM-DDTHH:mm:ss');
      this.scope.endDate = moment()
      .endOf('day')
      .format('YYYY-MM-DDTHH:mm:ss');
      this.LastStartDate = this.scope.startDate;
      this.LastEndDate = this.scope.endDate;
    }

    refreshPage() {
      this.scope.start = `${this.scope.startDate}`;
      this.scope.end = `${this.scope.endDate}`;
      this.getData();
    }
  },

};

export const activityState = {
  parent: 'home',
  name: 'activity',
  url: '/activity',
  component: 'activityView',
};

