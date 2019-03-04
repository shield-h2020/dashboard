import * as d3 from 'd3';
import moment from 'moment';

const DAY_TIME_AGR = {
    hour: '0',
    day: '1',
    week: '2',
    month: '3'
};

export const DoubleLinesChartDirective = ($compile, $timeout) => ({
    restrict: 'A',
    link(scope, element) {
      scope.$watch('$ctrl.doublelineChartData', () => {
        document.getElementById('chart_double_line').innerHTML = '';
        if(!scope.$ctrl.doublelineChartData)
            return;

        let dataLineChart = scope.$ctrl.doublelineChartData;

        if (!dataLineChart || dataLineChart.length === 0)
          return;

        // Set the dimensions of the canvas / graph
        const margin = { top: 30, right: 20, bottom: 40, left: 50 };
        const width = 700 - margin.left - margin.right;
        const height = 464 - margin.top - margin.bottom;

        // Adds the svg canvas
        const svg = d3.select('#chart_double_line').append('svg')
        .attr('viewBox', `0, 0,${width + margin.left + margin.right},${height + margin.top + margin.bottom}`)
        .attr('width', '100%')
        .attr('height', '54vh')
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

        let xTimeFormat;
        const xAxisLabel = 'Time';

        const formatDate = d3.time.format('%Y-%m-%dT%H:%M:%SZ').parse;

        if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.hour) {
          xTimeFormat = '%H:%M';
        }
        if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.day) {
          xTimeFormat = '%e-%b';
        }
        if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.week) {
          xTimeFormat = '%e-%b';
        }
        if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.month) {
          xTimeFormat = '%b';
        }
        const color = d3.scale.category10();

        // Set the ranges
        const x = d3.time.scale().range([0, width]);

        const y = d3.scale.linear().range([height - margin.bottom, 0]);

        const xAxis = d3.svg.axis().scale(x)
        .orient('bottom')
        .tickFormat(d3.time.format(xTimeFormat));

        const yAxis = d3.svg.axis().scale(y)
        .orient('left').ticks(5);

        const	valueline = d3.svg.line()
        .x(d => x(d.date))
        .y(d => y(d.active));

        const	valueline2 = d3.svg.line()
        .x(d => x(d.date))
        .y(d => y(d.blocked));

        // Get the data
        dataLineChart.forEach((d) => {
          d.date = formatDate(d.date);
          d.blocked = +d.blocked;
          d.active = +d.active;
        });

        // Scale the range of the data
        x.domain(d3.extent(dataLineChart, d => d.date));
        y.domain([0, d3.max(dataLineChart, d => Math.max(d.blocked, d.active))]);

        // Add the valueline path.
        svg.append('path')
        .attr('id', 'lineDouble')
        .style('stroke', scope.$ctrl.AvColors[0])
        .attr('stroke-width', 3)
        .attr('fill', 'none')
        .attr('d', valueline(dataLineChart));

        // Add the valueline2 path.
        svg.append('path')
        .attr('id', 'lineDouble')
        .style('stroke', scope.$ctrl.AvColors[2])
        .attr('stroke-width', 3)
        .attr('fill', 'none')
        .attr('d', valueline2(dataLineChart));

        // Add the X Axis
        svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(xAxis)
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.8em')
        .attr('dy', '.15em')
        .attr('transform', 'rotate(-65)');

        // Add the Y Axis
        svg.append('g')
        .attr('class', 'y axis')
        .call(yAxis);

        // text label for the x axis
        svg.append('text')
        .attr('transform', `translate(${width / 2},${height + (margin.bottom / 2)})`)
        .attr('font-size', '12px')
        .attr('fill', '#CCCCCC')
        .style('text-anchor', 'middle')
        .text(xAxisLabel);


        // text label for the y axis
        svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - ((height - margin.bottom) / 2))
        .attr('dy', '1em')
        .attr('font-size', '12px')
        .attr('fill', '#CCCCCC')
        .style('text-anchor', 'middle')
        .text('Number');

        const div = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0);

        // Add the scatterplot Active
        svg.selectAll('dot')
        .data(dataLineChart)
        .enter().append('circle')
        .attr('r', 5)
        .attr('fill', scope.$ctrl.AvColors[0])
        .attr('cx', d => x(d.date))
        .attr('cy', d => y(d.active))
        .on('mouseover', (d) => {
          div.transition()
              .duration(200)
              .style('opacity', 0.9);
          div.html(`${d.date}'</br>'Active: ${d.active}`)
              .style('left', `${event.pageX}px`)
              .style('top', `${event.pageY - 28}px`);
        })
        .on('mouseout', () => {
          div.transition()
              .duration(500)
              .style('opacity', 0);
        });
        // Add the scatterplot Blocked
        svg.selectAll('dot')
        .data(dataLineChart)
        .enter().append('circle')
        .attr('r', 5)
        .attr('fill', scope.$ctrl.AvColors[2])
        .attr('cx', d => x(d.date))
        .attr('cy', d => y(d.blocked))
        .on('mouseover', (d) => {
          div.transition()
              .duration(200)
              .style('opacity', 0.9);
          div.html(`${d.date}'</br>'Blocked ${d.blocked}`)
              .style('left', `${event.pageX}px`)
              .style('top', `${event.pageY - 28}px`);
        })
        .on('mouseout', () => {
          div.transition()
              .duration(500)
              .style('opacity', 0);
        });

        //LEGEND
        svg.append('rect')
        .attr('transform', 'translate(510,15)')
        .attr('width', 60)
        .attr('height', 3)
        .style('fill', scope.$ctrl.AvColors[2]);

        svg.append('text')
        .attr('transform', 'translate(540,10)')
        .attr('font-size', '14px')
        .attr('fill', scope.$ctrl.AvColors[2])
        .style('text-anchor', 'middle')
        .text('Blocked');

        svg.append('rect')
        .attr('transform', 'translate(580,15)')
        .attr('width', 60)
		    .attr('height', 3)
        .style('fill', scope.$ctrl.AvColors[0]);

        svg.append('text')
        .attr('transform', 'translate(610,10)')
        .attr('font-size', '14px')
        .attr('fill', scope.$ctrl.AvColors[0])
        .style('text-anchor', 'middle')
        .text('Active');

      });
    },
  bindToController: true,
});

export default DoubleLinesChartDirective;
