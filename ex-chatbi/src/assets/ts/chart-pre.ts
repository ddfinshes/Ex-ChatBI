import * as d3 from 'd3';
// LLM需要给出横轴、纵轴、变化数据、标题
// X轴：类别；
// Y轴：数值
// Title: 
// legend: x轴，y轴标签
// Tooltip
export function chart(vis_data: any) {
  // 获取容器
  
  const container = document.getElementById("vis-tag");
  console.log(container);
  if (!container) return;

  // 清空现有内容
  d3.select(`#vis-tag`).selectAll("*").remove();

  // 设置图表尺寸
  const width = 600;
  const height = 400;
  const margin = { top: 25, right: 30, bottom: 40, left: 50 };

  // 创建SVG容器
  const svg = d3
    .select(`#vis-tag`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  // 根据 vis_tag 判断图表类型
  switch (vis_data["vis_tag"]) {
    case "bar-chart":
      drawBarChart(svg, vis_data, width, height, margin);
      break;
    case "line-chart":
      drawLineChart(svg, vis_data, width, height, margin);
      break;
    case "pie-chart":
      drawPieChart(svg, vis_data, width, height, margin);
      break;
    default:
      console.error("Unsupported vis_tag:", vis_data["vis_tag"]);
  }
}

// 绘制柱状图
function drawBarChart(svg: any, vis_data: any, width: number, height: number, margin: any) {
  // 数据准备
  const data = vis_data["x"].map((x: string, i: number) => ({
    xvalue: x,
    yvalue: vis_data["y"][i],
  }));

  // X轴比例尺
  const x = d3
    .scaleBand()
    .domain(vis_data['x'].map((d: any) => d))
    .range([margin.left, width - margin.right])
    .padding(0.1);
  console.log('bandwidth', x.bandwidth());

  // Y轴比例尺（支持负值）
  const y = d3
    .scaleLinear()
    .domain([Math.min(0, d3.min(vis_data['y'], (d: any) => d)), d3.max(vis_data['y'], (d: any) => Math.abs(d))])
    .nice()
    .range([height - margin.bottom, margin.top]);

  // 绘制柱子
  svg
    .selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", (d: any) => x(d.xvalue))
    .attr("y", (d: any) => (d.yvalue >= 0 ? y(d.yvalue) : y(0))) // 正值从零向上，负值从零向下
    .attr("width", x.bandwidth())
    .attr("height", (d: any) => Math.abs(y(d.yvalue) - y(0))) // 高度为绝对值
    .attr("fill", "steelblue")
    .on("mouseover", function (event: any, d: any) {
      // 工具提示
      d3.select(this).attr("fill", "orange");
      svg
        .append("text")
        .attr("id", "tooltip")
        .attr("x", x(d.xvalue) + x.bandwidth() / 2)
        .attr("y", y(d.yvalue) - 10)
        .attr("text-anchor", "middle")
        .attr("fill", "black")
        .call((text: any) => {
          text
            .append("tspan")
            .attr("x", x(d.xvalue) + x.bandwidth() / 2) // 保持水平居中
            .attr("dy", "-1em")                        // 首行向上偏移
            .text(`${d.xvalue}: ${d.yvalue}`);           // 第一行
          text
            .append("tspan")
            .attr("x", x(d.xvalue) + x.bandwidth() / 2) // 保持水平居中
            .attr("dy", "1.2em")                       // 第二行向下偏移
            .text(vis_data["tooltip"]);                // 第二行
        });
    })
    .on("mouseout", function () {
      d3.select(this).attr("fill", "steelblue");
      d3.select("#tooltip").remove();
    });

  // 添加X轴
  // svg
  //   .append("g")
  //   .attr("transform", `translate(0, ${y(0)})`) // X轴放在零点位置
  //   .call(d3.axisBottom(x))
  //   .append("text")
  //   .attr("x", width / 2)
  //   .attr("y", margin.bottom - 5)
  //   .attr("fill", "black")
  //   .attr("text-anchor", "end")
  //   .text(vis_data["x-legend"]);
  svg
  .append("g")
  .attr("transform", `translate(0, ${y(0)})`) // X轴放在零点位置
  .call(d3.axisBottom(x))
  .append("text")
  .attr("x", width - margin.right) // 将 x 设置为最右端
  .attr("y", margin.bottom - 5)    // 保持垂直位置不变
  .attr("fill", "black")
  .attr("text-anchor", "end")      // 文本右对齐
  .text(vis_data["x-legend"]);

  // 添加Y轴
  // svg
  //   .append("g")
  //   .attr("transform", `translate(${margin.left}, 0)`)
  //   .call(d3.axisLeft(y))
  //   .append("text")
  //   .attr("x", -height / 2)
  //   .attr("y", -margin.left + 15)
  //   .attr("fill", "black")
  //   .attr("text-anchor", "middle")
  //   .attr("transform", "rotate(-90)")
  //   .text(vis_data["y-legend"]);
  svg
  .append("g")
  .attr("transform", `translate(${margin.left}, 0)`)
  .call(d3.axisLeft(y))
  .append("text")
  .attr("x", -margin.top)          // 将标签移到 Y 轴顶部
  .attr("y", -margin.left + 15)    // 保持水平偏移不变
  .attr("fill", "black")
  .attr("text-anchor", "start")    // 文本顶部对齐
  .attr("transform", "rotate(-90)") // 保持旋转
  .text(vis_data["y-legend"]);
  // 添加标题
  svg
    .append("text")
    .attr("x", width / 2)
    .attr("y", margin.top)
    .attr("text-anchor", "middle")
    .attr("fill", "black")
    .text(vis_data["title"]);
}

// 占位：折线图实现（未完成）
function drawLineChart(svg: any, vis_data: any, width: number, height: number, margin: any) {
  console.log("Line chart not implemented yet.");
}

// 占位：饼图实现（未完成）
function drawPieChart(svg: any, vis_data: any, width: number, height: number, margin: any) {
  console.log("Pie chart not implemented yet.");
}