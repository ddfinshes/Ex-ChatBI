<template>
  <div>
    <!-- 添加 Header -->
    <div class="header">View C</div>
    <!-- 原有的 chart 容器 -->
    <div ref="chart"></div>
  </div>
  
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import * as d3 from "d3";

const chart = ref(null);
const nodes = ref([]);
const nodeCards = ref([]);

const res = {
  content: [
    {
        "created_virtual_table": "False",
        "sql_content": [
        {
            "keywords": "Select",
            "scratched_content": [
            {"column_name": "month_id", "column_processing": ""},
            {"column_name": "Current_Month_Effi", "column_processing": "TO_CHAR (Current_Month_Effi, 'FM999,999,999.00') AS Current_Month_Effi"},
            {"column_name": "Previous_Month_Effi", "column_processing": "TO_CHAR (Previous_Month_Effi, 'FM999,999,999.00') AS Previous_Month_Effi"},
            {"column_name": "Growth_Percentage", "column_processing": "TO_CHAR (Growth_Percentage, 'FM999,999,999.00') || '%' AS Growth_Percentage"}
            ]
        },
        {
            "keywords": "From",
            "scratched_content": [
            {"table_name": "Monthly_Growth", "is_virtual_table": "True"}
            ]
        },
        {
            "keywords": "Join",
            "scratched_content": [
            {"content": "JOIN Effi_Comparison p ON c.month_id = TO_CHAR (DATEADD (month, 1, TO_DATE (p.month_id, 'YYYYMM')), 'YYYYMM')"}
            ]
        },
        {
            "keywords": "Where",
            "scratched_content": [
            {"content": "c.month_id = '202410'"}
            ]
        }
        ]
    },
    {
        "created_virtual_table": "True",
        "virtual_table_name": "Monthly_Growth",
        "sql_content": [
        {
            "keywords": "Select",
            "scratched_content": [
            {"column_name": "c.month_id", "column_processing": ""},
            {"column_name": "Current_Month_Effi", "column_processing": "c.Avg_effi AS Current_Month_Effi"},
            {"column_name": "Previous_Month_Effi", "column_processing": "p.Avg_effi AS Previous_Month_Effi"},
            {"column_name": "Growth_Percentage", "column_processing": "(c.Avg_effi / p.Avg_effi - 1) * 100 AS Growth_Percentage"}
            ]
        },
        {
            "keywords": "From",
            "scratched_content": [
            {"table_name": "Effi_Comparison c", "is_virtual_table": "True"}
            ]
        },
        {
            "keywords": "Join",
            "scratched_content": [
            {"content": "JOIN Effi_Comparison p ON c.month_id = TO_CHAR (DATEADD (month, 1, TO_DATE (p.month_id, 'YYYYMM')), 'YYYYMM')"}
            ]
        },
        {
            "keywords": "Where",
            "scratched_content": [
            {"content": "c.month_id = '202410'"}
            ]
        }
        ]
    },
    {
        "created_virtual_table": "True",
        "virtual_table_name": "Effi_Comparison",
        "sql_content": [
        {
            "keywords": "Select",
            "scratched_content": [
            {"column_name": "month_id", "column_processing": ""},
            {"column_name": "Avg_effi", "column_processing": "AVG(effi) AS Avg_effi"}
            ]
        },
        {
            "keywords": "From",
            "scratched_content": [
            {"table_name": "Store_effi", "is_virtual_table": "True"}
            ]
        },
        {
            "keywords": "Group By",
            "scratched_content": [
            {"content": "month_id"}
            ]
        }
        ]
    },
    {
        "created_virtual_table": "True",
        "virtual_table_name": "Store_effi",
        "sql_content": [
        {
            "keywords": "Select",
            "scratched_content": [
            {"column_name": "country", "column_processing": ""},
            {"column_name": "channel", "column_processing": ""},
            {"column_name": "store_type", "column_processing": ""},
            {"column_name": "area", "column_processing": ""},
            {
                "column_name": "effi",
                "column_processing": "CASE WHEN (COALESCE(area, '') = '' OR CAST(area AS DECIMAL(18, 2)) = 0) THEN 0 ELSE AVG(COALESCE(amt_usd_notax, 0)) * 365 / CAST(area AS DECIMAL(18, 2)) * 10.7639104 END AS effi"
            },
            {"column_name": "month_id", "column_processing": ""}
            ]
        },
        {
            "keywords": "From",
            "scratched_content": [
            {"table_name": "dm_fact_sales_chatbi", "is_virtual_table": "False"}
            ]
        },
        {
            "keywords": "Where",
            "scratched_content": [
            {
                "content": "date_code <= '2024-10-31' AND country = 'Mainland' AND channel = 'O&O' AND store_type = 'BH' AND comp_flag = 'Y'"
            }
            ]
        },
        {
            "keywords": "Group By",
            "scratched_content": [
            {"content": "country, channel, store_type, store_code, area, month_id"}
            ]
        }
        ]
    }
    ]
};
// const res = {
//   content: [
//     {
//         "created_virtual_table": "False",
//         "sql_content": [
//         {
//             "keywords": "Select",
//             "scratched_content": [
//             {"column_name": "country", "column_processing": ""},
//             {"column_name": "sales_notax", "column_processing": "SUM(amt_notax) AS sales_notax"},
//             {"column_name": "sales_notax_LW", "column_processing": "SUM(lw_amt_notax) AS sales_notax_LW"},
//             {
//                 "column_name": "sales_notax_wow_per",
//                 "column_processing": " CASE WHEN SUM(COALESCE(lw_amt_notax, 0)) = 0 THEN 0 ELSE SUM(amt_notax) / SUM(COALESCE(lw_amt_notax, 0)) - 1 END AS sales_notax_wow_per"
//             },
//             {"column_name": "traffic", "column_processing": "SUM(traffic) AS traffic"},
//             {"column_name": "traffic_LW", "column_processing": "SUM(lw_traffic) AS traffic_LW"},
//             {
//                 "column_name": "traffic_wow_per",
//                 "column_processing": "CASE WHEN SUM(COALESCE(lw_traffic, 0)) = 0 THEN 0 ELSE SUM(traffic) / SUM(COALESCE(lw_traffic, 0)) - 1 END AS traffic_wow_per"
//             }
//             ]
//         },
//         {
//             "keywords": "From",
//             "scratched_content": [
//             {"table_name": "dm_fact_sales_chatbi", "is_virtual_table": "False"}
//             ]
//         },
//         {
//             "keywords": "Where",
//             "scratched_content": [
//             {"content": "date_code BETWEEN '2025-02-23' AND '2025-02-24'"}
//             ]
//         },
//         {
//             "keywords": "Group By",
//             "scratched_content": [
//             {"content": "country"}
//             ]
//         },
//         {
//             "keywords": "Having",
//             "scratched_content": [
//             {"content": "sales_notax_wow_per < 0"}
//             ]
//         },
//         {
//             "keywords": "Order By",
//             "scratched_content": [
//             {"content": "sales_notax_wow_per"}
//             ]
//         }
//         ]
//     }
//     ]
// };

const SQL_KEYWORDS = [
  "Select",
  "From",
  "Where",
  "Group By",
  "Join",
  "Having",
  "Order By",
];

// onMounted(() => {
//   const data = transformToTree(res);
//   const root = d3.hierarchy(data);
//   const width = 1000;
//   const maxDepth = root.height; // 获取树的最大深度
//   const height = Math.max(800, maxDepth * 100); // 每层预留足够空间

//   // 创建 SVG 并启用缩放
//   const svg = d3
//     .select(chart.value)
//     .append("svg")
//     .attr("width", width)
//     .attr("height", height)
//     .call(
//       d3
//         .zoom()
//         .scaleExtent([0.1, 4])
//         .on("zoom", (event) => {
//           g.attr("transform", event.transform);
//         })
//     );

//   const g = svg.append("g").attr("transform", "translate(50, 50)");

//   const treeLayout = d3
//     .tree()
//     .size([height - 10, width - 10])
//     .separation((a, b) => {
//     // ⭐️ 动态计算节点间距
//     const minHorizontalGap = 1000; // 最小水平间距
//     const nodeWidth = 80; // 你的节点实际宽度

//     // 计算兄弟节点之间的最小间距系数
//     return (nodeWidth + minHorizontalGap) / nodeWidth;
//   });

//   // 更新函数：根据当前层次状态渲染树
//   function update() {
//     treeLayout(root);
//     const links = root.links();
//     const nodes = root.descendants();

//     // 更新连线
//     const linkSelection = g.selectAll(".link").data(links, (d) => d.target);
//     const linkEnter = linkSelection
//       .enter()
//       .append("path")
//       .attr("class", "link")
//       .attr("fill", "none")
//       .attr("stroke", "#ccc");
//     linkSelection.merge(linkEnter).attr(
//       "d",
//       d3
//         .linkVertical()
//         .x((d) => d.x)
//         .y((d) => d.y)
//     );
//     linkSelection.exit().remove();

//     // 更新节点
//     const nodeSelection = g.selectAll(".node").data(nodes, (d) => d);
//     const nodeEnter = nodeSelection.enter().append("g").attr("class", "node");

//     nodeEnter.each(function (d) {
//       const isKeyword = SQL_KEYWORDS.includes(d.data.name);
//       const selection = d3.select(this);

//       if (isKeyword) {
//         selection
//           .append("circle")
//           .attr("r", 20)
//           .attr("fill", (d) =>
//             d.data.name === "Select"
//               ? "#ff9999"
//               : d.data.name === "From"
//               ? "#99ccff"
//               : "#99ff99"
//           )
//           .style("cursor", "pointer");
//         selection
//           .append("text")
//           .attr("dy", ".35em")
//           .attr("text-anchor", "middle")
//           .text(d.data.name)
//           .style("font-size", "12px")
//           .style("pointer-events", "none");
//       } else {
//         // const textWidth = d.data.name.length*8 + 10;
//         // selection
//         //   .append("rect")
//         //   .attr("x", -textWidth / 2)
//         //   .attr("y", -15)
//         //   .attr("width", textWidth)
//         //   .attr("height", 30)
//         //   .attr("fill", "#f0f0f0")
//         //   .attr("stroke", "#999")
//         //   .attr("rx", 5)
//         //   .style("cursor", "pointer");
//         // 添加固定宽度的矩形（宽度60px）
//         const textContainer = selection
//           .append("g")
//           .attr("transform", "translate(-30, -15)");
//         const textWidth = 80;
//         const containerHeight = 60;

//         autoWrapText(textContainer, d.data.name, textWidth, containerHeight);
//       }
//     });

//     const nodeUpdate = nodeSelection.merge(nodeEnter);
//     nodeUpdate.attr("transform", (d) => `translate(${d.x},${d.y})`);
//     nodeUpdate.on("click", click);
//     nodeSelection.exit().remove();
//   }

//   // 点击事件：切换节点的展开/关闭状态
//   function click(event, d) {
//     if (d.children) {
//       // 收起节点
//       d._children = d.children;
//       d.children = null;
//     } else if (d._children) {
//       // 展开节点
//       d.children = d._children;
//       d._children = null;
//     }

//     update();
//   }

//   // 自动换行函数（使用foreignObject+div实现）
//   function autoWrapText(container, text, width, containerHeight) {
//     const fontSize = 12; // 保持与原字体大小一致
//     const lineHeight = 1.1; // 保持与原来一致的行高比例

//     // 创建foreignObject容器
//     const fo = container
//       .append("foreignObject")
//       .attr("x", 0)
//       .attr("y", 0)
//       .attr("width", width)
//       .attr("height", 0); // 初始高度设为0，后面动态计算

//     // 创建HTML div元素
//     const div = fo
//       .append("xhtml:div")
//       .style("font-size", `${fontSize}px`)
//       .style("width", `${width}px`)
//       .style("white-space", "pre-wrap") // 允许自动换行
//       .style("word-wrap", "break-word") // 允许单词内断行
//       .style("line-height", lineHeight) // 设置行高
//       .style("margin", "0")
//       .style("padding", "10px") // 内边距
//       .style("background-color", "#f0f0f0") // 背景颜色
//       .style("border", "1px solid #ccc") // 边框
//       .style("border-radius", "5px") // 圆角边框
//       .style("box-shadow", "2px 2px 5px rgba(0, 0, 0, 0.1)") // 阴影
//       .style("color", "#333") // 文本颜色
//       .style("overflow", "hidden") // 防止内容溢出
//       .text(text);

//     // 获取实际渲染高度
//     const divNode = div.node();
//     const contentHeight = divNode.scrollHeight;

//     // 更新foreignObject尺寸
//     fo.attr("height", contentHeight)
//       // 垂直居中计算：y = (容器总高度 - 内容高度)/2
//       .attr("y", (containerHeight - contentHeight) / 2);
//   }
//   // 初始渲染
//   update();
// });

// function transformToTree(data) {
//   return {
//     name: "SQL Queries",
//     children: data.content.map((item) => ({
//       name: item.virtual_table_name || "Main Query",
//       children: item.sql_content.map((sql) => ({
//         name: sql.keywords,
//         children: sql.scratched_content.map((content) => {
//           if (content.sub_select === "True") {
//             return {
//               name: content.column_name || "Subquery",
//               children: content.sub_scratched_content.map((sub) => ({
//                 name: sub.keywords,
//                 children: sub.scratched_content.map((subContent) => ({
//                   name:
//                     subContent.column_name ||
//                     subContent.table_name ||
//                     subContent.content,
//                 })),
//               })),
//             };
//           }
//           return {
//             name: content.column_name || content.table_name || content.content,
//           };
//         }),
//       })),
//     })),
//   };
// }

// **1. 数据转换：转换成树形结构**
function transformToTree(data) {
  const root = { name: "Main Query", children: [] };

  if (data.content[0].created_virtual_table === "False") {
    data.content[0].sql_content.forEach((section) => {
      const node = { name: section.keywords, children: [] };

      if (section.scratched_content) {
        section.scratched_content.forEach((item) => {
          if (item.column_name) {
            // 创建 column_name 节点，并添加 column_processing 作为其子节点
            const columnNode = { 
              name: item.column_name, 
              children: item.column_processing ? [{ name: item.column_processing }] : [] 
            };
            node.children.push(columnNode);
          } else if (item.table_name) {
            // table_name 节点保持不变
            node.children.push({ name: item.table_name });
          }
          else if (item.content) {
            // table_name 节点保持不变
            node.children.push({ name: item.content });
          }
        });
      }

      root.children.push(node);
    });
  }

  return root;
}

onMounted(() => {
  const data = transformToTree(res);
  const root = d3.hierarchy(data);

  const width = 1205;
  const height = 600;
  const rectHeight = 40; // 矩形高度
  const padding = 20; // 矩形两侧的额外间距

  // 创建 SVG 画布
  const svgContainer = d3
    .select(chart.value)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const svg = svgContainer.append("g").attr("transform", "translate(50,50)");

  // 添加缩放功能
  const zoom = d3.zoom().scaleExtent([0.5, 2]).on("zoom", (event) => {
    svg.attr("transform", event.transform);
  });
  svgContainer.call(zoom);

  // 初始树布局
  let treeHeight = height - 100; // 初始高度
  const treeWidth = width - 200;
  const treeLayout = d3.tree().size([treeHeight, treeWidth]);

  treeLayout(root);

  // **绘制连接线**
  svg
    .selectAll("path.link")
    .data(root.links().filter((d) => d.target.depth < 2)) // 排除 depth=2 的目标节点
    .enter()
    .append("path")
    .attr("class", "table-link")
    .attr("fill", "none")
    .attr("stroke", "#aaa")
    .attr("stroke-width", 2)
    .attr("d", (d) => `M${d.source.y + 50},${d.source.x} L${d.target.y - 50},${d.target.x}`);

  // **绘制节点**
  const nodes = svg
    .selectAll("g.node")
    .data(root.descendants().filter((d) => d.depth < 2)) // 排除 depth=2
    .enter()
    .append("g")
    .attr("transform", (d) => `translate(${d.y},${d.x})`);

  // **添加文本**
  const texts = nodes
    .append("text")
    .attr("dy", 5)
    .attr("text-anchor", "middle")
    .attr("fill", "black")
    .style("font-size", "14px")
    .text((d) => d.data.name);

  // **计算文本宽度，动态调整矩形**
  texts.each(function (d) {
    const textWidth = this.getBBox().width + padding * 2;
    d.rectWidth = textWidth;
  });

  // **绘制矩形**
  nodes
    .insert("rect", "text")
    .attr("x", (d) => -d.rectWidth / 2)
    .attr("y", -rectHeight / 2)
    .attr("width", (d) => d.rectWidth)
    .attr("height", rectHeight)
    .attr("rx", 8)
    .attr("ry", 8)
    .attr("fill", (d) => (d.depth === 0 || d.depth === 1 ? "#B0B0B0" : "#4CAF50")) // 根节点和第一层灰色
    .attr("stroke", "#333");

  // **处理表格样式的节点**
  const tableWidth = 250; // 表格宽度
  const rowHeight = 40; // 每行高度
  const headerHeight = 50; // 表头高度
  const tablePadding = 10; // 表格内边距
  const tableOffset = 300; // 表格相对于父节点的水平偏移量
  const fixedTableWidth = 250;

  // 筛选所有 depth=1 节点（第二层节点）
  const level1Nodes = root.descendants().filter((d) => d.depth === 1);

  // 筛选 Select 和 From 的子节点
  const selectNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "Select");
  const fromNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "From");

  // 计算表格总高度
  const selectHeight = headerHeight + selectNodes.length * rowHeight + tablePadding * 2;
  const fromHeight = headerHeight + fromNodes.length * rowHeight + tablePadding * 2;

  // 存储所有表格的边界框，用于检测重叠
  const tableBounds = [];

  // 处理 Select 表格
  if (selectNodes.length > 0) {
    const selectParent = selectNodes[0].parent;
    const selectTableX = selectParent.y + tableOffset; // 表格在 Select 右侧
    const selectTableY = selectParent.x - selectHeight / 2; // 表格顶部对齐

    const selectGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${selectTableX},${selectTableY})`);
    // 绘制 Column Name 表头
    selectGroup
      .append("rect")
      .attr("x", -fixedTableWidth / 2)
      .attr("y", 0)
      .attr("width", fixedTableWidth)
      .attr("height", headerHeight)
      .attr("fill", "#FFD700")
      .attr("stroke", "#333");

    selectGroup
      .append("text")
      .attr("x", 0)
      .attr("y", headerHeight / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("fill", "black")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Column Name");

    // 绘制 Column Name 表格行
    let currentYOffset = headerHeight; // 动态计算每一行的 Y 偏移
    selectNodes.forEach((d, i) => {
      const textContent = d.data.name || d.data.column_name;
      const textElement = selectGroup
        .append("text")
        .attr("x", 0)
        .attr("y", currentYOffset + rowHeight / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", "middle")
        .attr("fill", "#333")
        .style("font-size", "14px")
        .text(textContent);

      // 检查文本宽度并换行
      const textWidth = textElement.node().getBBox().width;
      let adjustedHeight = rowHeight;
      if (textWidth > fixedTableWidth - 20) { // 留 20px padding
        textElement
          .text("") // 清空单行文本
          .selectAll("tspan")
          .data(wrapText(textContent, fixedTableWidth - 20))
          .enter()
          .append("tspan")
          .attr("x", 0)
          .attr("dy", (t, j) => j === 0 ? "0.35em" : "1.2em")
          .text((t) => t);

        const lineCount = wrapText(textContent, fixedTableWidth - 20).length;
        adjustedHeight = rowHeight * lineCount; // 根据行数调整高度
      }

      selectGroup
        .insert("rect", "text")
        .attr("x", -fixedTableWidth / 2)
        .attr("y", currentYOffset)
        .attr("width", fixedTableWidth)
        .attr("height", adjustedHeight)
        .attr("fill", "#FFFFFF")
        .attr("stroke", "#333");

      // 更新节点的坐标
      d.y = selectTableX;
      d.x = selectTableY + currentYOffset + adjustedHeight / 2;

      currentYOffset += adjustedHeight; // 更新下一行的偏移
    });

    // 绘制从 Select 到每个 column_name 的连接线
    selectNodes.forEach((d) => {
      svg
        .append("path")
        .attr("fill", "none")
        .attr("class", "table-link")
        .attr("stroke", "#aaa")
        .attr("stroke-width", 2)
        .attr("stroke-opacity", 0.5)
        .attr("d", `M${selectParent.y + 50},${selectParent.x} L${d.y - 50},${d.x}`);
    });

    // 处理 Column Processing 表格
    const processingTableX = selectTableX + fixedTableWidth + 100;
    const processingTableY = selectTableY - 50;
    const processingGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${processingTableX},${processingTableY})`);

    // 绘制 Column Processing 表头
    processingGroup
      .append("rect")
      .attr("x", -fixedTableWidth / 2)
      .attr("y", 0)
      .attr("width", fixedTableWidth)
      .attr("height", headerHeight)
      .attr("fill", "#87CEEB")
      .attr("stroke", "#333");

    processingGroup
      .append("text")
      .attr("x", 0)
      .attr("y", headerHeight / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("fill", "black")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Column Processing");

    // 绘制 Column Processing 表格行
    currentYOffset = headerHeight; // 重置 Y 偏移
    selectNodes.forEach((d, i) => {
      const processingText = d.data.children && d.data.children.length > 0 ? d.data.children[0].name : "";
      const textElement = processingGroup
        .append("text")
        .attr("x", 0)
        .attr("y", currentYOffset + rowHeight / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", "middle")
        .attr("fill", "#333")
        .style("font-size", "14px")
        .text(processingText);

      // 检查文本宽度并换行
      const textWidth = textElement.node().getBBox().width;
      let adjustedHeight = rowHeight;
      if (textWidth > fixedTableWidth - 20) {
        textElement
          .text("")
          .selectAll("tspan")
          .data(wrapText(processingText, fixedTableWidth - 20))
          .enter()
          .append("tspan")
          .attr("x", 0)
          .attr("dy", (t, j) => j === 0 ? "0.35em" : "1.2em")
          .text((t) => t);

        const lineCount = wrapText(processingText, fixedTableWidth - 20).length;
        adjustedHeight = rowHeight * lineCount / 2;
      }

      processingGroup
        .insert("rect", "text")
        .attr("x", -fixedTableWidth / 2)
        .attr("y", currentYOffset)
        .attr("width", fixedTableWidth)
        .attr("height", adjustedHeight)
        .attr("fill", "#FFFFFF")
        .attr("stroke", "#333");

      if (d.data.children && d.data.children.length > 0) {
        d.data.children[0].y = processingTableX;
        d.data.children[0].x = selectTableY + currentYOffset + adjustedHeight / 2;
      }

      // 绘制从 column_name 到 column_processing 的连接线
      svg
        .append("path")
        .attr("fill", "none")
        .attr("class", "table-link")
        .attr("stroke", "#666")
        .attr("stroke-width", 2)
        .attr("stroke-opacity", 0.5)
        .attr("d", `M${d.y + fixedTableWidth / 2},${d.x} L${processingTableX - 50},${d.x}`);

      currentYOffset += adjustedHeight;
    });

    // 记录 Select 和 Processing 表格的边界框
    tableBounds.push(selectGroup.node().getBBox());
    tableBounds.push(processingGroup.node().getBBox());
  }

  // 处理 From 表格
  if (fromNodes.length > 0) {
    const fromParent = fromNodes[0].parent;
    const fromTableX = fromParent.y + tableOffset;
    const fromTableY = fromParent.x - fromHeight / 2;

    const fromGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${fromTableX},${fromTableY})`);

    fromGroup
      .append("rect")
      .attr("x", -fixedTableWidth / 2)
      .attr("y", 0)
      .attr("width", fixedTableWidth)
      .attr("height", headerHeight)
      .attr("fill", "#FFD700")
      .attr("stroke", "#333");

    fromGroup
      .append("text")
      .attr("x", 0)
      .attr("y", headerHeight / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("fill", "black")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Table Name");

    let currentYOffset = headerHeight;
    fromNodes.forEach((d, i) => {
      const textContent = d.data.name || d.data.table_name;
      const textElement = fromGroup
        .append("text")
        .attr("x", 0)
        .attr("y", currentYOffset + rowHeight / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", "middle")
        .attr("fill", "#333")
        .style("font-size", "14px")
        .text(textContent);

      const textWidth = textElement.node().getBBox().width;
      let adjustedHeight = rowHeight;
      if (textWidth > fixedTableWidth - 20) {
        textElement
          .text("")
          .selectAll("tspan")
          .data(wrapText(textContent, fixedTableWidth - 20))
          .enter()
          .append("tspan")
          .attr("x", 0)
          .attr("dy", (t, j) => j === 0 ? "0.35em" : "1.2em")
          .text((t) => t);

        const lineCount = wrapText(textContent, fixedTableWidth - 20).length;
        adjustedHeight = rowHeight * lineCount;
      }

      fromGroup
        .insert("rect", "text")
        .attr("x", -fixedTableWidth / 2)
        .attr("y", currentYOffset)
        .attr("width", fixedTableWidth)
        .attr("height", adjustedHeight)
        .attr("fill", "#FFFFFF")
        .attr("stroke", "#333");

      d.y = fromTableX;
      d.x = fromTableY + currentYOffset + adjustedHeight / 2;

      currentYOffset += adjustedHeight;
    });

    fromNodes.forEach((d) => {
      svg
        .append("path")
        .attr("fill", "none")
        .attr("class", "table-link")
        .attr("stroke", "#aaa")
        .attr("stroke-width", 2)
        .attr("stroke-opacity", 0.5)
        .attr("d", `M${fromParent.y + 50},${fromParent.x} L${d.y - 50},${d.x}`);
    });
    tableBounds.push(fromGroup.node().getBBox());
  }

  // 处理其他关键字（others）
  const others = level1Nodes.filter(
    (d) => d.data.name !== "Select" && d.data.name !== "From"
  );

  others.forEach((parentNode) => {
    // 筛选当前关键字的子节点（depth=2）
    const childNodes = root.descendants().filter(
      (d) => d.depth === 2 && d.parent && d.parent.data.name === parentNode.data.name
    );

    if (childNodes.length > 0) {
      const tableHeight = headerHeight + childNodes.length * rowHeight + tablePadding * 2;
      const tableX = parentNode.y + tableOffset;
      const tableY = parentNode.x - tableHeight / 2;

      const tableGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${tableX},${tableY})`);

      // 绘制表头（使用关键字名称）
      tableGroup
        .append("rect")
        .attr("x", -fixedTableWidth / 2)
        .attr("y", 0)
        .attr("width", fixedTableWidth)
        .attr("height", headerHeight)
        .attr("fill", "#FFD700") // 可根据需要调整颜色
        .attr("stroke", "#333");

      tableGroup
        .append("text")
        .attr("x", 0)
        .attr("y", headerHeight / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", "middle")
        .attr("fill", "black")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text(parentNode.data.name); // 表头为关键字名称，如 "Where" 或 "Join"

      // 绘制表格行
      let currentYOffset = headerHeight;
      childNodes.forEach((d, i) => {
        const textContent = d.data.name || d.data.condition || d.data.table_name || ""; // 根据实际数据调整
        const textElement = tableGroup
          .append("text")
          .attr("x", 0)
          .attr("y", currentYOffset + rowHeight / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "middle")
          .attr("fill", "#333")
          .style("font-size", "14px")
          .text(textContent);

        const textWidth = textElement.node().getBBox().width;
        let adjustedHeight = rowHeight;
        if (textWidth > fixedTableWidth - 20) {
          textElement
            .text("")
            .selectAll("tspan")
            .data(wrapText(textContent, fixedTableWidth - 20))
            .enter()
            .append("tspan")
            .attr("x", 0)
            .attr("dy", (t, j) => (j === 0 ? "0.35em" : "1.2em"))
            .text((t) => t);

          const lineCount = wrapText(textContent, fixedTableWidth - 20).length;
          adjustedHeight = rowHeight * lineCount;
        }

        tableGroup
          .insert("rect", "text")
          .attr("x", -fixedTableWidth / 2)
          .attr("y", currentYOffset)
          .attr("width", fixedTableWidth)
          .attr("height", adjustedHeight)
          .attr("fill", "#FFFFFF")
          .attr("stroke", "#333");

        d.y = tableX;
        d.x = tableY + currentYOffset + adjustedHeight / 2;

        currentYOffset += adjustedHeight;
      });

      // 绘制连接线
      childNodes.forEach((d) => {
        svg
          .append("path")
          .attr("fill", "none")
          .attr("class", "table-link")
          .attr("stroke", "#aaa")
          .attr("stroke-width", 2)
          .attr("stroke-opacity", 0.5)
          .attr("d", `M${parentNode.y + 50},${parentNode.x} L${d.y - 50},${d.x}`);
      });
      tableBounds.push(tableGroup.node().getBBox());
    }
  })

// 检测重叠并调整树高度
function checkOverlap(bounds) {
  for (let i = 0; i < bounds.length - 1; i++) {
    for (let j = i + 1; j < bounds.length; j++) {
      const b1 = bounds[i];
      const b2 = bounds[j];
      if (
        b1.x < b2.x + b2.width &&
        b1.x + b1.width > b2.x &&
        b1.y < b2.y + b2.height &&
        b1.y + b1.height > b2.y
      ) {
        return true; // 检测到重叠
      }
    }
  }
  return false;
}

if (checkOverlap(tableBounds)) {
  // 如果有重叠，增加树的高度
  treeHeight += 200; // 每次增加 200px，可调整
  treeLayout.size([treeHeight, treeWidth]);
  treeLayout(root);

  // 更新所有节点位置（depth=0 和 depth=1）
  nodes.attr("transform", (d) => `translate(${d.y},${d.x})`);

  // 移除所有旧的连接线
  svg.selectAll("path.link").remove();       // 移除 depth=0 到 depth=1 的连接线
  svg.selectAll("path.table-link").remove(); // 移除 depth=1 到 depth=2 的连接线

  // 重新绘制 depth=0 到 depth=1 的连接线
  svg
    .selectAll("path.link")
    .data(root.links().filter((d) => d.target.depth === 1)) // 只绘制 depth=0 到 depth=1
    .enter()
    .append("path")
    .attr("class", "link")
    .attr("fill", "none")
    .attr("stroke", "#aaa")
    .attr("stroke-width", 2)
    .attr("d", (d) => `M${d.source.y + 50},${d.source.x} L${d.target.y - 50},${d.target.x}`);

  // 更新表格位置
  tableBounds.length = 0; // 清空旧边界框
  svg.selectAll("g.table-group").remove(); // 移除所有旧表格
  redrawTables(svg, root, tableOffset, headerHeight, rowHeight, tablePadding, fixedTableWidth);
}
  // 将文本移回中心
  texts.attr("text-anchor", "middle");

 // 辅助函数：重绘表格
 function redrawTables(svg, root, tableOffset, headerHeight, rowHeight, tablePadding, fixedTableWidth) {
  const level1Nodes = root.descendants().filter((d) => d.depth === 1);
  const selectNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "Select");
  const fromNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "From");
  const others = level1Nodes.filter((d) => d.data.name !== "Select" && d.data.name !== "From");

  if (selectNodes.length > 0) {
    const selectParent = selectNodes[0].parent;
    const selectTableX = selectParent.y + tableOffset;
    const selectTableY = selectParent.x - selectHeight / 2;
    const selectGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${selectTableX},${selectTableY})`);
    drawTable(selectGroup, "Column Name", selectNodes, "#FFD700", fixedTableWidth, headerHeight, rowHeight, tablePadding, selectParent);

    const processingTableX = selectTableX + fixedTableWidth + 100;
    const processingTableY = selectTableY - 50;
    const processingGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${processingTableX},${processingTableY})`);
    drawProcessingTable(processingGroup, selectNodes, "#87CEEB", fixedTableWidth, headerHeight, rowHeight, tablePadding);

    tableBounds.push(selectGroup.node().getBBox());
    tableBounds.push(processingGroup.node().getBBox());
  }

  if (fromNodes.length > 0) {
    const fromParent = fromNodes[0].parent;
    const fromTableX = fromParent.y + tableOffset;
    const fromTableY = fromParent.x - fromHeight / 2;
    const fromGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${fromTableX},${fromTableY})`);
    drawTable(fromGroup, "Table Name", fromNodes, "#FFD700", fixedTableWidth, headerHeight, rowHeight, tablePadding, fromParent);
    tableBounds.push(fromGroup.node().getBBox());
  }

  let lastTableBottom = -Infinity;
  const tableSpacing = 20;

  others.forEach((parentNode) => {
    const childNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === parentNode.data.name);
    if (childNodes.length > 0) {
      const tableHeight = headerHeight + childNodes.length * rowHeight + tablePadding * 2;
      const tableX = parentNode.y + tableOffset;
      const tableY = Math.max(parentNode.x - tableHeight / 2, lastTableBottom + tableSpacing);
      const tableGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${tableX},${tableY})`);
      drawTable(tableGroup, parentNode.data.name, childNodes, "#FFD700", fixedTableWidth, headerHeight, rowHeight, tablePadding, parentNode);
      tableBounds.push(tableGroup.node().getBBox());
      lastTableBottom = tableY + tableHeight;
    }
  });
}

// 绘制普通表格
function drawTable(group, headerText, nodes, headerFill, fixedTableWidth, headerHeight, rowHeight, tablePadding, parentNode) {
  group.append("rect").attr("x", -fixedTableWidth / 2).attr("y", 0).attr("width", fixedTableWidth).attr("height", headerHeight).attr("fill", headerFill).attr("stroke", "#333");
  group.append("text").attr("x", 0).attr("y", headerHeight / 2).attr("dy", "0.35em").attr("text-anchor", "middle").attr("fill", "black").style("font-size", "16px").style("font-weight", "bold").text(headerText);

  let currentYOffset = headerHeight;
  nodes.forEach((d, i) => {
    const textContent = d.data.name || d.data.column_name || d.data.table_name || d.data.condition || "";
    const textElement = group.append("text").attr("x", 0).attr("y", currentYOffset + rowHeight / 2).attr("dy", "0.35em").attr("text-anchor", "middle").attr("fill", "#333").style("font-size", "14px").text(textContent);

    const textWidth = textElement.node().getBBox().width;
    let adjustedHeight = rowHeight;
    if (textWidth > fixedTableWidth - 20) {
      textElement.text("").selectAll("tspan").data(wrapText(textContent, fixedTableWidth - 20)).enter().append("tspan").attr("x", 0).attr("dy", (t, j) => (j === 0 ? "0.35em" : "1.2em")).text((t) => t);
      const lineCount = wrapText(textContent, fixedTableWidth - 20).length;
      adjustedHeight = rowHeight * lineCount; // 与初始绘制一致
    }

    group.insert("rect", "text").attr("x", -fixedTableWidth / 2).attr("y", currentYOffset).attr("width", fixedTableWidth).attr("height", adjustedHeight).attr("fill", "#FFFFFF").attr("stroke", "#333");

    d.y = group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/)[1];
    d.x = parseFloat(group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/)[2]) + currentYOffset + adjustedHeight / 2;

    svg.append("path").attr("class", "table-link").attr("fill", "none").attr("stroke", "#aaa").attr("stroke-width", 2).attr("stroke-opacity", "0.5").attr("d", `M${parentNode.y + 50},${parentNode.x} L${d.y - 50},${d.x}`);

    currentYOffset += adjustedHeight;
  });
}

// 绘制 Column Processing 表格
function drawProcessingTable(group, nodes, headerFill, fixedTableWidth, headerHeight, rowHeight, tablePadding) {
  group.append("rect").attr("x", -fixedTableWidth / 2).attr("y", 0).attr("width", fixedTableWidth).attr("height", headerHeight).attr("fill", headerFill).attr("stroke", "#333");
  group.append("text").attr("x", 0).attr("y", headerHeight / 2).attr("dy", "0.35em").attr("text-anchor", "middle").attr("fill", "black").style("font-size", "16px").style("font-weight", "bold").text("Column Processing");

  let currentYOffset = headerHeight;
  nodes.forEach((d, i) => {
    const processingText = d.data.children && d.data.children.length > 0 ? d.data.children[0].name : "";
    const textElement = group.append("text").attr("x", 0).attr("y", currentYOffset + rowHeight / 2).attr("dy", "0.35em").attr("text-anchor", "middle").attr("fill", "#333").style("font-size", "14px").text(processingText);

    const textWidth = textElement.node().getBBox().width;
    let adjustedHeight = rowHeight;
    if (textWidth > fixedTableWidth - 20) {
      textElement.text("").selectAll("tspan").data(wrapText(processingText, fixedTableWidth - 20)).enter().append("tspan").attr("x", 0).attr("dy", (t, j) => (j === 0 ? "0.35em" : "1.2em")).text((t) => t);
      const lineCount = wrapText(processingText, fixedTableWidth - 20).length;
      adjustedHeight = rowHeight * lineCount / 2; // 恢复初始绘制的紧凑逻辑
    }

    group.insert("rect", "text").attr("x", -fixedTableWidth / 2).attr("y", currentYOffset).attr("width", fixedTableWidth).attr("height", adjustedHeight).attr("fill", "#FFFFFF").attr("stroke", "#333");

    if (d.data.children && d.data.children.length > 0) {
      d.data.children[0].y = group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/)[1];
      d.data.children[0].x = parseFloat(group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/)[2]) + currentYOffset + adjustedHeight / 2;
    }

    svg.append("path").attr("class", "table-link").attr("fill", "none").attr("stroke", "#666").attr("stroke-width", 2).attr("stroke-opacity", "0.5").attr("d", `M${d.y + fixedTableWidth / 2},${d.x} L${parseFloat(group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/)[1]) - 50},${d.x}`);

    currentYOffset += adjustedHeight;
  });
}

// 辅助函数：将长文本拆分为多行
function wrapText(text, maxWidth) {
  const words = text.split(" ");
  const lines = [];
  let currentLine = words[0];

  const tempText = svg.append("text").attr("visibility", "hidden").style("font-size", "14px");
  for (let i = 1; i < words.length; i++) {
    tempText.text(currentLine + " " + words[i]);
    if (tempText.node().getBBox().width < maxWidth) {
      currentLine += " " + words[i];
    } else {
      lines.push(currentLine);
      currentLine = words[i];
    }
  }
  lines.push(currentLine);
  tempText.remove();
  return lines;
}

  // **将文本移回中心**
  texts.attr("text-anchor", "middle");
});
</script>

<style>
.link {
  stroke-width: 2px;
}

svg {
  border: 1px solid #ccc;
}

.header {
  background-color: #AEC6EA; /* 设置背景颜色 */
  padding: 10px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
}

.chart-nodes {
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 🌟 让 el-card 绝对定位，避免从上到下堆叠 */
.node-card {
  position: absolute;
  min-width: 180px; /* 避免过窄 */
  max-width: 250px; /* 限制最大宽度 */
  padding: 8px;
  background-color: #fff;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  transition: transform 0.3s ease-in-out;
  text-align: center;
  
  /* 🌟 让节点中心对齐，而不是左上角对齐 */
  transform: translate(-50%, -50%);
}

/* 🌟 让表格节点的子项居中 */
.node-row {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px;
  border-bottom: 1px solid #ddd;
  font-size: 14px;
}

/* 最后一行去掉分割线 */
.node-row:last-child {
  border-bottom: none;
}
</style>