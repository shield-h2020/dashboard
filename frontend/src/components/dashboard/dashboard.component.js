import moment from 'moment';
import template from './dashboard.html';
import * as d3 from 'd3';

const VIEW_STRING = {
	title: 'Threats Dashboard',
};

const DAY_TIME_AGR = {
	hour: '0',
	day: '1',
	week: '2',
	month: '3'
};

export const DashboardComponent = {
	template,
	bindings: {
		tenant: '<',
	},
	controller: class DashboardComponent {
		constructor($stateParams, $state, $scope, DashboardService, AuthService, TenantsService) {
			'ngInject';

			this.viewStrings = VIEW_STRING;
			this.dashboardService = DashboardService;
			this.authService = AuthService;
			this.tenantsService = TenantsService;
			this.scope = $scope;
		}

		$onInit() {
			this.scope.selected_period = '0';
			this.scope.isAdmin = this.authService.isUserPlatformAdmin();
			this.scope.user_tenant = this.authService.getTenant();
			this.attackType = null;
			this.attackIndex = -1;
			this.dayTimeAgr = false;
			this.customPeriodIndex = '3';
			this.showDatePicker = false;
			this.donutChartData;
			this.lineChartData;
			this.barChartData;
			this.customStart;
			this.customEnd;
			this.AvColors = ["#85AACD", "#7AC8A0", "#C4C26F", "#D39596", "#8FB996", "#D0EFB1", "#D2AB99", "#413C58"];
			this.GrayPieColor = "#D0D0D0";

			this.scope.$on('TM_NOTIF_BROADCAST', (event, data) => {
				this.scope.selected_tenant = data;
				this.refreshPage();
			});

			this.scope.onTenantChange = function (e) {
				this.$emit('TM_NOTIF_BROADCAST', e.selected_tenant);
			};

			if (this.scope.isAdmin) {
				this.tenantsService.getTenants()
					.then((data) => {
						//console.log(data);
						this.scope.tenants_list = [{ 'tenant_name': 'All tenants', 'tenant_id': -1 }, ...data];
						//this.scope.tenants_list = data;
						this.scope.selected_tenant = this.scope.tenants_list[0].tenant_id;
					});
			}

			this.setPeriod();

			this.setFilter = function (eData) {

				if (eData.key === 'sDate')
					this.customStart = eData.value;

				if (eData.key === 'eDate')
					this.customEnd = eData.value;

				if (this.scope.selected_period !== this.customPeriodIndex)
					return;

				this.scope.sdate = moment(this.customStart).format('YYYY-MM-DDTHH:mm:ss');
				this.scope.edate = moment(this.customEnd).format('YYYY-MM-DDTHH:mm:ss');

				this.showDatePicker = true;
				this.refreshPage();
			}
		}

		//* *********************************************************
		//* *************************REQUESTS************************
		//* *********************************************************

		getTotalAttacks() {
			this.dashboardService.getTotalAttacks(this.scope.start, this.scope.end, this.scope.tenant)
				.success((data) => {
					this.scope.total_attacks = 0;
					if (data.results[0].series) {
						for (let i = 0; i < data.results[0].series.length; i += 1) {
							this.scope.total_attacks += data.results[0].series[i].values[0][1];
						}
					}

					this.donutChartData = data.results[0].series;
					this.barChartData = data.results[0].series;

					this.scope.table_total_pages = parseInt(this.scope.total_attacks / 10);
					if (this.scope.total_attacks % 10 > 0) {
						this.scope.table_total_pages += 1;
					}
				})
				.catch((response) => {
					// TODO Tratar erro
					console.log(response.status);
				});
		}

		getTotalAttackByDay() {
			var duration = moment.duration(moment(this.scope.end).diff(this.scope.start));
			var inDays = duration.asDays();
			//console.log(inDays);
			var timeAgr;
			if (inDays <= 1) {

				timeAgr = 'time(1h)';
				this.dayTimeAgr = DAY_TIME_AGR.hour;
				//console.log("dia");
			}
			else {
				//console.log(inDays);
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
						this.scope.end = moment(this.scope.edate).endOf('month').format('YYYY-MM-DDTHH:mm:ss') + '.000Z';
						timeAgr = 'time(4w)';
						this.dayTimeAgr = DAY_TIME_AGR.month;
					}

				}

				//this.dayTimeAgr = true;
			}
			// TODO Verificar periodo selecionado
			this.dashboardService.getTotalAttacksByDay(this.scope.start, this.scope.end, timeAgr, this.scope.tenant, this.attackType)
				.success((data) => {

					// this.donutChartData = data.results[0].series;
					if (this.attackIndex == -1) {
						//Draw bar chart
						if (data.results[0].series) {
							this.lineChartData = data.results[0].series;
							this.barChartData = data.results[0].series;
						}
					}
					else {
						//Draw line chart
						this.lineChartData = data.results[0].series;
					}

				})
				.catch((response) => {
					// TODO Tratar erro
					console.log(response.status);
				});
		}

		getAttacks() {
			// TODO Verificar attack_type selecionado
			this.dashboardService.getAttack(this.scope.start, this.scope.end, this.scope.tenant, this.attackType, this.scope.table_page * 10)
				.success((data) => {
					this.scope.attacks = data;
				})
				.catch((response) => {
					// TODO Tratar erro
					console.log(response.status);
				});
		}

		//* *********************************************************
		//* *************************FILTERS*************************
		//* *********************************************************

		setPeriod() {
			switch (this.scope.selected_period) {
				case '0':
					this.scope.sdate = moment()
						.startOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');
					this.scope.edate = moment()
						.endOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');

					this.LastStartDate = this.scope.sdate;
					this.LastEndDate = this.scope.edate;
					this.showDatePicker = false;

					break;
				case '1':
					this.scope.sdate = moment()
						.subtract(1, 'd')
						.startOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');
					this.scope.edate = moment()
						.subtract(1, 'd')
						.endOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');

					this.LastStartDate = this.scope.sdate;
					this.LastEndDate = this.scope.edate;
					this.showDatePicker = false;

					break;
				case '2':
					this.scope.sdate = moment()
						.subtract(7, 'd')
						.startOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');
					this.scope.edate = moment()
						.endOf('day')
						.format('YYYY-MM-DDTHH:mm:ss');


					this.LastStartDate = this.scope.sdate;
					this.LastEndDate = this.scope.edate;
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

		refreshPage() {
			this.scope.table_page = 0;
			if (!this.scope.isAdmin) {
				this.scope.tenant = this.scope.user_tenant;
			}
			else {
				if (this.scope.selected_tenant !== -1) {
					this.scope.tenant = this.scope.selected_tenant;
				}
				else
					this.scope.tenant = null;
			}
			this.scope.start = `${this.scope.sdate}.000Z`;
			this.scope.end = `${this.scope.edate}.000Z`;

			this.getTotalAttacks();
			this.getTotalAttackByDay();
			this.getAttacks();
		}

		//* *********************************************************
		//* *************************TABLE***************************
		//* *********************************************************

		setPage(next) {
			if (next) {
				this.scope.table_page += 1;
			} else {
				this.scope.table_page -= 1;
			}
			this.getAttacks();
		}

	},
};

export const DashboardState = {
	parent: 'home',
	name: 'dashboard',
	url: '/dashboard',
	component: 'dashboardView',
};
