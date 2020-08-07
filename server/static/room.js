const drawOrder = [
  "player",
  "vacuum",
  "dirt",
  "coin",
  "wall",
  "labelA",
  "labelB",
];

export class Room extends EventTarget {
  constructor(element) {
    super();
    this.element = element;
    this.highlighted = null;
    this.data = [];
    this.init();
  }

  init() {
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
      .attr("height", "100%")
      .on("click", () => {
        this.highlighted = null;
        this.dispatchEvent(
          new CustomEvent("highlighted", {
            detail: { id: this.highlighted },
          })
        );
        this.draw();
      });

    svg.append("g");
  }

  setData(data) {
    // Filter to remove undrawable entities,
    // sort to make some types of entities appear above others
    this.data = data
      .filter(({ position, looksLike }) => position && looksLike)
      .sort(
        (a, b) =>
          drawOrder.indexOf(b.looksLike) - drawOrder.indexOf(a.looksLike)
      );
    this.draw();
  }

  draw() {
    const data = this.data;
    let minX = 0;
    let minY = 0;
    let maxX = 1;
    let maxY = 1;
    if (data.length > 0) {
      minX = d3.min(data.map((d) => d.position.x));
      minY = d3.min(data.map((d) => -d.position.y));
      maxX = d3.max(data.map((d) => d.position.x)) + 1;
      maxY = d3.max(data.map((d) => -d.position.y)) + 1;
    }
    const svg = d3
      .select(this.element)
      .select("svg")
      .attr("viewBox", `${minX} ${minY} ${maxX - minX} ${maxY - minY}`);
    svg.select("#background").attr("x", minX).attr("y", minY);

    const transition = svg.transition().duration(300).ease(d3.easeQuadOut);
    svg
      .select("g")
      .selectAll("g")
      .data(data, ({ id }) => id)
      .join(
        (enter) => {
          const g = enter
            .append("g")
            .attr(
              "transform",
              (d) => `translate(${d.position.x},${-d.position.y})`
            )
            .attr("opacity", 0)
            .call((g) => g.transition(transition).attr("opacity", 1));
          g.append("image")
            .attr("width", 1)
            .attr("height", 1)
            .attr("href", (d) => `assets/${d.looksLike}.svg`);
          g.append("rect")
            .attr("width", 1)
            .attr("height", 1)
            .attr("stroke", "red")
            .attr("fill-opacity", 0)
            .attr("stroke-width", 0.02)
            .attr("opacity", (d) => (d.id === this.highlighted ? 1 : 0));
          g.append("text")
            .attr("x", 0.38)
            .attr("y", 0.6)
            .attr("font-size", 0.4)
            .attr("fill", "white")
            .text((d) => d.score);
          g.append("rect")
            .attr("width", 1)
            .attr("height", 1)
            .attr("opacity", 0)
            .on("click", (d) => {
              if (this.highlighted === d.id) {
                this.highlighted = null;
              } else {
                this.highlighted = d.id;
              }
              this.dispatchEvent(
                new CustomEvent("highlighted", {
                  detail: { id: this.highlighted },
                })
              );
              this.draw();
            });
          return g;
        },
        (update) =>
          update.call((update) => {
            update
              .transition(transition)
              .attr(
                "transform",
                (d) => `translate(${d.position.x},${-d.position.y})`
              );
            update
              .select("rect")
              .transition(transition)
              .attr("opacity", (d) => (d.id === this.highlighted ? 1 : 0));
            update.select("text").text((d) => d.score);
            return update;
          }),
        (exit) =>
          exit
            .attr("opacity", 1)
            .transition(transition)
            .attr("opacity", 0)
            .remove()
      );
  }
}
