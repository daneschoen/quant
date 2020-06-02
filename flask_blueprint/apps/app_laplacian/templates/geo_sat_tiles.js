    var width = 960,
        height = 800;

    var projection = d3.geo.satellite()
        .distance(1.1)
        .scale(4500)
        .rotate([82.00, -34.50, 32.12])
        .center([-2, 5])
        .tilt(30)
        .clipAngle(25);

    var graticule = d3.geo.graticule()
        .extent([[-113, 27], [-47 + 1e-6, 57 + 1e-6]])
        .step([3, 3]);

    var fill = d3.scale.log()
        .domain([10, 500])
        .range(["brown", "steelblue"]);

    var path = d3.geo.path().projection(projection);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    svg.append("path")
        .datum(graticule)
        .attr("class", "graticule")
        .attr("d", path);

    d3.json("/static/js/geo_sat_tiles_us.json", function(error, us) {
      svg.append("g")
          .attr("class", "counties")
        .selectAll("path")
          //.data(topojson.feature(us, us.objects.counties).geometries)  // v1.0
          .data(topojson.object(us, us.objects.counties).geometries)
        .enter().append("path")
          .attr("d", path)
          .style("fill", function(d) { return fill(path.area(d)); });

      svg.append("path")
          .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a.id !== b.id; }))
          .attr("class", "states")
          .attr("d", path);
    });