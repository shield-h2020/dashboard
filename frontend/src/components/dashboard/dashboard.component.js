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
      this.customStart;
      this.customEnd;
      this.AvColors = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
      this.GrayPieColor = "#D0D0D0";
      //var _this = this;
      this.scope.$on('TM_NOTIF_BROADCAST', (event, data) => {
        this.scope.selected_tenant = data;
        this.refreshPage();
      });
      this.scope.onTenantChange = function(e) {
        //console.log(e);
        this.$emit('TM_NOTIF_BROADCAST', e.selected_tenant);
      };
      if (this.scope.isAdmin) {
        this.tenantsService.getTenants()
          .then((data) => {
            //console.log(data);
            this.scope.tenants_list = [{'tenant_name': 'All tenants', 'tenant_id': -1}, ...data];
            //this.scope.tenants_list = data;
            this.scope.selected_tenant = this.scope.tenants_list[0].tenant_id;
          });
      }
      
      /* When uncommenting this, watch out with the refreshPage routine
      that was running multiple times because in the function set period
      we're setting the first and last date (that will trigger this wathers)*/
    

      this.setPeriod();

      this.setFilter = function(eData) {

        //console.log(eData.key)

        if(eData.key === 'sDate')
          this.customStart = eData.value;

        if(eData.key === 'eDate')
          this.customEnd = eData.value;
        
        //console.log(this.scope.selected_period);
        //console.log(this.customPeriodIndex);

        if(this.scope.selected_period !== this.customPeriodIndex)
          return;

        this.scope.sdate = moment(this.customStart).format('YYYY-MM-DDTHH:mm:ss');
        this.scope.edate = moment(this.customEnd).format('YYYY-MM-DDTHH:mm:ss');
        
        //console.log(this.scope.sdate);
        //console.log(this.scope.edate);

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
      var duration = moment.duration(moment(this.scope.end).diff(this.scope.start));
      var inDays = duration.asDays();
      //console.log(inDays);
      var timeAgr;
      if(inDays <= 1) {
        
        timeAgr = 'time(1h)';
        this.dayTimeAgr = DAY_TIME_AGR.hour;
        //console.log("dia");
      }
      else {
        //console.log(inDays);
        if(inDays <= 12) {

          timeAgr = 'time(1d)';
          this.dayTimeAgr = DAY_TIME_AGR.day;
        }
        else {

          if(inDays < 30) {

            timeAgr = 'time(1w)';
            this.dayTimeAgr = DAY_TIME_AGR.week;
          }
          else {
            this.scope.end = moment(this.scope.edate).endOf('month').format('YYYY-MM-DDTHH:mm:ss') + '.000Z';
            //console.log(this.scope.end);
            timeAgr = 'time(4w)';
            this.dayTimeAgr = DAY_TIME_AGR.month;
          }

        }
        
        //this.dayTimeAgr = true;
      }
      // TODO Verificar periodo selecionado
      this.dashboardService.getTotalAttacksByDay(this.scope.start, this.scope.end, timeAgr, this.scope.tenant, this.attackType)
        .success((data) => {
          if (data.results[0].series) {
            this.drawBar(data.results[0].series);
          }
          else
            this.drawBar();
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
          this.showDatePicker =  false;

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
          this.showDatePicker =  false;      

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
          this.showDatePicker =  false;
          
          break;
        case '3':
          this.setFilter({key: '', value: ''});
          return;
        /*case '3':
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
          break;*/
        default:
          break;
      }
      console.log("Refreshing page");
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

      //console.log(this.scope.start);

      this.getTotalAttacks();
      this.getTotalAttackByDay();
      this.getAttacks();
    }

    

    //* *********************************************************
    //* ************************GRAPHS***************************
    //* *********************************************************

    drawDonut(data) {
      document.getElementById('chart_attacks').innerHTML = '';
      
      if(!data)
        return;
      
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
      var color;
      var nrSeries = data.length;
      //console.log("Number of series");
      //console.log(nrSeries);
      if(this.attackIndex === -1)
        color = d3.scale.ordinal().range(this.AvColors);
      else {
        var grayedColors = [];
        for (let j = 0; j < nrSeries; j += 1) {
          if(j !== this.attackIndex)
            grayedColors[j] = this.GrayPieColor;
          else
            grayedColors[j] = this.AvColors[j];
        }
        color = d3.scale.ordinal().range(grayedColors);
      }
      //console.log(color[0]);
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


      const restOfTheData = function (me) {
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
              return `translate(${(i * legendHeight) - (43*nrSeries)},150)`;
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
            'font-size': '10px'
          })
          .on("click", (d, i) => {
            
            if(me.attackIndex === i) {

              //console.log("Resetting value");
              me.attackIndex = -1;
              me.attackType = null;

              me.getTotalAttacks();
              me.getAttacks();
              me.getTotalAttackByDay();
            }
            else {

              //console.log("New value found" + i);
              var selectedAttack = d.substring(0, d.indexOf("-") - 1);
              me.attackIndex = i;
              me.attackType = selectedAttack;
              
              me.getTotalAttacks();
              me.getAttacks();
              me.getTotalAttackByDay();
            }
          })
          .on("mouseover", function(d) {
            d3.select(this).style("cursor", "pointer"); 
          })
          .on("mouseout", function(d) {
            d3.select(this).style("cursor", "default"); 
          });
      };
      setTimeout(restOfTheData(this), 1000);
    }

    drawBar(data2) {
      ////////////////////////////////////////////////////////
      // Configs
      const Chart = {
        margin: { left: 30, top: 20, right: 20, bottom: 20 },
        width: 450,
        height: 450,
        sideWidth: 10,
        bottomHeight: 60,
      };
      const BarArea = {
        width: Chart.width - Chart.margin.left - Chart.margin.right - Chart.sideWidth,
        height: Chart.height - Chart.margin.top - Chart.margin.bottom - Chart.bottomHeight,
      };
      ////////////////////////////////////////////////////////
      document.getElementById('chart_ocurrences').innerHTML = '';
      if(!data2)
        return;
      var n = data2[0].values.length, // number of samples
      m = data2.length; // number of series

      //console.log("Real values");
      //console.log(data2);

      var data = [];
      var maxValue = 0;
      for (let i = 0; i < data2.length; i += 1) {
        
        //console.log("First level");
        //console.log(data2[i].values);
        var innerData = [];
        for (let j = 0; j < data2[i].values.length; j += 1) {
          //console.log("Snd level");
          //console.log(data2[i].values[j]);
          //innerData[j][0] = data2[i].values[j][0];  
          //innerData[j][1] = data2[i].values[j][1];
          innerData[j] = data2[i].values[j][1];
          if(innerData[j] > maxValue)
            maxValue = innerData[j];
        }
        data[i] = innerData;
      }
      //console.log("Proccessed value");
      //console.log(data);

      var xAxisData = [];
      for (let i = 0; i < data2[0].values.length; i += 1) {
        
        if(this.dayTimeAgr === DAY_TIME_AGR.hour) {
          xAxisData[i] = moment(data2[0].values[i][0]).format('HH');
          //console.log(data2[0].values[i][0]);
        }
        if(this.dayTimeAgr === DAY_TIME_AGR.day) {
          xAxisData[i] = moment(data2[0].values[i][0]).format('DD-MM');
          //console.log(xAxisData[i]);
        }
        if(this.dayTimeAgr === DAY_TIME_AGR.week) {
          xAxisData[i] = moment(data2[0].values[i][0]).format('DD-MM');
          //console.log(xAxisData[i]);
        }
        if(this.dayTimeAgr === DAY_TIME_AGR.month) {
          xAxisData[i] = moment(data2[0].values[i][0]).format('MMMM').substring(0,3);
          //console.log(xAxisData[i]);
        }
      }
      //console.log("xAxisData");
      //console.log(xAxisData);
      
      /*var margin = {top: 20, right: 30, bottom: 30, left: 40},
          width = 960 - margin.left - margin.right,
          height = Chart.height - margin.top - margin.bottom;*/

      var y = d3.scale.linear()
          .domain([0, maxValue], 1)
          .range([0, BarArea.height]);
      
      var x0 = d3.scale.ordinal()
          .domain(d3.range(n))
          .rangeBands([0, BarArea.width], 0.1);
      
      var x1 = d3.scale.ordinal()
          .domain(d3.range(m))
          .rangeBands([0, x0.rangeBand()], 0.1);
      
      var color;
      if(this.attackIndex === -1)
        color = d3.scale.ordinal().range(this.AvColors);
      else
        color = d3.scale.ordinal().range([this.AvColors[this.attackIndex]]);

      var xScale = d3.scale.ordinal()
          .domain(xAxisData)
          .rangeBands([0, BarArea.width]);
      
      var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient("bottom");
      
      var yScale = d3.scale.linear()
          .domain([0, maxValue])
          .range([BarArea.height, 0]);

      var yAxis = d3.svg.axis()
          .scale(yScale)
          .orient("left")
          .ticks( Math.min(10, maxValue ));
      var svg = d3.select('#chart_ocurrences').attr({
        width: Chart.width,
        height: Chart.height,
      });
      
      svg.append("svg")
        //.attr("width", width + margin.left + margin.right)
        //.attr("height", height + margin.top + margin.bottom)
        .append("svg:g")
        .attr("transform", "translate(" + Chart.margin.left + "," + Chart.margin.top + ")");

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + BarArea.height + ")")
          .call(xAxis);

      svg.append("g").selectAll("g")
          .data(data)
        .enter().append("g")
          .style("fill", function(d, i) { return color(i); })
          .attr("transform", function(d, i) { return "translate(" + x1(i) + ",0)"; })
        .selectAll("rect")
          .data(function(d) { return d; })
        .enter().append("rect")
          .attr("width", x1.rangeBand())
          .attr("height", y)
          .attr("x", function(d, i) { return x0(i); })
          .attr("y", function(d) { return BarArea.height - 1 - y(d); })
          .attr("stroke", "black")
          .attr("stroke-opacity", "0.2");
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
