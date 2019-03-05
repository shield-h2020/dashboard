import template from './billing-detail.html';
import styles from './billing-detail.scss';

const VIEW_STRINGS = {
  title: 'Billing Detail',
  tableTitle: 'Billing Detail',
  button: 'Back',
};

const TABLE_HEADERS_NS = {
  ns_id: 'Network Service',
  ns_instance_id: 'Instance ID',
  usage_status: 'Status',
  used_from: 'Used from',
  used_to: 'Used to',
  fee: 'Monthly fee (€)',
  billable_percentage: 'Monthly usage (%)',
  billable_fee: 'Billable Fee (€)',
};

const TABLE_HEADERS_VNSF = {
  vnsf_id: 'vNSF',
  usage_status: 'Status',
  used_from: 'Used from',
  used_to: 'Used to',
  fee: 'Monthly fee (€)',
  billable_percentage: 'Monthly usage (%)',
  billable_fee: 'Amount (€)',
};

const TABLE_HEADERS_NS_ADMIN = {
  tenant_id: 'Tenant ID',
  ns_id: 'Network Service',
  ns_instance_id: 'Instance ID',
  usage_status: 'Instance Status',
  used_from: 'Used from',
  used_to: 'Used to',
  fee: 'Monthly fee (€)',
  billable_percentage: 'Monthly usage (%)',
  billable_fee: 'Billable Fee (€)',
};

const TABLE_HEADERS_VNSF_ADMIN = {
  user_id: 'User ID',
  vnsf_id: 'vNSF',
  usage_status: 'Status',
  used_from: 'Used from',
  used_to: 'Used to',
  fee: 'Monthly fee (€)',
  billable_percentage: 'Monthly usage (%)',
  billable_fee: 'Expense Fee (€)',
};

export const BillingDetailComponent = {
  template,
  controller: class BillingDetailComponent {
    constructor($scope, toastr, $stateParams, VNSFService, BillingDetailService, AuthService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.month = $stateParams.year_month;
      this.vNSFService = VNSFService;
      this.scope = $scope;
      this.toast = toastr;
      this.billingDetailService = BillingDetailService;
      this.authService = AuthService;
      this.createOpen = false;
      this.deleteOpen = false;
      this.detailsOpen = false;
      this.offset = 1;
      this.limit = 25;
      this.isLoading = false;
      this.filters = {};
      this.showTableAdmin = false;

      if (this.authService.isUserDeveloper()) {
        this.headers = TABLE_HEADERS_VNSF;
      } else if (this.authService.isUserTenantAdmin()) {
        this.headers = TABLE_HEADERS_NS;
      } else if (this.authService.isUserPlatformAdmin()) {
        this.headersNS = TABLE_HEADERS_NS_ADMIN;
        this.headersVNSFs = TABLE_HEADERS_VNSF_ADMIN;
      }
    }

    $onInit() {
      this.getData();
    }

    getData() {
      this.filters = { tenant_id: this.authService.getTenant(), month: this.month };
      this.isLoading = true;
      if (this.authService.isUserDeveloper()) {
        this.billingDetailService.getBillingUsageVNSF({ page: this.offset,
          limit: this.limit,
        }, this.filters)
          .then((items) => {
            this.items = items._items;
            this.items.push({ vnsf_id: 'Total Amount (€)', billable_fee: items.total_billable_fee });
          })
          .finally(() => { this.isLoading = false; });
      } else if (this.authService.isUserTenantAdmin()) {
        this.billingDetailService.getBillingUsageNS({ page: this.offset,
          limit: this.limit,
        }, this.filters)
          .then((items) => {
            this.items = items._items;
            this.items.push({ ns_id: 'Total Amount (€)', billable_fee: items.total_billable_fee });
          })
          .finally(() => { this.isLoading = false; });
      } else if (this.authService.isUserPlatformAdmin()) {
        this.showTableAdmin = true;
        this.billingDetailService.getBillingUsageNS({ page: this.offset,
          limit: this.limit,
        }, this.filters)
        .then((items) => {
          this.itemsNS = items._items;
          this.itemsNS.push({ tenant_id: 'Network Service Balance (€)', billable_fee: items.total_billable_fee });
          this.feeNS = items.total_billable_fee;
        })
        .finally(() => { this.isLoading = false; });

        this.billingDetailService.getBillingUsageVNSF({ page: this.offset,
          limit: this.limit,
        }, this.filters)
        .then((items) => {
          this.itemsVNSFs = items._items;
          this.itemsVNSFs.push({ user_id: 'VNSFs Balance (€)', billable_fee: items.total_billable_fee });
          this.feeVNSF = items.total_billable_fee;
        })
        .finally(() => { this.isLoading = false; });
      }
    }

    addToInventory({ _id }) {
      this.billingService.addServiceToInventory(_id);
    }

    toggleDetailsPage(billing) {
      this.state.go('history', { year_month: billing.month });
    }
  },
};

export const BillingDetailState = {
  parent: 'home',
  name: 'detail',
  url: '/detail/{year_month}',
  component: 'billingDetailView',
};

