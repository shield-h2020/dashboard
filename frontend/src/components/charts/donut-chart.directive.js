import * as d3 from 'd3';

export const DonutChartDirective = ($compile, $timeout) => ({
  restrict: 'A',
  link(scope, element) {
    scope.$watch('$ctrl.donutChartData', function () {
      document.getElementById('chart_attacks').innerHTML = '';

      let data = scope.$ctrl.donutChartData;
      
      if (!data)
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

      if (scope.$ctrl.attackIndex === -1)
        color = d3.scale.ordinal().range(scope.$ctrl.AvColors);
      else {
        var grayedColors = [];
        for (let j = 0; j < nrSeries; j += 1) {
          if (j !== scope.$ctrl.attackIndex)
            grayedColors[j] = scope.$ctrl.GrayPieColor;
          else
            grayedColors[j] = scope.$ctrl.AvColors[j];
        }
        color = d3.scale.ordinal().range(grayedColors);
      }

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
              return `translate(${(i * legendHeight) - (43 * nrSeries)},150)`;
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

            if (me.attackIndex === i) {

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
          .on("mouseover", function (d) {
            d3.select(this).style("cursor", "pointer");
          })
          .on("mouseout", function (d) {
            d3.select(this).style("cursor", "default");
          });
      };
      setTimeout(restOfTheData(scope.$ctrl), 1000);
    });
  },
  bindToController: true
});

export default DonutChartDirective;
