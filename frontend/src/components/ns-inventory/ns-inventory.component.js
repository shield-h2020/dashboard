import template from './ns-inventory.html';
import styles from './ns-inventory.scss';

const VIEW_STRINGS = {
	title: 'NS inventory',
	tableTitle: 'Inventory',
	modalTitle: 'NS Details',
	close: 'Close',
};

const TABLE_HEADERS = {
	capabilities: 'Capabilities',
	_created: 'Created',
	status: 'Status',
	actions: 'Actions'
};

const MODAL_ENTRIES = {
	_id: 'Id',
	capabilities: 'Capabilities',
	_created: 'Created',
};

export const InventoryComponent = {
	template,
	controller: class InventoryComponent {
		constructor(InventoryService) {
			'ngInject';

			this.viewStrings = VIEW_STRINGS;
			this.modalEntries = MODAL_ENTRIES;
			this.styles = styles;
			this.inventoryService = InventoryService;
			this.createOpen = false;
			this.deleteOpen = false;
			this.actionsItemAvailable = [
				{
					label: 'view',
					action: this.toggleNSDetails.bind(this)
				},
				{
					label: 'withdraw',
					action: this.removeFromInventory.bind(this)
				},
				{
					label: 'instantiate',
					action: this.instantiateToInventory.bind(this)
				}
			];
			this.actionsItemRunning = [
				{
					label: 'view',
					action: this.toggleNSDetails.bind(this)
				},
				{
					label: 'stop',
					action: this.stopInstance.bind(this)
				}
			]

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
			this.getData();
		}

		getData() {
			this.isLoading = true;
			this.inventoryService.getInventoryServices({
				page: this.offset,
				limit: this.limit,
			}, this.filters)
				.then((items) => {
					this.items = items.filter(it => it).map(item => {
						var selectedActions = [];
						// item.status = "running";
						if (item.status == 'available') {
							selectedActions = this.actionsItemAvailable
						}
						else {
							selectedActions = this.actionsItemRunning
						}

						return {
							...item,
							capabilities: item.manifest['manifest:ns'].properties.capabilities.join(', '),
							headerActions: selectedActions
						}
					});
				})
				.finally(() => { this.isLoading = false; });
		}

		toggleNSDetails(ns) {
			this.ns = ns;
			this.modalOpen = !this.modalOpen;
		}

		removeFromInventory({ _id, _etag }) {
			this.inventoryService.removeServiceFromInventory(_id, _etag);
			this.getData();
		}

		instantiateToInventory({ _id, _etag }) {
			this.inventoryService.instantiateService(_id, _etag);
			this.getData();
		}

		stopInstance({ _id, _etag }) {
			this.inventoryService.terminateService(_id, _etag);
			this.getData();
		}
	},
};

export const inventoryState = {
	parent: 'home',
	name: 'nsinventory',
	url: '/inventory',
	component: 'inventoryView',
};
