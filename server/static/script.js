import { Room } from "./room.js";

const testRoom = [
  { x: 0, y: 0, type: "player", ai: "pathfinder" },
  { x: 1, y: 1, type: "block" },
  { x: 1, y: 0, type: "coin" },
];

let room;

async function init() {
  await fetch("/api/rooms/testroom", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(testRoom),
  });
  room = new Room(document.querySelector(".room-area"));

  await update();
}

async function update() {
  const response = await fetch("/api/rooms/testroom");
  const data = await response.json();

  room.setData(data);
}

async function step() {
  await fetch("/api/rooms/testroom/step", { method: "POST" });
  update();
}

init();
document
  .querySelector("#restart-button")
  .addEventListener("click", () => init());
document.querySelector("#step-button").addEventListener("click", () => step());
