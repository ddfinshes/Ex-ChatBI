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
            node.children.push({ name: item.column_name });
          } else if (item.table_name) {
            node.children.push({ name: item.table_name });
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
  const svg = d3
    .select(chart.value)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(50,50)");

  // **横向树布局**
  const treeLayout = d3.cluster().size([height - 100, width - 200]);

  treeLayout(root);

  // **绘制连接线**
  svg
    .selectAll("path.link")
    .data(root.links())
    .enter()
    .append("path")
    .attr("fill", "none")
    .attr("stroke", "#aaa")
    .attr("stroke-width", 2)
    .attr("d", (d) => `M${d.source.y + 50},${d.source.x} L${d.target.y - 50},${d.target.x}`);

  // **绘制节点**
  const nodes = svg
    .selectAll("g.node")
    .data(root.descendants())
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
  nodes.each(function (d, i) {
  if (d.depth !== 2) return;

  const tableWidth = 250; // 调整宽度
  const rowHeight = 40;
  const headerHeight = 50;
  const padding = 10;

  // **获取当前节点的父节点**
  const parentNode = d.parent;
  console.log(parentNode.data)
  const isSelect = parentNode && parentNode.data.name === "Select";  // 正确获取 `Select`
  const isFrom = parentNode && parentNode.data.name === "From";  // 正确获取 `From`

  // 筛选 `Select` 和 `From` 下的所有 `depth === 2` 节点
  const selectNodes = nodes.filter(d => d.depth === 2 && d.parent && d.parent.data.name === "Select");
  const fromNodes = nodes.filter(d => d.depth === 2 && d.parent && d.parent.data.name === "From");

  // 计算 `Select` 和 `From` 相关节点的整体高度（包含表头）
  const totalSelectHeight = headerHeight + selectNodes.size() * rowHeight + padding * 2;
  const totalFromHeight = headerHeight + fromNodes.size() * rowHeight + padding * 2;

  // 获取当前节点
  const tableGroup = d3.select(this);
  const isFirstSelect = selectNodes.nodes()[0] === this;
  const isFirstFrom = fromNodes.nodes()[0] === this;

  // **计算每个 node 的 y 位置**
  let yOffset;
  if (isSelect) {
    yOffset = -totalSelectHeight / 2 + headerHeight + i * rowHeight + rowHeight / 2;
  } else {
    yOffset = -totalFromHeight / 2 + headerHeight + i * rowHeight + rowHeight / 2;
  }

  // **在第一个 `Select` 相关节点上绘制表头**
  if (isFirstSelect) {
    tableGroup
      .insert("rect", "text")
      .attr("x", -tableWidth / 2)
      .attr("y", -totalSelectHeight / 2)
      .attr("width", tableWidth)
      .attr("height", headerHeight)
      .attr("fill", "#FFD700")
      .attr("stroke", "#333");

    tableGroup
      .append("text")
      .attr("x", 0)
      .attr("y", -totalSelectHeight / 2 + headerHeight / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("fill", "black")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Column Name");
  }

  // **在第一个 `From` 相关节点上绘制表头**
  if (isFirstFrom) {
    tableGroup
      .insert("rect", "text")
      .attr("x", -tableWidth / 2)
      .attr("y", -totalFromHeight / 2)
      .attr("width", tableWidth)
      .attr("height", headerHeight)
      .attr("fill", "#FFD700")
      .attr("stroke", "#333");

    tableGroup
      .append("text")
      .attr("x", 0)
      .attr("y", -totalFromHeight / 2 + headerHeight / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("fill", "black")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Table Name");
  }

  // **绘制表格行（卡片背景）**
  tableGroup
    .insert("rect", "text")
    .attr("x", -tableWidth / 2)
    .attr("y", yOffset - rowHeight / 2)
    .attr("width", tableWidth)
    .attr("height", rowHeight)
    .attr("fill", "#FFFFFF")
    .attr("stroke", "#333");

  // **填充数据**
  tableGroup
    .append("text")
    .attr("x", 0)
    .attr("y", yOffset)
    .attr("dy", "0.35em")
    .attr("text-anchor", "middle")
    .attr("fill", "#333")
    .style("font-size", "14px")
    .text(isSelect ? d.data.column_name : d.data.table_name);

  // **添加分割线**
  if ((isSelect && !isFirstSelect) || (isFrom && !isFirstFrom)) {
    tableGroup
      .append("line")
      .attr("x1", -tableWidth / 2 + padding)
      .attr("x2", tableWidth / 2 - padding)
      .attr("y1", yOffset + rowHeight / 2)
      .attr("y2", yOffset + rowHeight / 2)
      .attr("stroke", "#ddd");
  }
});


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