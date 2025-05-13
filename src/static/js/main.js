document.addEventListener("DOMContentLoaded", () => {
  // Element selectors
  const integrationFormulaSelector = document.getElementById(
    "integration-formula-selector"
  );
  const functionExpressionInput = document.getElementById(
    "function-expression"
  );
  const formulaDescriptionDiv = document.getElementById("formula-description");
  const customFormulaNameInput = document.getElementById("custom-formula-name");
  const customFormulaNodesTextarea = document.getElementById(
    "custom-formula-nodes"
  );
  const calculationOutputDiv = document.getElementById("calculation-output");
  const startCalculationButton = document.getElementById("start-calculation");
  // const pauseResumeButton = document.getElementById("pause-resume-calculation");
  // const cancelCalculationButton = document.getElementById("cancel-calculation");
  const initializeButton = document.getElementById("initialize-calculation");

  const nodeColorInput = document.getElementById("node-color");
  const edgeColorInput = document.getElementById("edge-color");
  const fillColorInput = document.getElementById("fill-color");
  // const toggleAxesCheckbox = document.getElementById("toggle-axes");
  const plotAreaDiv = document.getElementById("plot-area");
  const drawNodeDistributionButton = document.getElementById(
    "draw-node-distribution"
  );
  const saveImageButton = document.getElementById("save-image");

  const vertex1xInput = document.getElementById("vertex1-x");
  const vertex1yInput = document.getElementById("vertex1-y");
  const vertex2xInput = document.getElementById("vertex2-x");
  const vertex2yInput = document.getElementById("vertex2-y");
  const vertex3xInput = document.getElementById("vertex3-x");
  const vertex3yInput = document.getElementById("vertex3-y");

  const downloadButton = document.getElementById("download-button");

  let triangleFormulas = {};

  function setDefaultVertices() {
    vertex1xInput.value = "0";
    vertex1yInput.value = "0";
    vertex2xInput.value = "1";
    vertex2yInput.value = "0";
    vertex3xInput.value = "0";
    vertex3yInput.value = "1";
    // console.log(
    //   "Default vertices set:",
    //   vertex1xInput.value,
    //   vertex1yInput.value,
    //   vertex2xInput.value,
    //   vertex2yInput.value,
    //   vertex3xInput.value,
    //   vertex3yInput.value
    // );
  }

  // --- Initialization and Event Binding ---
  setTimeout(setDefaultVertices, 100);
  // Load integration formulas
  fetch("/api/formulas") // Assuming a Flask route /api/formulas serves triangle_formula.json
    .then((response) => response.json())
    .then((data) => {
      triangleFormulas = data;
      populateFormulaSelector();
      updateFormulaDescription(); // Initial description update
    })
    .catch((error) => {
      console.error("Error loading integration formulas:", error);
      formulaDescriptionDiv.textContent = "Error loading formulas.";
    });

  function populateFormulaSelector() {
    integrationFormulaSelector.innerHTML = ""; // Clear existing options
    const orderedKeys = Object.keys(triangleFormulas).sort((a, b) => {
      if (!triangleFormulas[a] || !triangleFormulas[a].data) {
        return -1; // 如果 a 没有 data，则 a 排在前面
      }
      if (!triangleFormulas[b] || !triangleFormulas[b].data) {
        return 1; // 如果 b 没有 data，则 b 排在后面
      }
      return triangleFormulas[a].data.length - triangleFormulas[b].data.length;
    });

    orderedKeys.forEach((key) => {
      const option = document.createElement("option");
      option.value = key;
      option.textContent = triangleFormulas[key].name; // Use description for readability
      integrationFormulaSelector.appendChild(option);
    });
    // Object.keys(triangleFormulas).forEach((key) => {
    //   const option = document.createElement("option");
    //   option.value = key;
    //   option.textContent = triangleFormulas[key].name;
    //   integrationFormulaSelector.appendChild(option);
    // });
    const customOption = document.createElement("option");
    customOption.value = "custom";
    customOption.textContent = "自定义";
    integrationFormulaSelector.appendChild(customOption);
    toggleCustomFormulaFields(); // Initial state
  }

  function toggleCustomFormulaFields() {
    const isCustom = integrationFormulaSelector.value === "custom";
    customFormulaNameInput.disabled = !isCustom;
    customFormulaNodesTextarea.disabled = !isCustom;
    if (!isCustom) {
      customFormulaNameInput.value = "";
      customFormulaNodesTextarea.value = "";
    }
  }

  function updateFormulaDescription() {
    const selectedKey = integrationFormulaSelector.value;
    if (
      selectedKey &&
      selectedKey !== "custom" &&
      triangleFormulas[selectedKey]
    ) {
      formulaDescriptionDiv.innerHTML = ""; // Clear previous
      // Basic display, can be enhanced with KaTeX if description contains LaTeX
      const description =
        triangleFormulas[selectedKey].description || "暂无说明";
      // If description is LaTeX, render it. For now, just text.
      // Check if KaTeX is available before trying to use it
      if (typeof katex !== "undefined") {
        try {
          katex.render(description, formulaDescriptionDiv, {
            throwOnError: false,
          });
        } catch (e) {
          console.error("KaTeX rendering error:", e);
          formulaDescriptionDiv.textContent = description; // Fallback to text
        }
      } else {
        formulaDescriptionDiv.textContent = description;
      }
    } else if (selectedKey === "custom") {
      formulaDescriptionDiv.textContent = "用户自定义积分公式。";
    } else {
      formulaDescriptionDiv.textContent = "请选择一个积分公式。";
    }
    toggleCustomFormulaFields();
  }

  // Event Listeners
  integrationFormulaSelector.addEventListener(
    "change",
    updateFormulaDescription
  );

  initializeButton.addEventListener("click", () => {
    // Reset all inputs to default values
    functionExpressionInput.value = "";
    integrationFormulaSelector.selectedIndex = 0; // Select the first formula
    updateFormulaDescription(); // This will also handle custom fields
    customFormulaNameInput.value = "";
    customFormulaNodesTextarea.value = "";
    calculationOutputDiv.innerHTML = "";

    nodeColorInput.value = "red";
    edgeColorInput.value = "black";
    fillColorInput.value = "lightblue";
    // toggleAxesCheckbox.checked = true;

    // vertex1xInput.value = "";
    // vertex1yInput.value = "";
    // vertex2xInput.value = "";
    // vertex2yInput.value = "";
    // vertex3xInput.value = "";
    // vertex3yInput.value = "";
    setDefaultVertices();

    plotAreaDiv.innerHTML = "<p>绘图区</p>"; // Reset plot area

    // Reset button states
    startCalculationButton.disabled = false;
    // pauseResumeButton.disabled = true;
    // cancelCalculationButton.disabled = true;
    saveImageButton.disabled = true;
    drawNodeDistributionButton.disabled = false;

    console.log("Form initialized");
  });

  drawNodeDistributionButton.addEventListener("click", async () => {
    const vertices = [
      {
        x: parseFloat(vertex1xInput.value),
        y: parseFloat(vertex1yInput.value),
      },
      {
        x: parseFloat(vertex2xInput.value),
        y: parseFloat(vertex2yInput.value),
      },
      {
        x: parseFloat(vertex3xInput.value),
        y: parseFloat(vertex3yInput.value),
      },
    ];

    if (vertices.some((v) => isNaN(v.x) || isNaN(v.y))) {
      alert("请输入所有三个有效的顶点坐标。");
      return;
    }

    let nodes, weights;
    if (integrationFormulaSelector.value === "custom") {
      try {
        const customData = JSON.parse(
          customFormulaNodesTextarea.value.replace(/'/g, '"')
        ); // Allow single quotes
        if (
          !Array.isArray(customData) ||
          !customData.every(
            (row) =>
              Array.isArray(row) &&
              row.length === 3 &&
              typeof row[0] === "number" &&
              typeof row[1] === "number" &&
              typeof row[2] === "number"
          )
        ) {
          alert("自定义节点及权重格式错误。应为 n x 3 的数字数组。");
          return;
        }
        nodes = customData.map((row) => [row[0], row[1]]);
        weights = customData.map((row) => row[2]);
      } catch (e) {
        alert("自定义节点及权重解析错误。请检查格式。");
        console.error("Error parsing custom nodes/weights:", e);
        return;
      }
    } else {
      const selectedFormula =
        triangleFormulas[integrationFormulaSelector.value];
      if (
        !selectedFormula ||
        !selectedFormula.nodes ||
        !selectedFormula.weights
      ) {
        alert("选择的预设公式缺少节点或权重信息。");
        return;
      }
      nodes = selectedFormula.nodes;
      weights = selectedFormula.weights; // Though weights are not directly used for plotting nodes, they are part of the formula data
    }

    const plotData = {
      vertices: vertices,
      nodes: nodes,
      node_color: nodeColorInput.value,
      edge_color: edgeColorInput.value,
      fill_color: fillColorInput.value,
      // show_axes: toggleAxesCheckbox.checked,
    };

    plotAreaDiv.innerHTML = "<p>正在绘图...</p>";
    saveImageButton.disabled = true;

    try {
      const response = await fetch("/api/plot", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(plotData),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `绘图失败: ${response.statusText}`);
      }
      const result = await response.json();
      if (result.image_data) {
        plotAreaDiv.innerHTML = `<img src="data:image/png;base64,${result.image_data}" alt="积分节点分布图" style="max-width: 100%; max-height: 100%;">`;
        saveImageButton.disabled = false;
      } else {
        plotAreaDiv.textContent = "绘图区 (未能获取图像)";
      }
    } catch (error) {
      console.error("Error plotting:", error);
      plotAreaDiv.textContent = `绘图错误: ${error.message}`;
      saveImageButton.disabled = true;
    }
  });

  startCalculationButton.addEventListener("click", async () => {
    const funcStr = functionExpressionInput.value;
    if (!funcStr.trim()) {
      alert("请输入函数表达式 f(x,y)。");
      return;
    }

    const vertices = [
      {
        x: parseFloat(vertex1xInput.value),
        y: parseFloat(vertex1yInput.value),
      },
      {
        x: parseFloat(vertex2xInput.value),
        y: parseFloat(vertex2yInput.value),
      },
      {
        x: parseFloat(vertex3xInput.value),
        y: parseFloat(vertex3yInput.value),
      },
    ];

    if (vertices.some((v) => isNaN(v.x) || isNaN(v.y))) {
      alert("请输入所有三个有效的顶点坐标。");
      return;
    }

    let nodes, weights, formulaName;
    if (integrationFormulaSelector.value === "custom") {
      formulaName = customFormulaNameInput.value.trim() || "custom";
      try {
        // Assuming Python-like or JS-like array string: [[x1,y1,w1], [x2,y2,w2]]
        // A more robust parser might be needed for varied inputs.
        // For now, expect a JSON-parsable array of arrays.
        const customData = JSON.parse(
          customFormulaNodesTextarea.value.replace(/'/g, '"')
        );
        if (
          !Array.isArray(customData) ||
          !customData.every(
            (row) =>
              Array.isArray(row) &&
              row.length === 3 &&
              typeof row[0] === "number" &&
              typeof row[1] === "number" &&
              typeof row[2] === "number"
          )
        ) {
          alert("自定义节点及权重格式错误。应为 n x 3 的数字数组。");
          return;
        }
        nodes = customData.map((row) => [row[0], row[1]]);
        weights = customData.map((row) => row[2]);
      } catch (e) {
        alert(
          "自定义节点及权重解析错误。请检查格式 (应为JSON数组，例如 [[0.5,0,0.333],[0,0.5,0.333],[0.5,0.5,0.333]])。"
        );
        console.error("Error parsing custom nodes/weights:", e);
        return;
      }
    } else {
      const selectedFormulaKey = integrationFormulaSelector.value;
      const selectedFormula = triangleFormulas[selectedFormulaKey];
      if (
        !selectedFormula ||
        !selectedFormula.nodes ||
        !selectedFormula.weights
      ) {
        alert("选择的预设公式缺少节点或权重信息。");
        return;
      }
      nodes = selectedFormula.nodes;
      weights = selectedFormula.weights;
      formulaName = selectedFormula.name;
    }

    const calculationData = {
      func_str: funcStr,
      nodes: nodes,
      weights: weights,
      vertices: vertices, // Vertices might be needed if the formula is for a standard triangle and needs scaling/transformation
    };

    calculationOutputDiv.textContent = "正在计算...";
    startCalculationButton.disabled = true;
    // cancelCalculationButton.disabled = false; // Enable cancel
    // pauseResumeButton logic to be added if supported

    try {
      const response = await fetch("/api/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(calculationData),
      });

      const result = await response.json(); // Try to parse JSON regardless of ok status for error messages

      if (!response.ok) {
        throw new Error(result.error || `计算失败: ${response.statusText}`);
      }

      calculationOutputDiv.textContent = `计算结果 (${formulaName}): ${result.result}`;
    } catch (error) {
      console.error("Error calculating:", error);
      calculationOutputDiv.textContent = `计算错误: ${error.message}`;
    } finally {
      startCalculationButton.disabled = false;
      // cancelCalculationButton.disabled = true;
    }
  });

  saveImageButton.addEventListener("click", () => {
    const imgElement = plotAreaDiv.querySelector("img");
    if (imgElement && imgElement.src) {
      const link = document.createElement("a");
      link.href = imgElement.src;
      link.download = "triangle_integration_plot.png";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      alert("没有可保存的图像。");
    }
  });

  // Initial call to set up the formula selector and description
  // This is now handled by the fetch().then() block for formulas

  // Placeholder for LaTeX rendering of the function input (if desired)
  // functionExpressionInput.addEventListener('input', () => {
  //     const latexPreview = document.getElementById('latex-preview'); // Assuming such an element exists
  //     if (latexPreview && typeof katex !== 'undefined') {
  //         try {
  //             katex.render(functionExpressionInput.value, latexPreview, { throwOnError: false });
  //         } catch (e) {
  //             latexPreview.textContent = 'LaTeX 语法错误';
  //         }
  //     }
  // });

  downloadButton.addEventListener("click", () => {
    const link = document.createElement("a");
    link.href =
      "https://hsmkhexo.s3.ap-northeast-1.amazonaws.com/other/triangle_formula.json";
    link.download = "triangle_formula.json"; // 下载时保存的文件名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  console.log("Triangle Integration Demo UI Initialized.");
});
