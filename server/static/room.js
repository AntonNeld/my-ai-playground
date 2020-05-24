const testRoom = [
  { x: 0, y: 0, type: "player", ai: "pathfinder" },
  { x: 1, y: 1, type: "block" },
  { x: 1, y: 0, type: "coin" },
];

async function init() {
  await fetch("/api/rooms/testroom", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(testRoom),
  });
  d3.select("#room").remove();
  const svg = d3
    .select(".room-area")
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

  await update();
}

async function update() {
  const response = await fetch("/api/rooms/testroom");
  const newData = await response.json();

  let minX = 0;
  let minY = 0;
  let maxX = 1;
  let maxY = 1;
  if (newData.length > 0) {
    minX = d3.min(newData.map((d) => d.x));
    minY = d3.min(newData.map((d) => d.y));
    maxX = d3.max(newData.map((d) => d.x)) + 1;
    maxY = d3.max(newData.map((d) => d.y)) + 1;
  }
  const svg = d3
    .select("#room")
    .attr("viewBox", `${minX} ${minY} ${maxX - minX} ${maxY - minY}`);
  d3.select("#background").attr("x", minX).attr("y", minY);

  svg
    .select("g")
    .selectAll("rect")
    .data(newData)
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

async function step() {
  await fetch("/api/rooms/testroom/step", { method: "POST" });
  update();
}

init();
