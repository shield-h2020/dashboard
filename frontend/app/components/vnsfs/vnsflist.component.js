import template from './vnsflist.html';
import { UPLOAD_MODAL_EVENT } from '../../strings/event-strings';

const UI_STRINGS = {
  title: 'VNSF Store',
  button: 'Onboard VNSF',
  table: {
    title: 'VNSF Store',
    headers: [
      { label: 'Id', key: '_id' },
      { label: 'State', key: 'state' },
      { label: 'Vendor', key: 'vendor' },
    ],
    actions: ['details'],
  },
};

export const VNSFListComponent = {
  template,
  controller: class VNSFListComponent {
    constructor($state, $scope, toastr, VNSFService) {
      'ngInject';

      this.strings = UI_STRINGS;
      this.state = $state;
      this.scope = $scope;
      this.toast = toastr;
      this.vnsfsService = VNSFService;
      this.isLoading = true;
      this.modalOpen = false;
      this.selectedVNSF = null;
      this.tableConf = {
        headers: [],
      };

      UI_STRINGS.table.headers.forEach((header) => {
        this.tableConf.headers.push({
          header: header.label,
          key: header.key,
        });
      });
      this.tableConf.hasEnable = {
        key: 'status',
        value: 'ENABLED',
      };
      this.tableConf.rowSizes = [10, 20, 30];
    }

    $onInit() {
      this.strings.button = this.strings.button;
    }

    tableSource(pagination, filters) {
      this.refreshTable = false;
      return this.vnsfsService.getAllVNSFs(pagination, filters);
    }

    fileCreateApp() {
      this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.OPEN, {
        fileType: '.tar.gz',
        fileSize: null,
        uploadTitle: this.strings.button,
      });
    }

    updateApp(id, app) {
      let parsed;
      try {
        parsed = JSON.parse(app);
        this.vnsfsService.updateApp(id, parsed)
          .finally(() => {
            this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
          });
      } catch (e) {
        this.toast.error('vNSF can\'t be creacted', this.strings.ERROR.INVALID_JSON);
        this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
      }
    }

    modalHandler(value) {
      this.modalOpen = value;
    }

    uploadApp(file) {
      this.vnsfsService.uploadVNSF(file)
        .then(() => {
          this.toast.success('vNSF onboarded', '', {
            onHidden: () => { this.refreshTable = true; },
          });
          this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
        })
        .finally(() => {
          this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
          this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
        });
    }

    onAction(vnsf, action) {
      switch (action) {
        case 'details':
          this.selectedVNSF = vnsf;
          this.modalOpen = true;
          break;
        default:
      }
    }
  },
};

export const vnsfListState = {
  parent: 'home',
  name: 'vnsfslist',
  url: '/vnsflist',
  component: 'vnsfsListView',
};
