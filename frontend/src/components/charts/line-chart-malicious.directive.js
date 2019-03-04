import * as d3 from 'd3';
import moment from 'moment';

const DAY_TIME_AGR = {
    hour: '0',
    day: '1',
    week: '2',
    month: '3'
};

export const lineChartDataMaliciousDirective = ($compile, $timeout) => ({
    restrict: 'A',
    link(scope, element) {
      scope.$watch('$ctrl.lineChartDataMalicious', () => {
        document.getElementById('chart_malicious').innerHTML = '';
            if(!scope.$ctrl.lineChartDataMalicious)
                return;

            let dataLineChart = scope.$ctrl.lineChartDataMalicious[0].values;

            if (!dataLineChart || dataLineChart.length === 0)
                return;

            // Set the dimensions of the canvas / graph
            var margin = { top: 30, right: 20, bottom: 40, left: 50 },
                width = 700 - margin.left - margin.right,
                height = 464 - margin.top - margin.bottom;

            // Adds the svg canvas
            var svg = d3.select('#chart_malicious').append('svg')
                .attr('viewBox', '0, 0, ' + (width + margin.left + margin.right) + ', ' + (height + margin.top + margin.bottom))
                .attr('width', '100%')
                .attr('height', '54vh')
                .append('g')
                .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

            const data = [];
            var xAxisLabel = 'Time';
            var xTimeFormat;
            var formatDate = d3.time.format('%Y-%m-%dT%H:%M:%SZ');

            dataLineChart.forEach(element => {
                data.push({
                    date: formatDate.parse(element[0]),
                    value: +element[1]
                });
            });

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

            // Set the ranges

            var x = d3.time.scale()
                .range([0, width]);

            var y = d3.scale.linear()
                .range([height - margin.bottom, 0]);

            // // Define the axes
            var xAxis = d3.svg.axis().scale(x)
                .orient('bottom')
                .tickFormat(d3.time.format(xTimeFormat));

            var yAxis = d3.svg.axis().scale(y)
                .orient('left').ticks(5);

            x.domain(d3.extent(data, function (d) { return d.date; }));
            y.domain([0, d3.max(data, function (d) { return d.value; })]);

            var defs = svg.append('defs');
            var gradient = defs.append('linearGradient')
                .attr('id', 'svgGradient')
                .attr('x1', '0%')
                .attr('x2', '100%')
                .attr('y1', '0%')
                .attr('y2', '100%');

            gradient.append('stop')
                .attr('class', 'start')
                .attr('offset', '0%')
                .attr('stop-color', scope.$ctrl.AvColors[0])
                .attr('stop-opacity', 1);

            gradient.append('stop')
                .attr('class', 'end')
                .attr('offset', '100%')
                .attr('stop-color', 'white')
                .attr('stop-opacity', 0);

            // Define the area
            var area = d3.svg.area()
                .x(function (d) { return x(d.date); })
                .y0(y(0))
                .y1(function (d) { return y(d.value); })

            // Add the area
            svg.append('path')
                .datum(data)
                .attr('fill', 'url(#svgGradient)')
                .attr('d', area);

            //Define the line
            var valueline = d3.svg.line()
                .x(function (d) { return x(d.date); })
                .y(function (d) { return y(d.value); });

            // add the valueline path.
            svg.append('path')
                .data([data])
                .attr('stroke', scope.$ctrl.AvColors[scope.$ctrl.attackIndex])
                .attr('stroke-width', '3px')
                .attr('fill', 'none')
                .attr('d', valueline);

            var div = d3.select('body').append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0);

            // Add the scatterplot
            svg.selectAll('dot')
                .data(data)
                .enter().append('circle')
                .attr('r', 5)
                .attr('fill', scope.$ctrl.AvColors[0])
                .attr('cx', function (d) { return x(d.date); })
                .attr('cy', function (d) { return y(d.value); })
                .on('mouseover', function (d) {
                    div.transition()
                        .duration(200)
                        .style('opacity', .9);
                    div.html(d.date + '</br>' + d.value)
                        .style('left', (event.pageX) + 'px')
                        .style('top', (event.pageY - 28) + 'px');
                })
                .on('mouseout', function (d) {
                    div.transition()
                        .duration(500)
                        .style('opacity', 0);
                });

            // Add the X Axis
            svg.append('g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,' + (height - margin.bottom) + ')')
                .call(xAxis)
                .selectAll('text')
                .style('text-anchor', 'end')
                .attr('dx', '-.8em')
                .attr('dy', '.15em')
                .attr('transform', 'rotate(-65)');

            // text label for the x axis
            svg.append('text')
                .attr('transform', 'translate(' + (width / 2) + ' ,' + (height + margin.bottom / 2) + ')')
                .attr('font-size', '12px')
                .attr('fill', '#CCCCCC')
                .style('text-anchor', 'middle')
                .text(xAxisLabel);

            // Add the Y Axis
            svg.append('g')
                .attr('class', 'y axis')
                .call(yAxis);

            // text label for the y axis
            svg.append('text')
                .attr('transform', 'rotate(-90)')
                .attr('y', 0 - margin.left)
                .attr('x', 0 - ((height - margin.bottom) / 2))
                .attr('dy', '1em')
                .attr('font-size', '12px')
                .attr('fill', '#CCCCCC')
                .style('text-anchor', 'middle')
                .text('Number of occurrences');
        });
    },
    bindToController: true
});

export default lineChartDataMaliciousDirective;
