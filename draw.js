(() => {
  const drawing = document.querySelector(".drawing-svg");
  const palette = document.getElementById("palette");
  const undoBtn = document.getElementById("undoBtn");
  const resetBtn = document.getElementById("resetBtn");
  const finishBtn = document.getElementById("finishBtn");
  const successModal = document.getElementById("successModal");
  const successText = document.getElementById("successText");
  const saveStatus = document.getElementById("saveStatus");

  if (!drawing) return;

  const SVG_NS = "http://www.w3.org/2000/svg";

  let selectedColor = "#E53935";
  let tool = "fill";
  let brushSize = 16;
  let isDrawing = false;
  let activeStroke = null;
  let activeStrokePoints = [];
  let saveTimer = null;
  let saveInFlight = false;
  let pendingSave = false;

  const history = [];
  const fillables = [...drawing.querySelectorAll(".fillable")];

  // Keep brush paint inside the same SVG so it scales with the drawing.
  let brushLayer = drawing.querySelector("#brushLayer");
  if (!brushLayer) {
    brushLayer = document.createElementNS(SVG_NS, "g");
    brushLayer.setAttribute("id", "brushLayer");
    drawing.appendChild(brushLayer);
  }

  function getFills() {
    const fills = {};
    fillables.forEach(el => {
      const region = el.dataset.region;
      if (!region) return;
      const color = el.style.fill || "#FFFFFF";
      if (color && color.toUpperCase() !== "#FFFFFF" && color.toLowerCase() !== "white") {
        fills[region] = color;
      }
    });
    return fills;
  }

  function getStrokes() {
    return [...brushLayer.querySelectorAll(".brush-stroke")].map(path => ({
      d: path.getAttribute("d") || "",
      color: path.getAttribute("stroke") || "#E53935",
      width: Number(path.getAttribute("stroke-width")) || 16
    }));
  }

  function getState() {
    return {
      fills: getFills(),
      strokes: getStrokes(),
      last_tool: tool
    };
  }

  function applyState(state) {
    if (!state || typeof state !== "object") return;

    const fills = state.fills || {};
    fillables.forEach(el => {
      const region = el.dataset.region;
      el.style.fill = fills[region] || "#FFFFFF";
    });

    brushLayer.innerHTML = "";
    const strokes = Array.isArray(state.strokes) ? state.strokes : [];
    strokes.forEach(stroke => {
      if (!stroke || !stroke.d) return;
      const path = createBrushPath(
        stroke.d,
        stroke.color || "#E53935",
        Number(stroke.width) || 16
      );
      brushLayer.appendChild(path);
    });
  }

  function cloneState() {
    return JSON.parse(JSON.stringify(getState()));
  }

  function pushHistory() {
    history.push(cloneState());
    if (history.length > 50) history.shift();
  }

  function showSaveStatus(text, stateClass = "") {
    if (!saveStatus) return;
    saveStatus.textContent = text;
    saveStatus.classList.remove("saving", "saved", "error");
    if (stateClass) saveStatus.classList.add(stateClass);
  }

  async function saveNow() {
    if (saveInFlight) {
      pendingSave = true;
      return;
    }

    saveInFlight = true;
    pendingSave = false;
    showSaveStatus("Saving your drawing…", "saving");

    try {
      const response = await fetch(`/api/progress/${window.LUMI_DRAWING_ID}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(getState())
      });

      const data = await response.json();
      if (!response.ok || !data.ok) throw new Error(data.message || "Save failed");

      showSaveStatus("Saved ✓ · you can continue anytime", "saved");
    } catch (error) {
      showSaveStatus("Could not save · check connection", "error");
    } finally {
      saveInFlight = false;
      if (pendingSave) saveNow();
    }
  }

  function scheduleSave() {
    clearTimeout(saveTimer);
    showSaveStatus("Saving…", "saving");
    saveTimer = setTimeout(saveNow, 450);
  }

  function createBrushPath(d, color, width) {
    const path = document.createElementNS(SVG_NS, "path");
    path.setAttribute("class", "brush-stroke");
    path.setAttribute("d", d);
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", color);
    path.setAttribute("stroke-width", width);
    path.setAttribute("stroke-linecap", "round");
    path.setAttribute("stroke-linejoin", "round");
    path.setAttribute("pointer-events", "stroke");
    return path;
  }

  function clientToSvg(event) {
    const point = new DOMPoint(event.clientX, event.clientY);
    const ctm = drawing.getScreenCTM();
    return ctm ? point.matrixTransform(ctm.inverse()) : point;
  }

  function pointsToPath(points) {
    if (!points.length) return "";
    if (points.length === 1) {
      const p = points[0];
      return `M ${p.x.toFixed(2)} ${p.y.toFixed(2)} L ${(p.x + 0.01).toFixed(2)} ${(p.y + 0.01).toFixed(2)}`;
    }

    let d = `M ${points[0].x.toFixed(2)} ${points[0].y.toFixed(2)}`;
    for (let i = 1; i < points.length; i++) {
      d += ` L ${points[i].x.toFixed(2)} ${points[i].y.toFixed(2)}`;
    }
    return d;
  }

  // Restore the exact saved colors and brush strokes.
  applyState(window.LUMI_INITIAL_STATE || {});
  if ((window.LUMI_INITIAL_STATE?.fills && Object.keys(window.LUMI_INITIAL_STATE.fills).length) ||
      (window.LUMI_INITIAL_STATE?.strokes && window.LUMI_INITIAL_STATE.strokes.length)) {
    showSaveStatus("Saved work restored ✓", "saved");
  }

  palette?.addEventListener("click", event => {
    const btn = event.target.closest(".color-dot");
    if (!btn) return;

    document.querySelectorAll(".color-dot").forEach(el => el.classList.remove("selected"));
    btn.classList.add("selected");
    selectedColor = btn.dataset.color;
  });

  document.querySelectorAll(".tool-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      tool = btn.dataset.tool;
      document.querySelectorAll(".tool-btn").forEach(el => el.classList.remove("active"));
      btn.classList.add("active");

      if (tool === "brush") drawing.classList.add("brush-mode");
      else drawing.classList.remove("brush-mode");

      scheduleSave();
    });
  });

  document.querySelectorAll(".size-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      brushSize = Number(btn.dataset.size) || 16;
      document.querySelectorAll(".size-btn").forEach(el => el.classList.remove("active"));
      btn.classList.add("active");
      tool = "brush";
      document.querySelectorAll(".tool-btn").forEach(el => {
        el.classList.toggle("active", el.dataset.tool === "brush");
      });
      drawing.classList.add("brush-mode");
    });
  });

  drawing.addEventListener("pointerdown", event => {
    const fillTarget = event.target.closest?.(".fillable");
    const strokeTarget = event.target.closest?.(".brush-stroke");

    if (tool === "fill" && fillTarget) {
      event.preventDefault();
      pushHistory();
      fillTarget.style.fill = selectedColor;
      scheduleSave();
      return;
    }

    if (tool === "eraser") {
      event.preventDefault();
      if (strokeTarget) {
        pushHistory();
        strokeTarget.remove();
        scheduleSave();
      } else if (fillTarget) {
        pushHistory();
        fillTarget.style.fill = "#FFFFFF";
        scheduleSave();
      }
      return;
    }

    if (tool !== "brush") return;

    event.preventDefault();
    pushHistory();
    isDrawing = true;
    drawing.setPointerCapture?.(event.pointerId);

    const p = clientToSvg(event);
    activeStrokePoints = [p];
    activeStroke = createBrushPath(pointsToPath(activeStrokePoints), selectedColor, brushSize);
    brushLayer.appendChild(activeStroke);
  });

  drawing.addEventListener("pointermove", event => {
    if (!isDrawing || tool !== "brush" || !activeStroke) return;
    event.preventDefault();

    const p = clientToSvg(event);
    const last = activeStrokePoints[activeStrokePoints.length - 1];

    // Avoid creating hundreds of almost identical points.
    if (last && Math.hypot(p.x - last.x, p.y - last.y) < 2) return;

    activeStrokePoints.push(p);
    activeStroke.setAttribute("d", pointsToPath(activeStrokePoints));
  });

  function endBrush(event) {
    if (!isDrawing) return;
    isDrawing = false;
    try { drawing.releasePointerCapture?.(event.pointerId); } catch (_) {}
    activeStroke = null;
    activeStrokePoints = [];
    scheduleSave();
  }

  drawing.addEventListener("pointerup", endBrush);
  drawing.addEventListener("pointercancel", endBrush);
  drawing.addEventListener("pointerleave", event => {
    if (isDrawing && event.buttons === 0) endBrush(event);
  });

  undoBtn?.addEventListener("click", () => {
    const last = history.pop();
    if (!last) return;
    applyState(last);
    scheduleSave();
  });

  resetBtn?.addEventListener("click", () => {
    pushHistory();
    fillables.forEach(el => el.style.fill = "#FFFFFF");
    brushLayer.innerHTML = "";
    scheduleSave();
  });

  finishBtn?.addEventListener("click", async () => {
    finishBtn.disabled = true;
    finishBtn.textContent = "Saving…";

    try {
      clearTimeout(saveTimer);
      await saveNow();

      const response = await fetch(`/api/complete/${window.LUMI_DRAWING_ID}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"}
      });
      const data = await response.json();

      if (!response.ok || !data.ok) {
        alert(data.message || "Could not save completion.");
        return;
      }

      successText.textContent = `${data.message} Your exact colors and brush painting were saved too.`;
      successModal.classList.remove("hidden");

      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("Kids Drawing Buddy", { body: data.message });
      }
    } catch (error) {
      alert("Could not save completion. Please try again.");
    } finally {
      finishBtn.disabled = false;
      finishBtn.textContent = "✓ Finish";
    }
  });

  // Try to save before leaving the page.
  window.addEventListener("pagehide", () => {
    const payload = JSON.stringify(getState());
    navigator.sendBeacon?.(
      `/api/progress/${window.LUMI_DRAWING_ID}`,
      new Blob([payload], {type: "application/json"})
    );
  });
})();
