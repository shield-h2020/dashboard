import * as d3 from 'd3';

export const DashViewerDirective = () => {

    let svgHeight = 800;
    let svgWidth;
    let svg;
    let pieWidth = 250;
    let pieHeight = 250;
    let barChartWidth;// = 250;
    let barChartHeight = 250;
    var color = d3.scaleOrdinal(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    let simData = [
        { age: "A", population: 10 }, 
        { age: "B", population: 20 }, 
        { age: "C", population: 10 }, 
        { age: "D", population: 40 }, 
        { age: "E", population: 10 }
    ];

    function init(scope, element) {
        
        //height = element.clientHeight;
        svgWidth = element.clientWidth;
        barChartWidth = element.clientWidth;
        svg = d3.select(element)
            .append('svg')
            .attr('width', svgWidth)
            .attr('height', svgHeight);

            drawPieChart();
            //drawLineChart()
            drawBarChart();
    }

    function drawPieChart() {

        var g = svg.append("g").
            attr("transform", "translate(" + pieWidth / 2 + "," + pieHeight / 2 + ")");

        var radius = Math.min(pieWidth, pieHeight) / 2;
        var pie = d3.pie()
            .sort(null)
            .value(function(simData) {return simData.population; });

        var path = d3.arc()
            .outerRadius(radius - 10)
            .innerRadius(0);
        
        var label = d3.arc()
            .outerRadius(radius - 40)
            .innerRadius(radius - 40);

        var arc = g.selectAll(".arc")
        .data(pie(simData))
        .enter().append("g")
            .attr("class", "arc");
    
        arc.append("path")
            .attr("d", path)
            .attr("fill", function(d) { return color(d.data.age); });
    
        arc.append("text")
            .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
            .attr("dy", "0.35em")
            .text(function(d) {return d.data.age; });
    }

    function drawBarChart() {

        var g = svg.append("g").
            attr("transform", "translate(" + 25 + "," + Number(pieHeight + 30) + ")");

        var x = d3.scaleBand().rangeRound([0, barChartWidth]).padding(0.1),
            y = d3.scaleLinear().rangeRound([barChartHeight, 0]);

        x.domain(simData.map(function(d) {return d.age; }));
        y.domain([0, d3.max(simData, function(d) { return d.population; })]);

        g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + barChartHeight + ")")
            .call(d3.axisBottom(x));

        g.append("g")
            .attr("class", "axis axis--y")
            .call(d3.axisLeft(y))
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Frequency");

        g.selectAll(".bar")
            .data(simData)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.age); })
            .attr("y", function(d) { return y(d.population); })
            .attr("width", x.bandwidth())
            .attr("fill", function(d) { return color(d.age); })
            .attr("height", function(d) { return barChartHeight - y(d.population); });
    }

    function drawLineChart() {

        tempImportDrawLineChart();
    }

    function tempImportDrawLineChart() {

        d3.tsv("data.tsv", type, function(error, data) {
            if (error) throw error;
            
            console.log(data);
            /*var cities = data.columns.slice(1).map(function(id) {
              return {
                id: id,
                values: data.map(function(d) {
                  return {date: d.date, temperature: d[id]};
                })
              };
            });*/
        });
    }

    function type(d, _, columns) {
        d.date = parseTime(d.date);
        for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
        
        return d;
    }

    return {
        restrict: 'A',
        link(scope, element) {
          init(scope, element[0]);
        },
    };
};