export class Room {
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

    const transition = svg.transition().duration(300).ease(d3.easeQuadOut);
    svg
      .select("g")
      .selectAll("image")
      .data(data, ({ id }) => id)
      .join(
        (enter) =>
          enter
            .append("image")
            .attr("x", (d) => d.x)
            .attr("y", (d) => d.y)
            .attr("width", 1)
            .attr("height", 1)
            .attr("href", (d) => `assets/${d.type}.svg`)
            .attr("opacity", 0)
            .call((enter) => enter.transition(transition).attr("opacity", 1)),
        (update) =>
          update.call((update) =>
            update
              .transition(transition)
              .attr("x", (d) => d.x)
              .attr("y", (d) => d.y)
          ),
        (exit) =>
          exit
            .attr("opacity", 1)
            .call((exit) =>
              exit.transition(transition).attr("opacity", 0).remove()
            )
      );
  }
}
