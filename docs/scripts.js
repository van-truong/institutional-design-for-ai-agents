const familyByColor = {
  "#D85A30": {
    name: "Social / reputational",
    description: "Mechanisms that shape cooperation through norms, social information, relationships, and standing."
  },
  "#BA7517": {
    name: "Formal / institutional",
    description: "Mechanisms that use explicit rules, recognized authority, contracts, or formal procedures."
  },
  "#639922": {
    name: "Economic / incentive-based",
    description: "Mechanisms that alter the rewards, prices, benefits, or costs attached to a choice."
  },
  "#378ADD": {
    name: "Technical / protocol-enforced",
    description: "Mechanisms implemented through infrastructure, protocols, access controls, or automated constraints."
  },
  "#7F77DD": {
    name: "Mutual aid / solidarity",
    description: "Mechanisms organized around reciprocity, shared ownership, collective provision, and mutual support."
  },
  "#D4537E": {
    name: "Restorative / reparative",
    description: "Mechanisms concerned with repairing harm, restoring relationships, and supporting reintegration."
  }
};

const leafNotes = {
  "Institutional choice": "Participants help choose, revise, or replace the rules under which they interact.",
  "Pigouvian tax": "A cost is attached to an activity in proportion to the harm or externality it creates.",
  "Reputation score": "A recorded assessment of past conduct informs later access, trust, or coordination decisions.",
  "Hard rate limit": "A protocol places a fixed ceiling on how often an actor can use a resource or perform an action.",
  "Participatory budgeting": "Members collectively decide how a shared pool of resources should be allocated.",
  "Restitution": "A party responsible for harm returns value or otherwise compensates the party that was harmed.",
  "Apology": "An actor acknowledges harm or wrongdoing as one step in a wider process of repair."
};

const map = document.querySelector("#taxonomy-map");
const leafName = document.querySelector("#leaf-name");
const leafFamily = document.querySelector("#leaf-family");
const leafDescription = document.querySelector("#leaf-description");
const leafStatus = document.querySelector("#leaf-status");
let currentRotation = 0;
let rotationFrame;
let rotationLocked = false;

function showLeaf(label, color) {
  const family = familyByColor[color] || {
    name: "Cooperation-shaping mechanism",
    description: "This mechanism is part of the working taxonomy."
  };
  leafName.textContent = label;
  leafFamily.textContent = family.name;
  leafDescription.textContent = leafNotes[label] || family.description;
  leafStatus.innerHTML = `<span></span>${leafNotes[label] ? "Definition drafted · evidence review pending" : "Definition and evidence review pending"}`;
}

function shortestRotation(target) {
  const delta = ((target - currentRotation + 540) % 360) - 180;
  return currentRotation + delta;
}

function orientActiveFamilyText(wheel, angle) {
  wheel.querySelectorAll(".active-family-label").forEach((group) => {
    const pivot = group.dataset.originalTransform?.match(/rotate\([^ ]+\s+([-\d.]+)\s+([-\d.]+)\)/);
    if (pivot) group.setAttribute("transform", `rotate(${-angle} ${pivot[1]} ${pivot[2]})`);
  });
}

function selectFamilyText(wheel, color) {
  wheel.querySelectorAll(".active-family-label").forEach((group) => {
    group.setAttribute("transform", group.dataset.originalTransform || "");
    group.classList.remove("active-family-label");
  });

  wheel.querySelectorAll("g").forEach((group) => {
    const text = group.querySelector(":scope > .fam-label, :scope > .disc-label");
    if (text?.getAttribute("fill")?.toUpperCase() !== color) return;
    group.dataset.originalTransform = group.getAttribute("transform") || "";
    group.classList.add("active-family-label");
  });
  orientActiveFamilyText(wheel, currentRotation);
}

function rotateWheelToLeaf(wheel, leaf, color) {
  const dot = leaf.previousElementSibling;
  const x = Number(dot?.getAttribute("cx"));
  const y = Number(dot?.getAttribute("cy"));
  if (!Number.isFinite(x) || !Number.isFinite(y)) return;

  const leafAngle = Math.atan2(y - 500, x - 500) * 180 / Math.PI;
  const startRotation = currentRotation;
  const targetRotation = shortestRotation(-90 - leafAngle);
  const startTime = performance.now();
  const duration = 650;

  selectFamilyText(wheel, color);
  cancelAnimationFrame(rotationFrame);
  function turn(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const angle = startRotation + (targetRotation - startRotation) * eased;
    wheel.setAttribute("transform", `rotate(${angle} 500 500)`);
    orientActiveFamilyText(wheel, angle);
    if (progress < 1) {
      rotationFrame = requestAnimationFrame(turn);
    } else {
      currentRotation = targetRotation;
    }
  }
  rotationFrame = requestAnimationFrame(turn);
}

function highlightLeaf(svgDocument, wheel, leaf) {
  svgDocument.querySelectorAll(".is-active, .branch-active, .leaf-node-active, .branch-node-active").forEach((element) => {
    element.classList.remove("is-active", "branch-active", "leaf-node-active", "branch-node-active");
  });

  const dot = leaf.previousElementSibling;
  const line = dot?.previousElementSibling;
  const branch = line?.previousElementSibling;
  leaf.classList.add("is-active");
  dot?.classList.add("leaf-node-active");
  line?.classList.add("branch-active");
  branch?.classList.add("branch-active");

  const branchStart = branch?.getAttribute("d")?.match(/^M\s*([\d.]+)\s+([\d.]+)/);
  if (branchStart) {
    const startX = Number(branchStart[1]);
    const startY = Number(branchStart[2]);
    [...wheel.querySelectorAll('circle[r="4"]')].find((circle) =>
      Math.abs(Number(circle.getAttribute("cx")) - startX) < 0.05 &&
      Math.abs(Number(circle.getAttribute("cy")) - startY) < 0.05
    )?.classList.add("branch-node-active");
  }
}

function initializeTaxonomy() {
  const svgDocument = map.contentDocument;
  if (!svgDocument) return;
  if (svgDocument.documentElement.dataset.interactiveReady) return;
  svgDocument.documentElement.dataset.interactiveReady = "true";

  const svgRoot = svgDocument.documentElement;
  const centerCircle = svgRoot.querySelector('circle[cx="500"][cy="500"][r="60"]');
  const wheel = svgDocument.createElementNS("http://www.w3.org/2000/svg", "g");
  wheel.setAttribute("id", "taxonomy-wheel");
  svgRoot.insertBefore(wheel, centerCircle);
  [...svgRoot.children].filter((element) =>
    !["title", "desc", "style", "taxonomy-wheel"].includes(element.id || element.tagName) &&
    element !== centerCircle &&
    !element.classList.contains("root-big")
  ).forEach((element) => wheel.appendChild(element));

  const style = svgDocument.createElementNS("http://www.w3.org/2000/svg", "style");
  style.textContent = `
    .leaf-label { cursor: pointer; transition: fill .12s ease, font-size .12s ease; }
    .leaf-label:hover, .leaf-label:focus, .leaf-label.is-active { fill: #7c1948 !important; font-size: 10.5px; font-weight: 700; outline: none; }
    .branch-active { stroke-width: 2.5 !important; opacity: 1 !important; }
    .leaf-node-active { r: 5px; stroke: #fff; stroke-width: 2px; }
    .branch-node-active { r: 6px; stroke-width: 3px; fill: #fff; }
  `;
  svgRoot.appendChild(style);

  wheel.querySelectorAll(".leaf-label").forEach((leaf) => {
    const dot = leaf.previousElementSibling;
    const color = dot?.getAttribute("fill")?.toUpperCase();
    const label = leaf.textContent.trim();

    function activate(rotate = true) {
      showLeaf(label, color);
      highlightLeaf(svgDocument, wheel, leaf);
      if (rotate) rotateWheelToLeaf(wheel, leaf, color);
    }

    leaf.setAttribute("tabindex", "0");
    leaf.setAttribute("role", "button");
    leaf.setAttribute("aria-label", `${label}. Show taxonomy details.`);
    leaf.addEventListener("mouseenter", () => {
      if (rotationLocked) return;
      rotationLocked = true;
      activate();
      window.setTimeout(() => { rotationLocked = false; }, 700);
    });
    leaf.addEventListener("focus", () => activate());
    leaf.addEventListener("click", () => activate());
    leaf.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        activate();
      }
    });
  });
}

map.addEventListener("load", initializeTaxonomy);
if (map.contentDocument?.documentElement) initializeTaxonomy();
