class Room {
  constructor(element) {
    this.element = element;
    this.init();
  }

  init(data) {
    d3.select(this.element).select("svg").remove();
    const svg = d3
      .select(this.element)
      .append("svg")
      .attr("id", "room")
      .attr("width", "100%")
      .attr("height", "99vh");

    svg
      .append("rect")
      .attr("id", "background")
      .attr("fill", "black")
      .attr("width", "100%")
      .attr("height", "100%");

    svg.append("g");
  }

  setData(data) {
    let minX = 0;
    let minY = 0;
    let maxX = 1;
    let maxY = 1;
    if (data.length > 0) {
      minX = d3.min(data.map((d) => d.x));
      minY = d3.min(data.map((d) => d.y));
      maxX = d3.max(data.map((d) => d.x)) + 1;
      maxY = d3.max(data.map((d) => d.y)) + 1;
    }
    const svg = d3
      .select(this.element)
      .select("svg")
      .attr("viewBox", `${minX} ${minY} ${maxX - minX} ${maxY - minY}`);
    svg.select("#background").attr("x", minX).attr("y", minY);

    svg
      .select("g")
      .selectAll("rect")
      .data(data)
      .join("rect")
      .attr("x", (d) => d.x)
      .attr("y", (d) => d.y)
      .attr("width", 1)
      .attr("height", 1)
      .attr("fill", (d) => {
        switch (d.type) {
          case "block":
            return "dimgray";
          case "player":
            return "blue";
          case "coin":
            return "yellow";
          default:
            return "red";
        }
      });
  }
}
