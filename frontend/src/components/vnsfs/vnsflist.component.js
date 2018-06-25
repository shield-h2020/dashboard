import { UPLOAD_MODAL_EVENT } from '@/strings/event-strings';
import template from './vnsflist.html';
import styles from './vnsf.scss';

const VIEW_STRINGS = {
  title: 'vNSF Catalogue',
  tableTitle: 'Catalogue',
  button: 'Onboard vNSF',
  modalHeaders: {
    _id: 'Id',
    _created: 'Created',
    _updated: 'Updated',
    state: 'State',
    vendor: 'Vendor',
  },
  modalTitle: 'vNSF details',
  modalTitle2: 'Descriptor (yaml)',
  modalTitle3: 'Security Info',
  close: 'close',
  uploadError: 'Error uploading app file',
};

const TABLE_HEADERS = {
  _id: 'Id',
  state: 'State',
  vendor: 'Vendor',
};

export const VNSFListComponent = {
  template,
  controller: class VNSFListComponent {
    constructor($state, $scope, toastr, VNSFService) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.styles = styles;
      this.state = $state;
      this.scope = $scope;
      this.toast = toastr;
      this.vnsfsService = VNSFService;

      this.tableHeaders = {
        ...TABLE_HEADERS,
        actions: [
          {
            label: 'view',
            action: this.toggleVNSFDetails.bind(this),
          },
        ],
      };
      this.page = 0;
      this.filters = {};
      this.items = [];
      this.currVnsf = null;
      this.modalOpen = false;
      this.modalControls = {
        descriptorExpanded: false,
        securityExpanded: false,
      };
    }

    $onInit() {
      this.vnsfsService.getAllVNSFs(this.page, this.filters)
        .then((data) => {
          this.items = [...data.items];
        });
    }

    toggleVNSFDetails(vnsf) {
      this.currVnsf = vnsf;
      this.modalOpen = !this.modalOpen;
    }

    prettyJSON(obj) {
      return JSON.stringify(obj, null, 2);
    }

    toggleFileUploadModal() {
      this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.OPEN, {
        fileType: '.tar.gz',
        fileSize: null,
        uploadTitle: this.viewStrings.button,
      });
    }

    uploadApp(file) {
      try {
        this.vnsfsService.uploadVNSF(file)
          .then(() => {
            this.toast.success('vNSF file uploaded', 'Successful onboard');
            this.getData();
          })
          .finally(() => {
            this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
            this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
          });
      } catch (e) {
        this.toast.error('vNSF can\'t be created', this.viewStrings.uploadError);
        this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
        this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
      }
    }
  },
};

export default VNSFListComponent;

export const vnsfListState = {
  parent: 'home',
  name: 'vnsfslist',
  url: '/vnsflist',
  component: 'vnsfsListView',
};
