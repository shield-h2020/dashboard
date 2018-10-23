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
      this.offset = 1;
      this.limit = 25;
      this.isLoading = false;
      this.filters = {};
      this.vnsfsService = VNSFService;

      this.headers = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.toggleDetailsModal.bind(this),
          },
          {
            label: 'delete',
            action: this.toggleDeleteModal.bind(this),
          },
        ],
      };

      if (this.authService.isUserTenantAdmin()) {
        this.headers.actions = [
          ...this.headers.actions,
          {
            label: 'enroll',
            action: this.addToInventory.bind(this),
          },
        ];
      }
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

    toggleDetailsModal(ns) {
      this.ns = ns;
      this.detailsOpen = !this.detailsOpen;
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
          .then(() => {
            this.toast.success('NS file uploaded', 'Successful onboard');
            this.getData();
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

