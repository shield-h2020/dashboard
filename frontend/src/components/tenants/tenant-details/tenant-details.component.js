import template from './tenant-details.html';

const VIEW_STRINGS = {
  title: 'SecaaS client',
  tenantEntries: {
    tenant_name: 'Client name',
    description: 'Client description',
    ips: 'Client IPs',
  },
};

export const TenantDetailsComponent = {
  template,
  controller: class TenantDetailsComponent {
    constructor(TenantsService) {
      'ngInject';

      this.tenantsService = TenantsService;
      this.viewStrings = VIEW_STRINGS;

      this.isLoading = false;
    }

    $onInit() {
      this.getTenant();
    }

    getTenant() {
      this.isLoading = true;
      this.tenantsService.getTenant()
        .then((tenant) => {
          this.tenant = tenant;
          this.isLoading = false;
        });
    }
  },
};

export default TenantDetailsComponent;
