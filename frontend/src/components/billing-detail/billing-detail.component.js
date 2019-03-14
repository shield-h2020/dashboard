import template from './billing-detail.html';
import styles from './billing-detail.scss';

const VIEW_STRINGS = {
  title: 'Billing Detail',
  tableTitle: 'Billing Detail',
  button: 'Back',
};

const TABLE_HEADERS_NS = {
  ns_name: 'Network Service',
  ns_instance_id: 'Instance ID',
  usage_status: 'Status',
  used_from: 'Used from',
  used_to: 'Used to',
  fee: 'Monthly fee (€)',
  billable_percentage: 'Monthly usage (%)',
  billable_fee: 'Billable Fee (€)',
};

const TABLE_HEADERS_VNSF = {
  vnsf_name: 'vNSF',
  usage_status: 'Status',
  used_from: 'Used from',
  used_to: 'Used to',
  fee: 'Monthly fee (€)',
  billable_percentage: 'Monthly usage (%)',
  billable_fee: 'Amount (€)',
};

const TABLE_HEADERS_NS_ADMIN = {
  tenant_name: 'Client',
  ns_name: 'Network Service',
  ns_instance_id: 'Instance ID',
  usage_status: 'Instance Status',
  used_from: 'Used from',
  used_to: 'Used to',
  fee: 'Monthly fee (€)',
  billable_percentage: 'Monthly usage (%)',
  billable_fee: 'Billable Fee (€)',
};

const TABLE_HEADERS_VNSF_ADMIN = {
  user_name: 'User',
  vnsf_name: 'vNSF',
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
      this.pagination = {
        page: 1,
        limit: 12,
        totalItems: null,
      };
      this.paginationVNSFs = {
        page: 1,
        limit: 5,
        totalItems: null,
      };
      this.paginationNS = {
        page: 1,
        limit: 5,
        totalItems: null,
      };
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
      this.isLoading = true;
      if (this.authService.isUserDeveloper()) {
        this.filters = { tenant_id: this.authService.getTenant(), month: this.month };
        this.billingDetailService.getBillingUsageVNSF(this.pagination, this.filters)
          .then((items) => {
            this.items = items._items;
            this.pagination.totalItems = items._meta.total ? items._meta.total : 0;
            this.feed = items.total_billable_fee || 0;
            this.paging = this.calcPageItems();
          })
          .finally(() => { this.isLoading = false; });
      } else if (this.authService.isUserTenantAdmin()) {
        this.filters = { tenant_id: this.authService.getTenant(), month: this.month };
        this.billingDetailService.getBillingUsageNS(this.pagination, this.filters)
          .then((items) => {
            this.items = items._items;
            this.pagination.totalItems = items._meta.total ? items._meta.total : 0;
            this.feed = items.total_billable_fee || 0;
            this.paging = this.calcPageItems();
          })
          .finally(() => { this.isLoading = false; });
      } else if (this.authService.isUserPlatformAdmin()) {
        this.filters = { month: this.month };
        this.showTableAdmin = true;
        this.billingDetailService.getBillingUsageNS(this.paginationNS, this.filters)
        .then((items) => {
          this.itemsNS = items._items;
          this.paginationNS.totalItems = items._meta.total ? items._meta.total : 0;
          this.feedNS = items.total_billable_fee || 0;
          this.pagingNS = this.calcPageItemsNS();
        })
        .finally(() => { this.isLoading = false; });

        this.billingDetailService.getBillingUsageVNSF(this.paginationVNSFs, this.filters)
        .then((items) => {
          this.itemsVNSFs = items._items;
          this.paginationVNSFs.totalItems = items._meta.total ? items._meta.total : 0;
          this.feedVNSFs = items.total_billable_fee || 0;
          this.pagingVNSFs = this.calcPageItemsVNFs();
        })
        .finally(() => { this.isLoading = false; });
      }
    }

    addToInventory({ _id }) {
      this.billingService.addServiceToInventory(_id);
    }

    changePage(amount) {
      const { page, totalItems, limit } = this.pagination;
      const numberOfPages = Math.ceil(totalItems / limit);
      const condition = amount > 0 ?
       page + 1 <= numberOfPages : this.paginationNS.page > 1;
      if (condition) {
        this.paginationNS.page += amount;
        this.getData();
      }
    }

    calcPageItems() {
      const { page, totalItems, limit } = this.pagination;
 
      const numberOfPages = Math.ceil(totalItems / limit);
      return { page, totalPage: numberOfPages, total: totalItems };
    }

    changePageNS(amount) {
      const { page, totalItems, limit } = this.paginationNS;
      const numberOfPages = Math.ceil(totalItems / limit);
      const condition = amount > 0 ?
       page + 1 <= numberOfPages : this.paginationNS.page > 1;
      if (condition) {
        this.paginationNS.page += amount;
        this.getData();
      }
    }

    calcPageItemsNS() {
      const { page, totalItems, limit } = this.paginationNS;
      console.log(page, totalItems, limit)
      
      const numberOfPages = Math.ceil(totalItems / limit);
      return { page, totalPage: numberOfPages, total: totalItems };
    }

    changePageVNFs(amount) {
      const { page, totalItems, limit } = this.paginationVNSFs;
      const numberOfPages = Math.ceil(totalItems / limit);
      const condition = amount > 0 ?
       page + 1 <= numberOfPages : this.paginationNS.page > 1;
      if (condition) {
        this.paginationNS.page += amount;
        this.getData();
      }
    }

    calcPageItemsVNFs() {
      const { page, totalItems, limit } = this.paginationVNSFs;
      
      const numberOfPages = Math.ceil(totalItems / limit);
      return { page, totalPage: numberOfPages, total: totalItems };
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

