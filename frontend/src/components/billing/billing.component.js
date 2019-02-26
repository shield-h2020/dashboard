import template from './billing.html';
import styles from './billing.scss';

const VIEW_STRINGS = {
  title: 'Billing',
  tableTitle: 'Billing',
};

const TABLE_HEADERS_NS = {
  month: 'Year-Month',
  number_nss: '# Network Services',
  number_ns_instances: '# NS Instances',
  status: 'Status',
  billable_fee: 'Billable Fee (€)',
};

const TABLE_HEADERS_VNSF = {
  month: 'Year-Month',
  number_vnsfs: '# VNSFs',
  status: 'Status',
  billable_fee: 'Profitable Fee (€)',
};

const TABLE_HEADERS_ADMIN = {
  month: 'Year-Month',
  number_tenants: '# Tenants',
  number_nss: '# Network Services',
  number_ns_instances: '# NS Instances',
  number_vnsfs: '# VNSFs',
  status: 'Status',
  profit_balance: 'Profit Balance (€)',
};

export const BillingComponent = {
  template,
  controller: class BillingComponent {
    constructor($scope, $state, toastr, BillingService, AuthService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.scope = $scope;
      this.state = $state;
      this.toast = toastr;
      this.billingService = BillingService;
      this.authService = AuthService;
      this.createOpen = false;
      this.deleteOpen = false;
      this.detailsOpen = false;
      this.offset = 1;
      this.limit = 25;
      this.isLoading = false;
      this.filters = {};
      if (this.authService.isUserTenantAdmin()) {
        this.headers = {
          ...TABLE_HEADERS_NS,
          actions: [
            {
              label: 'Details',
              action: this.goToDetailsPage.bind(this),
            },
          ],
        };
      } else if (this.authService.isUserDeveloper()) {
        this.headers = {
          ...TABLE_HEADERS_VNSF,
          actions: [
            {
              label: 'Details',
              action: this.goToDetailsPage.bind(this),
            },
          ],
        };
      } else if (this.authService.isUserPlatformAdmin()) {
        this.headers = {
          ...TABLE_HEADERS_ADMIN,
          actions: [
            {
              label: 'Details',
              action: this.goToDetailsPage.bind(this),
            },
          ],
        };
      }
    }

    $onInit() {
      this.getData();
    }

    getData() {
      this.isLoading = true;
      this.filters = { tenant_id: this.authService.getTenant() };
      if (this.authService.isUserDeveloper()) {
        this.billingService.getBillingSummaryVNSF({ page: this.offset,
          limit: this.limit,
        })
          .then((items) => {
            this.items = items;
          })
          .finally(() => { this.isLoading = false; });
      } else if (this.authService.isUserTenantAdmin()) {
        this.billingService.getBillingSummaryNS({ page: this.offset,
          limit: this.limit,
        }, this.filters)
          .then((items) => {
            this.items = items;
          })
          .finally(() => { this.isLoading = false; });
      } else if (this.authService.isUserPlatformAdmin()) {
        this.billingService.getBillingSummary({ page: this.offset,
          limit: this.limit,
        })
          .then((items) => {
            this.items = items;
          })
          .finally(() => { this.isLoading = false; });
      }
    }

    goToDetailsPage({ month }) {
      this.state.go('detail', { year_month: month });
    }
  },
};

export const BillingState = {
  parent: 'home',
  name: 'billing',
  url: '/billing',
  component: 'billingView',
};

