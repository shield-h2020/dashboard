import * as d3 from 'd3';
import moment from 'moment';

const DAY_TIME_AGR = {
    hour: '0',
    day: '1',
    week: '2',
    month: '3'
};

export const BarChartDirective = ($compile, $timeout) => ({
    restrict: 'A',
    link(scope, element) {
        scope.$watch('$ctrl.barChartData', function () {
            document.getElementById('chart_ocurrences').innerHTML = '';

            let datachart = scope.$ctrl.barChartData;

            if (!datachart)
                return;

            // Configs
            const Chart = {
                margin: { top: 30, right: 20, bottom: 40, left: 50 },
                width: 700 - 50 - 30,                                   //width - margin.left - margin.right
                height: 464 - 30 - 30,                                  //height - margin.top - margin.bottom
                sideWidth: 10,
                bottomHeight: 60,
            };

            var n = datachart[0].values.length, // number of samples
                m = datachart.length;           // number of series

            var data = [];
            var maxValue = 0;
            for (let i = 0; i < datachart.length; i += 1) {
                var innerData = [];
                for (let j = 0; j < datachart[i].values.length; j += 1) {
                    innerData[j] = datachart[i].values[j][1];
                    if (innerData[j] > maxValue)
                        maxValue = innerData[j];
                }
                data[i] = innerData;
            }

            var xAxisData = [];
            var xAxisLabel = "Time";

            for (let i = 0; i < datachart[0].values.length; i += 1) {
                if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.hour) {
                    xAxisData[i] = moment.utc(datachart[0].values[i][0]).format('HH:mm');
                }
                if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.day) {
                    xAxisData[i] = moment.utc(datachart[0].values[i][0]).format('DD-MM');
                }
                if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.week) {
                    xAxisData[i] = moment.utc(datachart[0].values[i][0]).format('DD-MM');
                }
                if (scope.$ctrl.dayTimeAgr === DAY_TIME_AGR.month) {
                    xAxisData[i] = moment.utc(datachart[0].values[i][0]).format('MMMM').substring(0, 3);
                }
            }

            var y = d3.scale.linear()
                .domain([0, maxValue], 1)
                .range([0, (Chart.height - Chart.margin.bottom)]);

            var x0 = d3.scale.ordinal()
                .domain(d3.range(n))
                .rangeBands([0, Chart.width], 0.1);

            var x1 = d3.scale.ordinal()
                .domain(d3.range(m))
                .rangeBands([0, x0.rangeBand()], 0.1);

            var color;
            if (scope.$ctrl.attackIndex === -1)
                color = d3.scale.ordinal().range(scope.$ctrl.AvColors);
            else
                color = d3.scale.ordinal().range([scope.$ctrl.AvColors[scope.$ctrl.attackIndex]]);

            // Set the ranges
            var xScale = d3.scale.ordinal()
                .domain(xAxisData)
                .rangeBands([0, Chart.width]);

            var yScale = d3.scale.linear()
                .domain([0, maxValue])
                .range([(Chart.height - Chart.margin.bottom), 0]);

            //Set the axis
            var xAxis = d3.svg.axis()
                .scale(xScale)
                .orient("bottom");


            var yAxis = d3.svg.axis()
                .scale(yScale)
                .orient("left")
                .ticks(Math.min(10, maxValue))
                .tickSize(-Chart.width);

            //Add svg to body
            var svg = d3.select("#chart_ocurrences").append("svg")
                .attr("viewBox", "0, 0, "+ (Chart.width + Chart.margin.left + Chart.margin.right) + ", "+ (Chart.height + Chart.margin.top + Chart.margin.bottom))
                .attr("width", "100%")
                .attr("height","54vh")
                .append("g")
                .attr("transform", "translate(" + Chart.margin.left + "," + Chart.margin.top + ")");

            // Add y axis
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

            // text label for the y axis
            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - Chart.margin.left)
                .attr("x", 0 - (Chart.height / 2))
                .attr("dy", "1em")
                .attr("font-size", "12px")
                .attr("fill", "#CCCCCC")
                .style("text-anchor", "middle")
                .text("Number of occurrences");

            // Add x axis
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + (Chart.height - Chart.margin.bottom) + ")")
                .call(xAxis)
                .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-65)");

            // text label for the x axis
            svg.append("text")
                .attr("transform", "translate(" + (Chart.width / 2) + " ," + (Chart.height + Chart.margin.bottom / 2) + ")")
                .attr("font-size", "12px")
                .attr("fill", "#CCCCCC")
                .style("text-anchor", "middle")
                .text(xAxisLabel);

            svg.append("g").selectAll("g")
                .data(data)
                .enter().append("g")
                .style("fill", function (d, i) { return color(i); })
                .attr("transform", function (d, i) { return "translate(" + x1(i) + ",0)"; })
                .selectAll("rect")
                .data(function (d) { return d; })
                .enter().append("rect")
                .attr("width", x1.rangeBand())
                .attr("height", y)
                .attr("x", function (d, i) { return x0(i); })
                .attr("y", function (d) { return Chart.height - Chart.margin.bottom - y(d); })
                .attr("stroke", "black")
                .attr("stroke-opacity", "0.2");

        })
    },
    bindToController: true
});

export default BarChartDirective;
