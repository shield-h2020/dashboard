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
  _created: "Instantiated",
  status: "Status",
  actions: "Actions"
};

const MODAL_ENTRIES = {
  _id: "Id",
  capabilities: "Capabilities",
  _created: "Instantiated",
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

      this.actionsItemConfiguring = [
        {
          label: "view",
          action: this.toggleNSDetails.bind(this)
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
      this.buttonClicked = false;
      this.nsSocketAtmp = 0;
    }

    $onInit() {
      this.initNsinventorySocket();

      this.scope.$on("NSINVENTORY_UPDATE_DATA", (event, data) => {
        this.getData();
      });

      this.getData();
    }

    initNsinventorySocket() {
      var nsinventorySocket = this.inventoryService.connectNSInventorySocket(
        this.authService.getTenant()
      );
      nsinventorySocket.onopen = e => {
        this.nsSocketAtmp = 0;
      };
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
            onShown: () => {
              this.scope.$broadcast("NSINVENTORY_UPDATE_DATA");
            },
            closeButton: true
          });
        }
      };
      nsinventorySocket.onclose = e => {
        if (this.nsSocketAtmp < 3) {
          this.nsSocketAtmp++;
          setTimeout(this.initNsinventorySocket(), 1000);
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
            } else if (item.status == "running") {
              selectedActions = this.actionsItemRunning;
            } else {
              selectedActions = this.actionsItemConfiguring;
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
