import * as d3 from 'd3';
import styles from './donut-labels-chart.scss';

export const DonutLabelsChartDirective = ($compile, $timeout) => ({
    restrict: 'A',
    link(scope, element) {
        scope.$watch('$ctrl.donutChartData', function () {
            document.getElementById('chart_attacks').innerHTML = '';

            let data = scope.$ctrl.donutChartData;

            if (!data)
                return;

            var color;
            const legendRectSize = 16;
            const legendHeight = 100;
            var nrSeries = data.length;

            var svg = d3.select("#chart_attacks")
                .append("svg")
                .attr({
                    viewBox: "0, 0, 600, 450",
                    width: "100%",
                    height: "54vh"
                })
                .append("g")
                .attr({
                    transform: `translate(${600 / 2},${450 / 2})`,
                });

            svg.append("g")
                .attr("class", "slices");
            svg.append("g")
                .attr("class", "labels");
            svg.append("g")
                .attr("class", "lines");

            var width = 600,
                height = 400,
                radius = Math.min(width, height) / 2;

            var pie = d3.layout.pie()
                .sort(null)
                .value(function (d) {
                    return d.value;
                });

            var arc = d3.svg.arc()
                .outerRadius(radius * 0.7)
                .innerRadius(radius * 0.6);

            var outerArc = d3.svg.arc()
                .innerRadius(radius * 0.9)
                .outerRadius(radius * 0.9);

            svg.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

            var key = function (d) { return d.data.name; };

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

            const dataset = [];
            if (data) {
                for (let i = 0; i < data.length; i += 1) {
                    dataset.push({
                        label: data[i].values[0][1] + " attacks",
                        name: data[i].tags.attack_type,
                        value: data[i].values[0][1],
                    });
                }
            }
            change(dataset);

            function change(data) {
                /* ------- PIE SLICES -------*/
                var slice = svg.select(".slices").selectAll("path.slice")
                    .data(pie(data), key);

                slice.enter()
                    .insert("path")
                    .style("fill", function (d) { return color(d.data.name); })
                    .attr("class", "slice")
                    .on("click", (d, i) => {
                        if (scope.$ctrl.attackIndex === i) {
                            scope.$ctrl.attackIndex = -1;
                            scope.$ctrl.attackType = null;

                            scope.$ctrl.getTotalAttacks();
                            scope.$ctrl.getAttacks();
                            scope.$ctrl.getTotalAttackByDay();
                        }
                        else {
                            var selectedAttack = d.data.name.substring(0, d.data.name.indexOf("-") - 1);
                            scope.$ctrl.attackIndex = i;
                            scope.$ctrl.attackType = selectedAttack;

                            scope.$ctrl.getTotalAttacks();
                            scope.$ctrl.getAttacks();
                            scope.$ctrl.getTotalAttackByDay();
                        }
                    })
                    .on("mouseover", function (d) {
                        d3.select(this).style("cursor", "pointer");
                    })
                    .on("mouseout", function (d) {
                        d3.select(this).style("cursor", "default");
                    });

                slice
                    .transition().duration(1000)
                    .attrTween("d", function (d) {
                        this._current = this._current || d;
                        var interpolate = d3.interpolate(this._current, d);
                        this._current = interpolate(0);
                        return function (t) {
                            return arc(interpolate(t));
                        };
                    })

                slice.exit()
                    .remove();

                /* ------- TEXT LABELS -------*/

                var text = svg.select(".labels").selectAll("text")
                    .data(pie(data), key);

                text.enter()
                    .append("text")
                    .attr("dy", ".35em")
                    .text(function (d) {
                        return d.data.label;
                    });

                function midAngle(d) {
                    return d.startAngle + (d.endAngle - d.startAngle) / 2;
                }

                text.transition().duration(1000)
                    .attrTween("transform", function (d) {
                        this._current = this._current || d;
                        var interpolate = d3.interpolate(this._current, d);
                        this._current = interpolate(0);
                        return function (t) {
                            var d2 = interpolate(t);
                            var pos = outerArc.centroid(d2);
                            pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
                            return "translate(" + pos + ")";
                        };
                    })
                    .styleTween("text-anchor", function (d) {
                        this._current = this._current || d;
                        var interpolate = d3.interpolate(this._current, d);
                        this._current = interpolate(0);
                        return function (t) {
                            var d2 = interpolate(t);
                            return midAngle(d2) < Math.PI ? "start" : "end";
                        };
                    });

                text.exit()
                    .remove();

                /* ------- SLICE TO TEXT POLYLINES -------*/

                var polyline = svg.select(".lines").selectAll("polyline")
                    .data(pie(data), key);

                polyline.enter()
                    .append("polyline")
                    .attr("fill", "none")
                    .attr("stroke",function (d) { return color(d.data.name); })
                    .attr("stroke-width","2px");

                polyline.transition().duration(1000)
                    .attrTween("points", function (d) {
                        this._current = this._current || d;
                        var interpolate = d3.interpolate(this._current, d);
                        this._current = interpolate(0);
                        return function (t) {
                            var d2 = interpolate(t);
                            var pos = outerArc.centroid(d2);
                            pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
                            return [arc.centroid(d2), outerArc.centroid(d2), pos];
                        };
                    });

                polyline.exit()
                    .remove();

                /* ------- LEGENDS -------*/

                const legend = svg.selectAll('.legend')
                    .data(color.domain())
                    .enter()
                    .append('g')
                    .attr({
                        class: 'legend',
                        transform(d, i) {
                            // Just a calculation for x & y position
                            if (i >= 4) {
                                return `translate(${((i-4) * legendHeight) - (25 * nrSeries)},230)`;
                            }
                            else {
                                return `translate(${(i * legendHeight) - (25 * nrSeries)},200)`;
                            }

                        },
                    });

                legend.append('rect')
                    .attr({
                        width: legendRectSize,
                        height: legendRectSize,
                        rx: 16,
                        ry: 16,
                    })
                    .style({
                        fill: color,
                        stroke: color,
                    });

                legend.append('text')
                    .attr({
                        x: 20,
                        y: 15,
                    })
                    .text(d => d)
                    .style({
                        fill: '#818181',
                        'font-size': '12px'
                    })
                    .on("click", (d, i) => {
                        if (scope.$ctrl.attackIndex === i) {

                            //console.log("Resetting value");
                            scope.$ctrl.attackIndex = -1;
                            scope.$ctrl.attackType = null;

                            scope.$ctrl.getTotalAttacks();
                            scope.$ctrl.getAttacks();
                            scope.$ctrl.getTotalAttackByDay();
                        }
                        else {
                            var selectedAttack = d.substring(0, d.indexOf("-") - 1);
                            scope.$ctrl.attackIndex = i;
                            scope.$ctrl.attackType = selectedAttack;

                            scope.$ctrl.getTotalAttacks();
                            scope.$ctrl.getAttacks();
                            scope.$ctrl.getTotalAttackByDay();
                        }
                    })
                    .on("mouseover", function (d) {
                        d3.select(this).style("cursor", "pointer");
                    })
                    .on("mouseout", function (d) {
                        d3.select(this).style("cursor", "default");
                    });
            };


        });
    },
    bindToController: true
});

export default DonutLabelsChartDirective;
