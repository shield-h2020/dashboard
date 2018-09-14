import moment from 'moment';
import template from './dashboard.html';


const VIEW_STRING = {
  title: 'Incidents DashBoard',
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
      this.scope.selected_period = '2';
      this.scope.isAdmin = this.authService.isUserPlatformAdmin();
      this.scope.user_tenant = this.authService.getTenant();

      if (this.scope.isAdmin) {
        this.tenantsService.getTenants()
          .then((data) => {
            this.scope.tenants_list = data;
          });
      }

      this.scope.$watch('start_date', () => {
        this.scope.end_min_date = moment(this.scope.start_date)
          .format('YYYY-MM-DDTHH:mm:ss');
        this.scope.sdate = this.scope.end_min_date;
        this.refreshPage();
      });

      this.scope.$watch('end_date', () => {
        this.scope.start_max_date = moment(this.scope.end_date)
          .format('YYYY-MM-DDTHH:mm:ss');
        this.scope.edate = this.scope.start_max_date;
        this.refreshPage();
      });

      this.setPeriod();
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

          this.drawDonut(data.results[0].series);

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
      // TODO Verificar periodo selecionado
      this.dashboardService.getTotalAttacksByDay(this.scope.start, this.scope.end, 'time(1d)', this.scope.tenant)
        .success((data) => {
          if (data.results[0].series) {
            this.drawBar(data.results[0].series[0].values);
          } else {
            this.drawBar(null);
          }
        })
        .catch((response) => {
          // TODO Tratar erro
          console.log(response.status);
        });
    }

    getAttacks() {
      // TODO Verificar attack_type selecionado
      this.dashboardService.getAttack(this.scope.start, this.scope.end, this.scope.tenant, '', this.scope.table_page * 10)
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
          break;
        case '1':
          this.scope.sdate = moment()
            .subtract(1, 'd')
            .startOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          this.scope.edate = moment()
            .endOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          break;
        case '2':
          this.scope.sdate = moment()
            .subtract(7, 'd')
            .startOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          this.scope.edate = moment()
            .endOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          break;
        case '3':
          this.scope.sdate = moment()
            .startOf('month')
            .format('YYYY-MM-DDTHH:mm:ss');
          this.scope.edate = moment()
            .endOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          break;
        case '4':
          this.scope.sdate = moment()
            .subtract(170, 'd')
            .startOf('month')
            .format('YYYY-MM-DDTHH:mm:ss');
          this.scope.edate = moment()
            .endOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          break;
        case '5':
          this.scope.sdate = moment()
            .startOf('year')
            .format('YYYY-MM-DDTHH:mm:ss');
          this.scope.edate = moment()
            .endOf('day')
            .format('YYYY-MM-DDTHH:mm:ss');
          break;
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

      this.scope.start = `${this.scope.sdate}.000Z`;
      this.scope.end = `${this.scope.edate}.000Z`;

      if (this.scope.selected_tenant) {
        this.scope.tenant = this.scope.selected_tenant;
      }

      this.getTotalAttacks();
      this.getTotalAttackByDay();
      this.getAttacks();
    }

    //* *********************************************************
    //* ************************GRAPHS***************************
    //* *********************************************************

    drawDonut(data) {
      document.getElementById('chart_attacks').innerHTML = '';
      const dataset = [];
      if (data) {
        for (let i = 0; i < data.length; i += 1) {
          dataset.push({
            name: data[i].tags.attack_type,
            value: data[i].values[0][1],
          });
        }
      }
      const pie = d3.layout.pie()
        .value(d => d.value)
        .sort(null)
        .padAngle(0.03);

      const w = 400;
      const h = 350;

      const outerRadius = 120;
      const innerRadius = 100;

      const color = d3.scale.category10();

      const arc = d3.svg.arc()
        .outerRadius(outerRadius)
        .innerRadius(innerRadius);

      const svg = d3.select('#chart_attacks')
        .append('svg')
        .attr({
          width: w,
          height: h,
        })
        .append('g')
        .attr({
          transform: `translate(${w / 2},${h / 2})`,
        });
      const path = svg.selectAll('path')
        .data(pie(dataset))
        .enter()
        .append('path')
        .attr({
          d: arc,
          fill(d, i) {
            return color(`${d.data.name} - ${d.data.value}`);
          },
        });

      path.transition()
        .duration(1000)
        .attrTween('d', (d) => {
          const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
          return function (t) {
            return arc(interpolate(t));
          };
        });


      const restOfTheData = function () {
        const legendRectSize = 20;
        const legendHeight = 100;

        const legend = svg.selectAll('.legend')
          .data(color.domain())
          .enter()
          .append('g')
          .attr({
            class: 'legend',
            transform(d, i) {
              // Just a calculation for x & y position
              return `translate(${(i * legendHeight) - 190},150)`;
            },
          });
        legend.append('rect')
          .attr({
            width: legendRectSize,
            height: legendRectSize,
            rx: 20,
            ry: 20,
          })
          .style({
            fill: color,
            stroke: color,
          });

        legend.append('text')
          .attr({
            x: 30,
            y: 15,
          })
          .text(d => d)
          .style({
            fill: '#929DAF',
            'font-size': '14px',
          });
      };
      setTimeout(restOfTheData, 1000);
    }

    drawBar(values) {
      document.getElementById('chart_ocurrences').innerHTML = '';

      const dataset = [];
      if (values) {
        for (let i = 0; i < values.length; i += 1) {
          dataset.push([
            values[i][0].substring(0, 10),
            values[i][1],
          ]);
        }
      }

      // Configs
      const Chart = {
        margin: { left: 20, top: 20, right: 20, bottom: 20 },
        width: 450,
        height: 400,
        sideWidth: 10,
        bottomHeight: 60,
      };
      const BarArea = {
        width: Chart.width - Chart.margin.left - Chart.margin.right - Chart.sideWidth,
        height: Chart.height - Chart.margin.top - Chart.margin.bottom - Chart.bottomHeight,
      };
      const Bar = {
        padding: 0.01,
        outerPadding: 0.02,
        color: '#85AACD',
        startColor: '#85AACD',
      };

      let dataTrigger = false;

      // Setup
      let data;
      const svg = d3.select('#chart_ocurrences')
        .attr({
          width: Chart.width,
          height: Chart.height,
        });
      let bars;

      svg.append('clippath')
        .attr('id', 'chart-area')
        .append('rect')
        .attr({
          x: Chart.margin.left + Chart.sideWidth,
          y: Chart.margin.top,
          width: BarArea.width,
          height: BarArea.height,
        });

      const barGroup = svg.append('g')
        .attr('id', 'bars')
        .attr('clip-path', 'url(#chart-area)')
        .attr('transform',
          `translate(${Chart.margin.left + Chart.sideWidth}, ${Chart.margin.top})`)
        .attr('clip-path', 'url(#chart-area)');

      svg.append('g')
        .attr('transform', `translate(${
        Chart.margin.left + Chart.sideWidth}, ${
        Chart.margin.top + BarArea.height})`)
        .classed('axis', true)
        .classed('x', true)
        .classed('nostroke', true);

      svg.append('g')
        .attr('transform',
          `translate(${Chart.margin.left + Chart.sideWidth}, ${Chart.margin.top})`)
        .classed('axis', true)
        .classed('y', true);

      svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', (0 - Chart.margin.left))
        .attr('x', 0 - (Chart.height / 2))
        .attr('dy', '1em')
        .attr('class', 'dashboard_datepicker_text')
        .style('text-anchor', 'middle')
        .text('Number of ocurrences');

      // Manipulators
      window.changeData = () => {
        dataTrigger = !dataTrigger;
        // const dataset = dataTrigger ? dataset;
        data = JSON.parse(JSON.stringify(dataset));
        renderChart();
      };

      let newIndex = 0;
      window.appendData = () => {
        const len = 10;
        for (let i = 0; i < len; i += 1) {
          const record = [`new${++newIndex}`, Math.ceil(Math.random() * 100)];
          data.push(record);
        }
        renderChart();
      };

      window.removeData = (d) => {
        const idx = data.indexOf(d);
        if (idx > -1) {
          data.splice(idx, 1);
        }
        renderChart();
      };

      window.sortData = () => {
        data.sort((a, b) => d3.ascending(a[1], b[1]));
        renderChart();
      };

      // Rendering
      data = JSON.parse(JSON.stringify(dataset));
      renderChart();
      setTimeout(window.changeData, 1200);


      function renderChart() {
        const xScale = d3.scale
          .ordinal()
          .rangeRoundBands([0, BarArea.width], Bar.padding, Bar.outerPadding)
          .domain(data.map((v, i) => v[0]));

        const yScale = d3.scale.linear()
          .range([BarArea.height, 0])
          .domain([0, d3.max(data, d => d[1])]);

        const xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('bottom');

        const yAxis = d3.svg.axis()
          .ticks(5)
          .scale(yScale)
          .orient('left');

        const totalDelay = 500;
        const oneByOne = (d, i) => totalDelay * i / data.length;

        bars = barGroup.selectAll('rect')
          .data(data, d => d[0]);

        bars.enter()
          .append('rect')
          .attr({
            x: d => xScale(d[0]),
            y: BarArea.height,
            width: xScale.rangeBand(),
            height: 0,
            fill: Bar.startColor,
          });

        bars.transition()
          .duration(1500)
          .delay(oneByOne)
          .ease('elastic')
          .attr({
            x: d => xScale(d[0]),
            y: d => yScale(d[1]),
            width: xScale.rangeBand(),
            height: d => BarArea.height - yScale(d[1]),
            fill: Bar.color,
          });

        bars.exit()
          .transition()
          .duration(500)
          .attr({
            y: BarArea.height,
            height: 0,
            color: Bar.startColor,
          })
          .remove();

        let labels = barGroup.selectAll('text');
        if (xScale.rangeBand() > 25) {
          labels = labels.data(data, d => d[0]);
        } else {
          labels = labels.data([]);
        }

        labels.enter()
          .append('text')
          .classed('label', true)
          .classed('noselect', true)
          .classed('unclickable', true)
          .attr('fill', 'white');

        const belowOrAbove = (d) => {
          const y = yScale(d[1]);
          if (y + 30 < BarArea.height) {
            return [y + 20, 'white'];
          }
          return [y - 10, 'black'];
        };

        labels.transition()
          .duration(1500)
          .delay(oneByOne)
          .ease('elastic')
          .attr({
            x: d => xScale(d[0]) + xScale.rangeBand() / 2,
            y: d => belowOrAbove(d)[0],
            fill: d => belowOrAbove(d)[1],
          })
          .text(d => d[1]);

        labels.exit()
          .remove();

        // TODO: how to calculate this 20
        if (xScale.rangeBand() > 20) {
          d3.select('.x.axis')
            .transition()
            .duration(1500)
            .ease('elastic')
            .call(xAxis)
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('transform', 'rotate(-20)');
        } else {
          d3.select('.x.axis')
            .selectAll('.tick')
            .remove();
        }

        d3.select('.y.axis')
          .transition()
          .duration(1000)
          .call(yAxis);
      }
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
