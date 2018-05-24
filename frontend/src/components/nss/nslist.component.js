import template from './nslist.html';
import { UPLOAD_MODAL_EVENT } from '../../strings/event-strings';

const UI_STRINGS = {
  title: 'NS Store',
  button: 'Onboard NS',
  table: {
    title: 'NS Store',
    headers: [
      { label: 'Id', key: '_id' },
      { label: 'State', key: 'state' },
    ],
    actions: ['details'],
  },
};

export const NSListComponent = {
  template,
  controller: class NSListComponent {
    constructor($state, $scope, toastr, NSService) {
      'ngInject';

      this.strings = UI_STRINGS;
      this.state = $state;
      this.scope = $scope;
      this.toast = toastr;
      this.nssService = NSService;
      this.isLoading = true;
      this.modalOpen = false;
      this.selectedNS = null;
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
      return this.nssService.getAllNSs(pagination, filters);
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
        this.nssService.updateApp(id, parsed)
          .finally(() => {
            this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
          });
      } catch (e) {
        this.toast.error('NS can\'t be creacted', this.strings.ERROR.INVALID_JSON);
        this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
      }
    }

    modalHandler(value) {
      this.modalOpen = value;
    }

    uploadApp(file) {
      this.nssService.uploadNS(file)
        .then(() => {
          this.toast.success('NS onboarded', '', {
            onHidden: () => { this.refreshTable = true; },
          });
          this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
        })
        .finally(() => {
          this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.CLOSE);
          this.scope.$broadcast(UPLOAD_MODAL_EVENT.CAST.LOADING);
        });
    }

    onAction(ns, action) {
      switch (action) {
        case 'details':
          this.selectedNS = ns;
          this.modalOpen = true;
          break;
        default:
      }
    }
  },
};

export const nsListState = {
  parent: 'home',
  name: 'nsslist',
  url: '/nslist',
  component: 'nssListView',
};
