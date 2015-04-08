var diameter = 800,
format = d3.format(",d"),
color = d3.scale.category20c();

var bubble = d3.layout.pack()
//  .sort(null)
//  .sort(d3.ascending)
//  .sort(d3.descending)
//    .sort( function(a, b) { return  -1;} ) // basically a < b always
    .sort(function(a, b) { return -(a.value - b.value); }) // circular layout
    .size([diameter, diameter])
    .padding(1.5);

var svg = d3.select(".starter-template").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");

// The variable final_result must be set outside this file, first!
// d3.json("static/js/final_python_use.json", function(error, root) 
d3.json(final_result, function(error, root) 
{
  var node = svg.selectAll(".node")
        .data(bubble.nodes(classes(root))
        .filter(function(d) { return !d.children; }))
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  node.append("title")
      .text(function(d) { return d.className + ": " + format(d.value); });

  node.append("circle")
      .attr("r", function(d) { return d.r; })
      .style("fill", function(d) 
            { 
                return color(d.packageName); 
                // return color(d.value); // this gives a different color for every leaf node
            });

  node.append("text")
      .attr("dy", ".3em")
      .style("text-anchor", "middle")
      .text(function(d) { return d.className.substring(0, d.r / 3); });
});

// Returns a flattened hierarchy containing all leaf nodes under the root.
function classes(root) 
{
  var classes = [];

  function recurse(name, node) {
    if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
    else classes.push({packageName: name, className: node.name, value: node.size});
  }

  recurse(null, root);
  return {children: classes};
}

d3.select(self.frameElement).style("height", diameter + "px");
