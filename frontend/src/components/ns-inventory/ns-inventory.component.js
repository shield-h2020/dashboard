import template from "./ns-inventory.html";
import styles from "./ns-inventory.scss";
import * as YAML from "yamljs";

const VIEW_STRINGS = {
  title: "NS inventory",
  tableTitle: "Inventory",
  modalTitle: "NS Details",
  close: "Close"
};

const TABLE_HEADERS = {
  capabilities: "Capabilities",
  _created: "Created",
  status: "Status",
  actions: "Actions"
};

const MODAL_ENTRIES = {
  _id: "Id",
  capabilities: "Capabilities",
  _created: "Created",
  type: "Type",
  target: "Target"
};

export const InventoryComponent = {
  template,
  controller: class InventoryComponent {
    constructor($scope, InventoryService, AuthService, toastr) {
      "ngInject";

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
      this.actionsItemAvailable = [
        {
          label: "view",
          action: this.toggleNSDetails.bind(this)
        },
        {
          label: "withdraw",
          action: this.removeFromInventory.bind(this)
        },
        {
          label: "instantiate",
          action: this.instantiateToInventory.bind(this)
        }
      ];
      this.actionsItemRunning = [
        {
          label: "view",
          action: this.toggleNSDetails.bind(this)
        },
        {
          label: "terminate",
          action: this.stopInstance.bind(this)
        }
      ];

      this.offset = 0;
      this.limit = 25;
      this.isLoading = false;
      this.filters = {};
      this.headers = {
        ...TABLE_HEADERS
      };
      this.modalOpen = false;
    }

    $onInit() {
      this.initNsinventorySocket();

      this.scope.$on("NSINVENTORY_UPDATE_DATA", (event, data) => {
        this.getData();
      });

      this.getData();
    }

    initNsinventorySocket() {
      var nsinventorySocket = this.inventoryService.connecNSInventorySocket(
        this.authService.getTenant()
      );
      nsinventorySocket.onmessage = message => {
        const data = JSON.parse(message.data);
        if (data.result == "success") {
          this.toast.info(data.ns_name + " is up and running", {
            onShown: () => {
              this.scope.$broadcast("NSINVENTORY_UPDATE_DATA");
            },
            closeButton: true
          });
        } else {
          this.toast.error(data.ns_name + ": failed to instantiate", {
            closeButton: true
          });
        }
      };
    }

    getData() {
      this.isLoading = true;
      this.inventoryService
        .getInventoryServices(
          {
            page: this.offset,
            limit: this.limit
          },
          this.filters
        )
        .then(items => {
          console.log(items);
          this.items = items.filter(it => it).map(item => {
            var selectedActions = [];
            // item.status = "running";
            if (item.status == "available") {
              selectedActions = this.actionsItemAvailable;
            } else {
              selectedActions = this.actionsItemRunning;
            }

            return {
              ...item,
              capabilities: item.manifest[
                "manifest:ns"
              ].properties.capabilities.join(", "),
              headerActions: selectedActions
            };
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    }

    toggleNSDetails(ns) {
      if (ns) {
        this.ns = {
          ...ns,
          type: ns.manifest["manifest:ns"].type,
          target: ns.manifest["manifest:ns"].target
        };
        // debugger;
      }
      this.modalOpen = !this.modalOpen;
    }

    removeFromInventory({ _id, _etag }) {
      this.inventoryService
        .removeServiceFromInventory(_id, _etag)
        .then(() => this.getData());
    }

    instantiateToInventory({ _id, _etag }) {
      this.inventoryService
        .instantiateService(_id, _etag)
        .then(() => this.getData());
    }

    stopInstance({ _id, _etag }) {
      this.inventoryService
        .terminateService(_id, _etag)
        .then(() => this.getData());
    }

    prettyYAML(obj) {
      return JSON.stringify(this.yaml.parse(obj), null, 4);
    }
  }
};

export const inventoryState = {
  parent: "home",
  name: "nsinventory",
  url: "/inventory",
  component: "inventoryView"
};
