import moment from 'moment';
import template from './cesicat.html';
import * as d3 from 'd3';
import styles from './cesicat.scss';

const VIEW_STRING = {
  title: 'CERT Dashboard',
};

const TABLE_HEADERS = {
  attack: 'Type of Infection',
  status: 'Status',
  detection_timestamp: 'Issue detected',
  closure_timestamp: 'Issue closed',
};

const DAY_TIME_AGR = {
  hour: '0',
  day: '1',
  week: '2',
  month: '3',
};

export const CESICATComponent = {
  template,
  bindings: {
	   tenant: '<',
  },
  controller: class CESICATComponent {
    constructor($stateParams, $state, $scope, CESICATService) {
			'ngInject';

			this.viewStrings = VIEW_STRING;
			this.cesicatService = CESICATService;
			this.scope = $scope;
			this.isLoadingAttacks = false;
			this.styles = styles;
			this.headers = {
				...TABLE_HEADERS,
			}
		}



		$onInit() {
			this.scope.selected_period = '0';
			this.attackType = null;
			this.dayTimeAgr = false;
			this.customPeriodIndex = '3';
			this.showDatePicker = false;
			this.lineChartDataMalicious;
			this.doubleLineChartData;
			this.customStart;
			this.customEnd;
			this.pagination = {
        page: 1,
        limit: 12,
        totalItems: 10,
      };
			this.AvColors = ["#85AACD", "#7AC8A0", "#C4C26F", "#D39596", "#8FB996", "#D0EFB1", "#D2AB99", "#413C58"];

			this.setPeriod();

			this.setFilter = function (eData) {
				if (eData.key === 'startDate')
					this.customStart = eData.value;

				if (eData.key === 'endDate')
					this.customEnd = eData.value;

				if (this.scope.selected_period !== this.customPeriodIndex)
				 return;
		
				this.scope.startDate = moment(this.customStart).format('YYYY-MM-DDTHH:mm:ss');
				this.scope.endDate = moment(this.customEnd).format('YYYY-MM-DDTHH:mm:ss');

				this.showDatePicker = true;
				this.refreshPage();
			}
		}

		//* *********************************************************
		//* *************************REQUESTS************************
		//* *********************************************************
	
  getTotalAttackByDay() {
    const duration = moment.duration(moment(this.scope.end).diff(this.scope.start));
    const inDays = duration.asDays();
    let timeAgr;
    if (inDays <= 1) {
      timeAgr = 'time(1h)';
      this.dayTimeAgr = DAY_TIME_AGR.hour;
    }
		else {
			if (inDays <= 12) {

				timeAgr = 'time(1d)';
				this.dayTimeAgr = DAY_TIME_AGR.day;
			}
			else {

				if (inDays < 30) {

					timeAgr = 'time(1w)';
					this.dayTimeAgr = DAY_TIME_AGR.week;
				}
				else {
					this.scope.end = `${moment(this.scope.edate).endOf('month').format('YYYY-MM-DDTHH:mm:ss')}.000Z`;
					timeAgr = 'time(4w)';
					this.dayTimeAgr = DAY_TIME_AGR.month;
				}
			}
	  }
    this.maliciousDevices = { 
			statement_id: 0,
			series: [
				{ 
					name: 'malicious',
					columns: ['time', 'count'],
					values: [],
			  },
			],
		};
    this.networkDevices = null;
    this.filter = { 
			timestamp: { 
				$gte: moment(this.scope.start).unix(), 
				$lte: moment(this.scope.end).unix() 
			} 
		};

		setTimeout(() => {
		this.cesicatService.getStatics(this.filter).then((data) => {
			this.networkDevices = [];
      data._items.forEach((element) => {
        this.maliciousDevices.series[0].values.push([
					`${moment.unix(element.timestamp).format('YYYY-MM-DDTHH:mm:ss')}Z`,
					element.cumulative
				]);
				this.networkDevices.push({
					date: `${moment.unix(element.timestamp).format('YYYY-MM-DDTHH:mm:ss')}Z`,
					active: element.active,
					blocked: element.blocked,
				});

			});
    }).finally(() => {
			this.lineChartDataMalicious = this.maliciousDevices.series;
			this.doublelineChartData = this.networkDevices;
		});
		}, 500);

  }

//* *********************************************************
//* *************************FILTERS*************************
//* *********************************************************

  setPeriod() {
			switch (this.scope.selected_period) {
				case '0':
					 this.scope.startDate = moment()
						.startOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');
					 this.scope.endDate = moment()
						.endOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');
					 this.LastStartDate = this.scope.startDate;
					 this.LastEndDate = this.scope.endDate;
					 this.showDatePicker = false;
					 break;
				case '1':
					this.scope.startDate = moment()
						.subtract(1, 'd')
						.startOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');
					this.scope.endDate = moment()
						.subtract(1, 'd')
						.endOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');

					this.LastStartDate = this.scope.startDate;
					this.LastEndDate = this.scope.endDate;
					this.showDatePicker = false;

					break;
				case '2':
					this.scope.startDate = moment()
						.subtract(7, 'd')
						.startOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');
					this.scope.endDate = moment()
						.endOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');


					this.LastStartDate = this.scope.startDate;
					this.LastEndDate = this.scope.endDate;
					this.showDatePicker = false;

					break;
				case '3':
					this.setFilter({ key: '', value: '' });
					return;
				default:
					break;
			}
			
			this.refreshPage();
	}
	
	// TABLE

	getAttacks() {
		this.isLoadingAttacks = true;
		this.attacksList = [];
		this.filters = {
			detection_timestamp: {
				$gte: moment(this.scope.start).unix(),
				$lte: moment(this.scope.end).unix(),
			} 
		};

		this.cesicatService.getAttackRegistry(this.filters)
			.then((data) => {
				data._items.map((item) =>
					this.attacksList.push({
					attack: item.attack,
					status: item.status,
					detection_timestamp: moment.unix(item.detection_timestamp).format('YYYY-MM-DD HH:mm:ss'),
					closure_timestamp: moment.unix(item.closure_timestamp).format('YYYY-MM-DD HH:mm:ss') === 'Invalid date' ? '--'
					: moment.unix(item.closure_timestamp).format('YYYY-MM-DD HH:mm:ss'),
				})
			)
				this.pagination.totalItems = data ? data._meta.total : 0;
				this.isLoadingAttacks = false;
			});
	}

	// Change Page
	changePage(amount) {
		const { page, totalItems, limit } = this.pagination;
		const numberOfPages = Math.ceil(totalItems / limit);
		const condition = amount > 0 ?
		 page + 1 <= numberOfPages : this.paginationNS.page > 1;
		if (condition) {
			this.paginationNS.page += amount;
			this.getData();
		}
	}

	calcPageItems() {
		const { page, totalItems, limit } = this.pagination;

		const numberOfPages = Math.ceil(totalItems / limit);
		return { page, totalPage: numberOfPages, total: totalItems };
	}

    refreshPage() {
			this.scope.start = `${this.scope.startDate}`;
			this.scope.end = `${this.scope.endDate}`;
			this.getTotalAttackByDay();
			this.getAttacks();
    }
 },
};

export const CESICATState = {
  parent: 'home',
  name: 'cert',
  url: '/cert',
  component: 'cesicatView',
};
