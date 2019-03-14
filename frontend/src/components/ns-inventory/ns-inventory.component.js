import template from './ns-inventory.html';
import styles from './ns-inventory.scss';
import * as YAML from 'yamljs';


const VIEW_STRINGS = {
  title: 'NS inventory',
  tableTitle: 'Inventory',
  modalTitle: 'NS Details',
  close: 'Close',
};

const TABLE_HEADERS = {
  ns_name: 'Nework Services',
  capabilities: 'Capabilities',
  status: 'Status',
  instance_id: 'Instance ID',
  actions: 'Actions',
};

const MODAL_ENTRIES = {
  _id: 'Id',
  capabilities: 'Capabilities',
  _created: 'Instantiated',
  type: 'Type',
  target: 'Target',
};

export const InventoryComponent = {
  template,
  controller: class InventoryComponent {
    constructor($scope, InventoryService, AuthService, toastr) {
      'ngInject';

      this.viewStrings = VIEW_STRINGS;
      this.modalEntries = MODAL_ENTRIES;
      this.styles = styles;
      this.inventoryService = InventoryService;
      this.authService = AuthService;
      this.toast = toastr;
      this.yaml = YAML;
      this.scope = $scope;
      this.createOpen = false;
      this.deleteOpen = false;
      this.nsIds = [];
      this.actionsItemAvailable = [
        {
          label: 'view',
          action: this.toggleNSDetails.bind(this),
        },
        {
          label: 'withdraw',
          action: this.removeFromInventory.bind(this),
        },
        {
          label: 'instantiate',
          action: this.instantiateToInventory.bind(this),
        },
      ];

      this.actionsItemConfiguring = [
        {
          label: 'view',
          action: this.toggleNSDetails.bind(this),
        },
      ];

      this.actionsItemRunning = [
        {
          label: 'view',
          action: this.toggleNSDetails.bind(this),
        },
        {
          label: 'terminate',
          action: this.stopInstance.bind(this),
        },
      ];

      this.pagination = {
        page: 1,
        limit: 10,
        totalItems: 0,
      };
      this.isLoading = false;
      this.filters = {};
      this.modalOpen = false;
      this.buttonClicked = false;
      this.nsSocketAtmp = 0;
      this.nsinventorySocket;
      this.headers = { ...TABLE_HEADERS };
    }

    $onInit() {
      this.initNsinventorySocket();

      this.scope.$on('NSINVENTORY_UPDATE_DATA', (event, data) => {
        this.getData();
      });

      this.getData();
    }

    $onDestroy() {
      this.nsSocketAtmp = 3;
      this.nsinventorySocket.close();
    }

    initNsinventorySocket() {
      this.nsinventorySocket = this.inventoryService.connectNSInventorySocket(
        this.authService.getTenant(),
      );
      this.nsinventorySocket.onopen = () => {
        this.nsSocketAtmp = 0;
      };
      this.nsinventorySocket.onmessage = (message) => {
        const data = JSON.parse(message.data);
        if (data.result === 'success') {
          this.toast.info(data.ns_name + ' is up and running', {
            onShown: () => {
              this.scope.$broadcast('NSINVENTORY_UPDATE_DATA');
            },
            closeButton: true,
          });
        } else {
          this.toast.error(`${data.ns_name} : failed to instantiate`, {
            onShown: () => {
              this.scope.$broadcast('NSINVENTORY_UPDATE_DATA');
            },
            closeButton: true,
          });
        }
      };
      this.nsinventorySocket.onclose = () => {
        if (this.nsSocketAtmp < 3) {
          this.nsSocketAtmp++;
          setTimeout(this.initNsinventorySocket(), 1000);
        }
      };
    }

    getData() {
      this.isLoading = true;
      this.inventoryService
        .getInventoryServices(this.pagination, this.filters)
        .then((result) => {
          this.items = [];
          result.items.filter(it => it).forEach((item) => {
            let selectedActions = [];
            if (item.status === 'available') {
              selectedActions = this.actionsItemAvailable;
            } else if (item.status === 'running') {
              selectedActions = this.actionsItemRunning;
            } else {
              selectedActions = this.actionsItemConfiguring;
              item.instance_id = 'N.A';
            }
            this.items.push({
              ...item,
              capabilities: item.manifest[
              'manifest:ns'
              ].properties.capabilities.join(', '),
              headerActions: selectedActions,
            });
            this.items.map((data) => 
              data.instance_id === '' ? data.instance_id = 'N.A' : data.instance_id = data.instance_id);
          });
          this.pagination.totalItems = result ? result.meta.total : 0;
          this.paging = this.calcPageItems();
        })
        .finally(() => {
          this.isLoading = false;
        });
    }

    toggleNSDetails(ns) {
      if (ns) {
        this.ns = {
          ...ns,
          type: ns.manifest['manifest:ns'].type,
          target: ns.manifest['manifest:ns'].target,
        };
      }
      this.modalOpen = !this.modalOpen;
    }

    removeFromInventory({ _id, _etag }) {
      this.buttonClicked = true;
      this.inventoryService
        .removeServiceFromInventory(_id, _etag)
        .then(() => {
          this.buttonClicked = false;
          this.getData();
        })
        .catch(() => {
          this.buttonClicked = false;
        });
    }

    instantiateToInventory({ _id, _etag }) {
      this.buttonClicked = true;
      this.inventoryService
        .instantiateService(_id, _etag)
        .then(() => {
          this.buttonClicked = false;
          this.getData();
        })
        .catch(() => {
          this.buttonClicked = false;
        });
    }

    stopInstance({ _id, _etag }) {
      this.buttonClicked = true;
      this.inventoryService
        .terminateService(_id, _etag)
        .then(() => {
          this.buttonClicked = false;
          this.getData();
        })
        .catch(() => {
          this.buttonClicked = false;
        });
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

    prettyYAML(obj) {
      return JSON.stringify(this.yaml.parse(obj), null, 4);
    }
  },
};

export const inventoryState = {
  parent: 'home',
  name: 'nsinventory',
  url: '/inventory',
  component: 'inventoryView',
};
