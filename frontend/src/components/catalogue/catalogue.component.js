import { UPLOAD_MODAL_EVENT } from '@/strings/event-strings';
import template from './catalogue.html';
import styles from './catalogue.scss';

const VIEW_STRINGS = {
  title: 'NS catalogue',
  button: 'Onboard NS',
  tableTitle: 'Catalogue',
  modalTitle: 'Details',
  modalTitle2: 'Descriptor',
  close: 'Close',
  validations: 'Validation',
  deleteModalTitle: 'Delete NS',
  deleteButton: 'Delete',
  cancelButton: 'Cancel',
  confirmDelete: 'Are you sure you want to delete the NS',
  modalTitleBilling: 'Assign Billing for NS',
};

const TABLE_HEADERS = {
  capabilities: 'Capabilities',
  _created: 'Enrolled',
};

const MODAL_ENTRIES = {
  _id: 'Id',
  capabilities: 'Capabilities',
  _created: 'Enrolled',
  _updated: 'Updated',
  state: 'State',
  vendor: 'Vendor',
};

export const CatalogueComponent = {
  template,
  controller: class CatalogueComponent {
    constructor($scope, toastr, CatalogueService, AuthService, VNSFService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.modalEntries = MODAL_ENTRIES;
      this.scope = $scope;
      this.toast = toastr;
      this.catalogueService = CatalogueService;
      this.authService = AuthService;
      this.createOpen = false;
      this.deleteOpen = false;
      this.detailsOpen = false;
      this.billingOpen = false;
      this.offset = 1;
      this.limit = 25;
      this.isLoading = false;
      this.isLoadingBilling = false;
      this.filters = {};
      this.vnsfsService = VNSFService;
      this.selectNS = null;

      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'View',
            action: this.toggleDetailsModal.bind(this),
          },
        ],
      };

      if (this.authService.isUserTenantAdmin()) {
        this.headers.actions = [
          ...this.headers.actions,
          {
            label: 'Enroll',
            action: this.addToInventory.bind(this),
          },
        ];
      } else if (this.authService.isUserPlatformAdmin()) {
        this.headers.actions = [
          ...this.headers.actions,
          {
            label: 'Delete',
            action: this.toggleDeleteModal.bind(this),
          },
          {
            label: 'Billing Fee',
            action: this.toggleBillingFee.bind(this),
          },
        ];
      }

      this.billing = {
        table: {
          title: 'Simulation Results',
          headers: {
            parameter: 'Parameter',
            description: 'Description',
            ns_instances: '# NS Instances',
            fee: 'Fee',
          },
        },
        input: {
          labelTotal: 'Total monthly expense fee',
          labelMonthly: 'Specify monthly fee per instance',
        },
        button: {
          simulate: 'Simulate',
          apllyFee: 'Apply Fee',
        },
      };
    }


    $onInit() {
      this.getData();
    }

    getData() {
      this.isLoading = true;
      this.catalogueService.getCatalogueServices({
        page: this.offset,
        limit: this.limit,
      }, this.filters)
        .then((items) => {
          this.items = items.map(item => ({
            ...item,
            capabilities: item.manifest['manifest:ns'].properties.capabilities.join(', '),
          }));
        })
        .finally(() => { this.isLoading = false; });
    }

    addToInventory({ _id }) {
      this.catalogueService.addServiceToInventory(_id);
    }

    toggleBillingFee(ns) {
      this.billingOpen = !this.billingOpen;
      if (this.billingOpen) {
        this.selectNS = ns;
        this.getInfoBilling();
      }
    }

    getInfoBilling() {
      this.infoBilling = {};
      this.isLoadingBilling = true;
      this.catalogueService.getBillingFeeService(this.selectNS._id).then((info) => {
        this.infoBilling = {
          fee: info.fee,
          expense_fee: info.expense_fee,
          nsId: info.ns_id,
          etag: info._etag,
        };
      }).finally(() => {
        this.isLoadingBilling = false;
        this.getBillingSimulation();
      });
    }

    getBillingSimulation() {
      this.catalogueService.simulateBillingFee(this.infoBilling)
        .then((data) => {
          this.infoTableBilling = [
            {
              parameter: 'Required Instances',
              description: 'Balance of a single instance (expense fee minus specified fee)',
              ns_instances: data.instance_balance[0],
              fee: data.instance_balance[1],
            },
            {
              parameter: 'Active instances usage',
              description: 'Current active instances usage (assumed for active for the entire month)',
              ns_instances: data.running_instances[0],
              fee: data.running_instances[1],
            },
            {
              parameter: 'Balance per instance',
              description: 'Minimum amount of instances to achieve profitablility',
              ns_instances: data.flatten_min_instances[0],
              fee: data.flatten_min_instances[1],
            },
            {
              parameter: 'Balance',
              description: '',
              ns_instances: '',
              fee: data.total_balance,
            },
          ];
        });
    }

    getBillingApllyFee() {
      this.catalogueService.getBillingFeeService(this.selectNS._id).then((info) => {
        this.infoBilling.etag = info._etag;
      })
      .finally(() => {
        this.applyFee();
      });
    }

    applyFee() {
      this.catalogueService.applyFeeBilling(this.infoBilling)
      .then(() => {
        this.billingOpen = !this.billingOpen;
        this.toast.success('Fee update successfully', 'Fee update');
      });
    }

    toggleDetailsModal(ns) {
      this.ns = ns;
      this.detailsOpen = !this.detailsOpen;
    }

    changeCurrFee(key, value) {
      this.infoBilling[key] = parseFloat(value, 10);
    }

    toggleFileUploadModal() {
      this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.OPEN, {
        fileType: '.tar.gz',
        fileSize: null,
        uploadTitle: this.viewStrings.button,
      });
    }

    toggleDeleteModal(ns) {
      this.ns = ns;
      this.deleteModalOpen = !this.deleteModalOpen;
    }

    deleteNs() {
      this.vnsfsService.deleteNs(this.ns)
        .then(() => {
          this.toast.success('NS deleted successfully', 'NS delete');
          this.toggleDeleteModal();
          this.getData();
        });
    }

    uploadApp(file) {
      try {
        this.vnsfsService.uploadNS(file)
          .then((data) => {
            this.toast.success('NS file uploaded', 'Successful onboard');
            this.getData();
            this.catalogueService.createBillingService(data._id);
          })
          .finally(() => {
            this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
            this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
          });
      } catch (e) {
        this.toast.error('NS can\'t be created', this.viewStrings.uploadError);
        this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
        this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
      }
    }
  },
};

export const catalogueState = {
  parent: 'home',
  name: 'nscatalogue',
  url: '/catalogue',
  component: 'catalogueView',
};

