<template>
  <div style="height: 747px; width: 100%;">
    <!-- 添加 Header -->
    <div class="view-header">Dual-Mode SQL Refinement View</div>
    <!-- 原有的 chart 容器 -->
    <div ref="chart"></div>
    <div class="NLExplain">
      <el-card shadow="always" class="combined-card" v-if="sqlstepnl && sqlstepnl !== ''">
        <div v-for="(item, index) in sqlstepnl.data" :key="index" class="data-item">
          <p class="description">{{ item.descripe }}</p>
          <pre class="code-block"><code v-html="highlightRef(item.ref[0])"></code></pre>
        </div>
        <div class="simple-logic">
          <p><strong>Simple Logic:</strong> {{ sqlstepnl['Simple Logic'] }}</p>
        </div>
      </el-card>
    </div>
  </div>

</template>

<script>
import { ref, onMounted, nextTick, watch, computed, onUnmounted, watchEffect } from "vue";
import * as d3 from "d3";
import { useQueryStore } from '@/stores/query';
import { emitter } from '@/assets/ts/eventBus.js';
import axios from "axios";
import { ca } from "element-plus/es/locales.mjs";

export default {
  data() {
    return {
      store: useQueryStore(),
      sqlcode: '', // sql 代码
      sqljson: '', // json 格式的 sql
      subsql: '',
      subsqljson: '',
      sqlstepnl: '', //最下方框中的内容
      explanation: "这个 SQL 查询使用了索引扫描，提高了查询效率，但可能还可以优化为覆盖索引...",
      chart: null,
      nodes: [],
      nodeCards: [],
      data: '',
      // res: {
      //   content: [
      //     {
      //       "created_virtual_table": "False",
      //       "sql_content": [
      //         {
      //           "keywords": "From",
      //           "scratched_content": [
      //             { "table_name": "Monthly_Growth", "is_virtual_table": "True", 'NL Explain': "AAA"}
      //           ]
      //         },
      //         {
      //           "keywords": "Select",
      //           "scratched_content": [
      //             { "column_name": "month_id", "column_processing": "", 'NL Explain': "BBB"},
      //             { "column_name": "Current_Month_Effi", "column_processing": "TO_CHAR (Current_Month_Effi, 'FM999,999,999.00') AS Current_Month_Effi", 'NL Explain': "CCC"},
      //             { "column_name": "Previous_Month_Effi", "column_processing": "TO_CHAR (Previous_Month_Effi, 'FM999,999,999.00') AS Previous_Month_Effi", 'NL Explain': "DDD"},
      //             { "column_name": "Growth_Percentage", "column_processing": "TO_CHAR (Growth_Percentage, 'FM999,999,999.00') || '%' AS Growth_Percentage", 'NL Explain': "EEE"}
      //           ]
      //         },
      //         {
      //           "keywords": "Join",
      //           "scratched_content": [
      //             { "content": "TO_CHAR (DATEADD (month, 1, TO_DATE (p.month_id, 'YYYYMM')), 'YYYYMM')", 'NL Explain': "FFF"}
      //           ]
      //         },
      //         {
      //           "keywords": "Where",
      //           "scratched_content": [
      //             { "content": "c.month_id = '202410'",'NL Explain': "ZZZ"}
      //           ]
      //         }
      //       ]
      //     },
      //     {
      //       "created_virtual_table": "True",
      //       "virtual_table_name": "Monthly_Growth",
      //       "sql_content": [
      //         {
      //           "keywords": "Select",
      //           "scratched_content": [
      //             { "column_name": "c.month_id", "column_processing": "", 'NL Explain': "hhh"},
      //             { "column_name": "Current_Month_Effi", "column_processing": "c.Avg_effi AS Current_Month_Effi" },
      //             { "column_name": "Previous_Month_Effi", "column_processing": "p.Avg_effi AS Previous_Month_Effi" },
      //             { "column_name": "Growth_Percentage", "column_processing": "(c.Avg_effi / p.Avg_effi - 1) * 100 AS Growth_Percentage" }
      //           ]
      //         },
      //         {
      //           "keywords": "From",
      //           "scratched_content": [
      //             { "table_name": "Effi_Comparison c", "is_virtual_table": "True", 'NL Explain': "wowowo"}
      //           ]
      //         },
      //         {
      //           "keywords": "Join",
      //           "scratched_content": [
      //             { "content": "JOIN Effi_Comparison p ON c.month_id = TO_CHAR (DATEADD (month, 1, TO_DATE (p.month_id, 'YYYYMM')), 'YYYYMM')" }
      //           ]
      //         },
      //         {
      //           "keywords": "Where",
      //           "scratched_content": [
      //             { "content": "c.month_id = '202410'" }
      //           ]
      //         }
      //       ]
      //     },
      //     {
      //       "created_virtual_table": "True",
      //       "virtual_table_name": "Effi_Comparison",
      //       "sql_content": [
      //         {
      //           "keywords": "Select",
      //           "scratched_content": [
      //             { "column_name": "month_id", "column_processing": "" },
      //             { "column_name": "Avg_effi", "column_processing": "AVG(effi) AS Avg_effi" }
      //           ]
      //         },
      //         {
      //           "keywords": "From",
      //           "scratched_content": [
      //             { "table_name": "Store_effi", "is_virtual_table": "True" }
      //           ]
      //         },
      //         {
      //           "keywords": "Group By",
      //           "scratched_content": [
      //             { "content": "month_id" }
      //           ]
      //         }
      //       ]
      //     },
      //     {
      //       "created_virtual_table": "True",
      //       "virtual_table_name": "Store_effi",
      //       "sql_content": [
      //         {
      //           "keywords": "Select",
      //           "scratched_content": [
      //             { "column_name": "country", "column_processing": "" },
      //             { "column_name": "channel", "column_processing": "" },
      //             { "column_name": "store_type", "column_processing": "" },
      //             { "column_name": "area", "column_processing": "" },
      //             {
      //               "column_name": "effi",
      //               "column_processing": "CASE WHEN (COALESCE(area, '') = '' OR CAST(area AS DECIMAL(18, 2)) = 0) THEN 0 ELSE AVG(COALESCE(amt_usd_notax, 0)) * 365 / CAST(area AS DECIMAL(18, 2)) * 10.7639104 END AS effi"
      //             },
      //             { "column_name": "month_id", "column_processing": "" }
      //           ]
      //         },
      //         {
      //           "keywords": "From",
      //           "scratched_content": [
      //             { "table_name": "dm_fact_sales_chatbi", "is_virtual_table": "False" }
      //           ]
      //         },
      //         {
      //           "keywords": "Where",
      //           "scratched_content": [
      //             {
      //               "content": "date_code <= '2024-10-31' AND country = 'Mainland' AND channel = 'O&O' AND store_type = 'BH' AND comp_flag = 'Y'"
      //             }
      //           ]
      //         },
      //         {
      //           "keywords": "Group By",
      //           "scratched_content": [
      //             { "content": "country, channel, store_type, store_code, area, month_id" }
      //           ]
      //         }
      //       ]
      //     }
      //   ]
      // },
      // subsql: {
      //   content: [
      //     {
      //       "created_virtual_table": "False",
      //       "sql_content": [
      //         {
      //           "keywords": "From",
      //           "scratched_content": [
      //             { "table_name": "Monthly_Growth", "is_virtual_table": "True", 'Nl Explain': "AAA"}
      //           ]
      //         },
      //         {
      //           "keywords": "Select",
      //           "scratched_content": [
      //           { "column_name": "Current_Month_Effi", "column_processing": "TO_CHAR (Current_Month_Effi, 'FM999,999,999.00') AS Current_Month_Effi", 'NL Explain': "CCC"},
      //           ]
      //         },
      //         {
      //           "keywords": "Join",
      //           "scratched_content": [
      //             { "content": "TO_CHAR (DATEADD (month, 1, TO_DATE (p.month_id, 'YYYYMM')), 'YYYYMM')", 'Nl Explain': "FFF"}
      //           ]
      //         }
      //       ]
      //     },
      //     {
      //       "created_virtual_table": "True",
      //       "virtual_table_name": "Monthly_Growth",
      //       "sql_content": [
      //         {
      //           "keywords": "Select",
      //           "scratched_content": [
      //             { "column_name": "c.month_id", "column_processing": "", 'NL Explain': "hhh"},
      //             { "column_name": "Growth_Percentage", "column_processing": "(c.Avg_effi / p.Avg_effi - 1) * 100 AS Growth_Percentage" }
      //           ]
      //         },
      //         {
      //           "keywords": "From",
      //           "scratched_content": [
      //             { "table_name": "Effi_Comparison c", "is_virtual_table": "True", 'NL Explain': "wowowo"}
      //           ]
      //         },
      //       ]
      //     }
      //   ]
      // },
      res: [],
      currentTree: null,
      vistualtable_svgs: [],
      // testData: {
      // "data": [
      // {
      // "descripe": "1. Pick the Data Source: Use a table called dm_fact_sales_chatbi, like a spreadsheet of sales data.",
      // "ref": ["FROM dm_fact_sales_chatbi"]
      // },
      // {
      // "descripe": "2. Calculate the Total: Add up all values in the amt_notax column (sales without tax) and name the result curr_sales.",
      // "ref": ["SUM(amt_notax) AS curr_sales"]
      // },
      // {
      // "descripe": "3. Filter by Date: Only include sales from February 16 to February 19, 2025.",
      // "ref": ["date_code BETWEEN '2025-02-16' AND '2025-02-19'"]
      // },
      // {
      // "descripe": "4. Filter by Status: Only include sales marked as completed (comp_flag = 'Y').",
      // "ref": ["comp_flag = 'Y'"]
      // }
      // ],
      // "Simple Logic": "From the sales table, sum the sales amounts without tax for completed sales between Feb 16-19, 2025, and show the total as curr_sales."
      // },
      SQL_KEYWORDS: [
        "Select",
        "From",
        "Where",
        "Group By",
        "Join",
        "Having",
        "Order By",
      ]
    };
  },
  mounted() {
    this.$nextTick(() => {
      console.log("Component mounted, checking res...");
      // console.log("Initial store state:", this.store.$state);
      // const data = this.transformToTree(this.res);
      // this.currentTree = this.transformToTree(this.subsql)
      // this.draw(data);
    })
  },
  watch: {
    'store.response': {
      handler(newVal) {
        setTimeout(() => {
          if (newVal) {
            this.sqlcode = newVal.code;
            console.log('store.response updated:', this.sqlcode);
            if (newVal.code) {
              this.getSQL2JSON(newVal.code).then(result => {
                this.sqljson = result['sql_json'];
                this.res = result['sql_json']; // 将 res.data 直接作为新的 res
                this.sqlstepnl = result['sql_stepnl']
                console.log('---------------sqlstepnl----------------------', this.sqlstepnl);
                console.log('---------------sqljson----------------------', this.sqljson);
                if (this.res) {
                  this.data = this.transformToTree(this.res);
                  this.draw(this.data); // 使用新的 res 数据绘制
                }
              }).catch(error => {
                console.error("Error fetching SQL2JSON:", error);
              });
            }
          }
        }, 1000); // 保留原始 1000ms 延迟
      },
      deep: true,
      immediate: true // 检查初始值
    },

    'store.subsqljson': {
      handler(newVal) {
        setTimeout(() => {
          console.log(newVal);
          if (newVal) {
            this.subsql = newVal['sql_json'];
            console.log('subsql', this.subsql);
            this.sqlstepnl = newVal['sql_stepnl']
            console.log('---------------sub-sqlstepnl----------------------', this.sqlstepnl)
            this.currentTree = this.transformToTree(this.subsql);
            console.log('----------------currentTree for highlight------------------', this.currentTree);
            this.draw(this.data)
            // this.getSubsqljson(this.subsql).then(res => {
            //   this.subsqljson = res.content;
            //   console.log('subsqljson', this.subsqljson);
            // }).catch(error => {
            //   console.error("Error fetching subsqljson:", error);
            // });
          }
        }, 1000);
      },
      deep: true
    }
  },
// ------------------------------------------------
// const store = useQueryStore();
// const sqlcode = ref(''); // sql代码
// let sqljson = ''; // json格式的sql
// const subsql = ref('');
// const subsqljson = '';
// watchEffect(() => {
//   setTimeout(() => {
//     if (store.response) {
//       sqlcode.value = store.response.code
//       console.log('store.response updated:', sqlcode.value);
//       if (store.response.code) {
//         getSQL2JSON(store.response.code).then(result => {
//           sqljson = result;
//           console.log('---------------sqljson----------------------', result)
//           console.log('---------------sqljson----------------------', sqljson)
//         })
//       }
//     }

//   }, 1000);
//   setTimeout(() => {
//     console.log(store.subsqljson)
//     if (store.subsqljson) {
//       subsql = store.subsqljson;
//       console.log('subsqljson', subsqljson);
//       getSubsqljson(subsqljson).then(res => {
//         subsqljson = res.content;
//         console.log('subsqljson', subsqljson);
//       })
//     }
//   }, 1000);
// })

// async function getSubsqljson(payload) {
//   const res = await axios.post(
//     "/api/relatsql",
//     payload
//   );
//   return res.data;
// }

// async function getSQL2JSON(sql) {
//   const res = await axios.post(
//     "/api/sql2json",
//     { data: sql },
//     { headers: { "Content-Type": "application/json" } }
//   );
//   return res.data;
// }

// if (sqljson) {
//   console.log('sqljson', sqljson)
// }


//--------------------------------------------------------

// let res = '';
// if (sqljson) {
//   res = sqljson;
//   console.log('-------res-------', res)
// }

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
// const res = sqljson;


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
 methods: {
  // async getSubsqljson(payload) {
  //     const res = await axios.post("/api/relatsql", payload);
  //     return res.data;
  //   },

    async getSQL2JSON(sql) {
      const res = await axios.post(
        "/api/sql2json",
        { data: sql },
        { headers: { "Content-Type": "application/json" } }
      );
      return res.data;
    },
  
    highlightRef(ref) {
      // 将 ref 字符串拆分为单词和空白部分
      const parts = ref.split(/(\s+)/); // 按空白分割，保留空格
      return parts
        .map(part => {
          if (/\S/.test(part)) {
            // 非空白部分，高亮
            return `<span class="highlight">${part}</span>`;
          } else {
            // 空白部分，不高亮
            return part;
          }
        })
        .join('');
    },
  // **1. 数据转换：转换成树形结构**
    transformToTree(data) {
      const root = { name: "Main Query", children: [] };
      const virtualTables = new Map(); // 存储虚拟表，便于查找和嵌套

      // 第一步：处理所有虚拟表，构建子树
      data.content.forEach((contentItem) => {
        if (contentItem.created_virtual_table === "True") {
          const virtualTableNode = {
            name: contentItem.virtual_table_name,
            children: [],
            isVirtual: true
          };

          contentItem.sql_content.forEach((section) => {
            const sectionNode = { name: section.keywords, children: [] };

            if (section.scratched_content) {
              section.scratched_content.forEach((item) => {
                let nodeName = item.column_name || item.table_name || item.content || "";
                let newNode;

                // 检查 nodeName 是否包含某个虚拟表名
                let matchedVirtualTable = null;
                for (const [virtualName, virtualNode] of virtualTables) {
                  if (nodeName.includes(virtualName)) {
                    matchedVirtualTable = virtualNode;
                    break;
                  }
                }

                if (matchedVirtualTable) {
                  newNode = matchedVirtualTable; // 使用匹配的虚拟表
                  // 如果有 Nl Explain，附加到虚拟表节点（可选）
                  if (item['NL Explain']) {
                    newNode.nlExplain = item['NL Explain'];
                  }
                } else {
                  newNode = {
                    name: nodeName,
                    children: [],
                    nlExplain: item['NL Explain'] || '' // 始终记录 Nl Explain
                  };
                  // 如果是 column_name 且有 column_processing，添加子节点
                  if (item.column_name && item.column_processing && item.column_processing.trim() !== '') {
                    newNode.children.push({
                      name: item.column_processing,
                      nlExplain: '' // 子节点默认无 Nl Explain
                    });
                  }
                }

                sectionNode.children.push(newNode);
              });
            }

            virtualTableNode.children.push(sectionNode);
          });

          virtualTables.set(contentItem.virtual_table_name, virtualTableNode);
        }
      });

      // 第二步：处理主查询
      if (data.content[0].created_virtual_table === "False") {
        data.content[0].sql_content.forEach((section) => {
          const sectionNode = { name: section.keywords, children: [] };

          if (section.scratched_content) {
            section.scratched_content.forEach((item) => {
              let nodeName = item.column_name || item.table_name || item.content || "";
              let newNode;

              // 检查 nodeName 是否包含某个虚拟表名
              let matchedVirtualTable = null;
              for (const [virtualName, virtualNode] of virtualTables) {
                if (nodeName.includes(virtualName)) {
                  matchedVirtualTable = virtualNode;
                  break;
                }
              }

              if (matchedVirtualTable) {
                newNode = matchedVirtualTable; // 使用匹配的虚拟表
                // 如果有 Nl Explain，附加到虚拟表节点（可选）
                if (item['NL Explain']) {
                  newNode.nlExplain = item['NL Explain'];
                }
              } else {
                newNode = {
                  name: nodeName,
                  children: [],
                  nlExplain: item['NL Explain'] || '' // 始终记录 Nl Explain
                };
                // 如果是 column_name 且有 column_processing，添加子节点
                if (item.column_name && item.column_processing && item.column_processing.trim() !== '') {
                  newNode.children.push({
                    name: item.column_processing,
                    nlExplain: '' // 子节点默认无 Nl Explain
                  });
                }
              }

              sectionNode.children.push(newNode);
            });
          }

          root.children.push(sectionNode);
        });
      }

      return root;
    },

    draw(data) {
      const self = this
      let virtual_svgs = []
      d3.select(this.$refs.chart).select("svg").remove(); // 清除旧 SVG
      const root = d3.hierarchy(data);

      const width = 1205;
      const height = 630;
      const rectHeight = 40; // 矩形高度
      const padding = 20; // 矩形两侧的额外间距


      // 创建 SVG 画布
      const svgContainer = d3
        .select(this.$refs.chart)
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
        .data(root.links().filter((d) => d.target.depth === 1 && !d.target.data.isVirtual)) // 排除 depth=2 的目标节点
        .enter()
        .append("path")
        .attr("class", "table-link")
        .attr("fill", "none")
        .attr("stroke", "#aaa")
        .attr("stroke-width", 4)
        .attr("d", (d) => `M${d.source.y + 50},${d.source.x} L${d.target.y - 50},${d.target.x}`);
      
      
      // **绘制节点**
      const nodes = svg
        .selectAll("g.node")
        .data(root.descendants().filter((d) => d.depth === 0 || (d.depth === 1 && !d.data.isVirtual))) // 排除 depth=2
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
        .attr("fill", "#A0D5D0") // 根节点和第一层灰色
        .attr("stroke", "none");

      // **处理表格样式的节点**
      const tableWidth = 250; // 表格宽度
      const rowHeight = 30; // 每行高度
      const headerHeight = 50; // 表头高度
      const tablePadding = 10; // 表格内边距
      const tableOffset = 300; // 表格相对于父节点的水平偏移量
      const fixedTableWidth = 250;

      // 筛选所有 depth=1 节点（第二层节点）
      const level1Nodes = root.descendants().filter((d) => d.depth === 1 && !d.data.isVirtual);

      // 筛选 Select 和 From 的子节点
      const selectNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "Select");
      const fromNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "From");

      // 计算表格总高度
      const selectHeight = headerHeight + selectNodes.length * rowHeight + tablePadding * 2;
      const fromHeight = headerHeight + fromNodes.length * rowHeight + tablePadding * 2;

      // 存储所有表格的边界框，用于检测重叠
      const tableBounds = [];

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
          .attr("fill", "#ffae78")
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
            .attr("stroke-width", 4)
            .attr("stroke-opacity", 0.8)
            .attr("d", `M${fromParent.y + 50},${fromParent.x} L${d.y - 50},${d.x}`);
        });
        tableBounds.push(fromGroup.node().getBBox());
      }

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
          .attr("fill", "#ffae78")
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
            .attr("stroke-width", 4)
            .attr("stroke-opacity", 0.8)
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
            d.data.children[0].y = processingTableX
            d.data.children[0].x = currentYOffset + adjustedHeight / 2;
          }

          // 绘制从 column_name 到 column_processing 的连接线
          svg
            .append("path")
            .attr("fill", "none")
            .attr("class", "table-link")
            .attr("stroke", "#666")
            .attr("stroke-width", 4)
            .attr("stroke-opacity", 0.8)
            .attr("d", `M${d.y + fixedTableWidth / 2},${d.x} L${processingTableX - 50},${d.x}`);

          currentYOffset += adjustedHeight;
        });

        // 记录 Select 和 Processing 表格的边界框
        tableBounds.push(selectGroup.node().getBBox());
        tableBounds.push(processingGroup.node().getBBox());
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
            .attr("fill", "#ffae78") // 可根据需要调整颜色
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
              .attr("stroke-width", 4)
              .attr("stroke-opacity", 0.8)
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
          .data(root.links().filter((d) => d.target.depth === 1 && !d.target.data.isVirtual))
          .enter()
          .append("path")
          .attr("class", "link")
          .attr("fill", "none")
          .attr("stroke", "#B0ACAC")
          .attr("stroke-opacity", 0.8)
          .attr("stroke-width", 4)
          .attr("d", (d) => {
            const control1Y = d.source.y + 50;                   // 第一个控制点 Y 与起点 Y 相同
            const control1X = (d.source.x + d.target.x) / 2;     // 第一个控制点 X 在中点
            const control2Y = d.target.y - 50;                   // 第二个控制点 Y 与终点 Y 相同
            const control2X = (d.source.x + d.target.x) / 2;     // 第二个控制点 X 在中点
            return `M${d.source.y + 50},${d.source.x} C${control1Y},${control1X} ${control2Y},${control2X} ${d.target.y - 50},${d.target.x}`;
          });

        // 更新表格位置
        tableBounds.length = 0; // 清空旧边界框
        svg.selectAll("g.table-group").remove(); // 移除所有旧表格
        redrawTables(svg, root, tableOffset, headerHeight, rowHeight, tablePadding, fixedTableWidth);
      }
      // 将文本移回中心
      texts.attr("text-anchor", "middle");

      // 辅助函数：重绘表格
      function redrawTables(svg, root, tableOffset, headerHeight, rowHeight, tablePadding, fixedTableWidth) {
        const level1Nodes = root.descendants().filter((d) => d.depth === 1 && !d.data.isVirtual);
        const selectNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "Select");
        const fromNodes = root.descendants().filter((d) => d.depth === 2 && d.parent && d.parent.data.name === "From");
        const others = level1Nodes.filter((d) => d.data.name !== "Select" && d.data.name !== "From");

        if (selectNodes.length > 0) {
          const selectParent = selectNodes[0].parent;
          const selectTableX = selectParent.y + tableOffset;
          const selectTableY = selectParent.x - selectHeight / 2;
          const selectGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${selectTableX},${selectTableY})`);
          drawTable(selectGroup, "Column Name", selectNodes, "#ffae78", fixedTableWidth, headerHeight, rowHeight, tablePadding, selectParent);

          const processingTableX = selectTableX + fixedTableWidth + 100;
          const processingTableY = selectTableY - 50;
          const processingGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${processingTableX},${processingTableY})`);
          drawProcessingTable(processingGroup, selectNodes, "#87CEEB", fixedTableWidth, headerHeight, rowHeight, tablePadding, processingTableX);

          // 添加 Column Processing 的 NL Explain 表格
          const processingHeight = headerHeight + selectNodes.reduce((acc, d) => {
            const text = d.data.children && d.data.children.length > 0 ? d.data.children[0].name : "";
            const lineCount = wrapText(text, fixedTableWidth - 20).length;
            return acc + (lineCount > 1 ? rowHeight * lineCount / 2 : rowHeight);
          }, 0);
          const explainTableX = processingTableX + fixedTableWidth + 5;
          const explainTableY = processingTableY;
          const explainGroup = svg.append("g").attr("class", "explain-group").attr("transform", `translate(${explainTableX},${explainTableY})`);
          drawNLExplainTable(explainGroup, selectNodes, "#90EE90", fixedTableWidth, headerHeight, rowHeight, tablePadding);

          // 检查并绘制虚拟表
          let lastTableX = explainTableX + fixedTableWidth; // 从 NL Explain 右侧开始
          selectNodes.forEach((node) => {
            if (node.data.isVirtual && node.children && node.children.length > 0) {
              const virtualTableX = lastTableX + 50; // 在 NL Explain 后偏移
              const virtualTableY = selectTableY; // 与 Select 对齐
              const virtualGroup = svg.append("g")
                .attr("class", "virtual-table-group")
                .attr("transform", `translate(${virtualTableX},${virtualTableY})`);
              drawVirtualTable(virtualGroup, node, "#ffae78", fixedTableWidth, headerHeight, rowHeight, tablePadding);

              // 绘制从 Column Name 到虚拟表的连接线
              const sourceX = selectTableX + fixedTableWidth / 2; // Column Name 的右侧中心
              const sourceY = node.x; // node 在 Column Name 中的 Y 坐标
              const targetX = virtualTableX - 50; // 虚拟表左侧
              const targetY = virtualTableY + headerHeight / 2; // 虚拟表表头中心
              svg.append("path")
                .datum({ parent: node.parent, child: node })// 绑定父子节点
                .attr("class", "table-link")
                .attr("fill", "none")
                .attr("stroke", "#B0ACAC")
                .attr("stroke-width", 4)
                .attr("stroke-opacity", 0.8)
                .attr("d", (d) => {
                  const control1Y = sourceY + 50;                   // 第一个控制点 Y 与起点 Y 相同
                  const control1X = (sourceX + targetX) / 2;     // 第一个控制点 X 在中点
                  const control2Y = targetY - 50;                   // 第二个控制点 Y 与终点 Y 相同
                  const control2X = (sourceX + targetX) / 2;     // 第二个控制点 X 在中点
                  return `M${sourceY + 50},${sourceX} C${control1Y},${control1X} ${control2Y},${control2X} ${targetY- 50},${targetX}`;
                });

              tableBounds.push(virtualGroup.node().getBBox());
              lastTableX = virtualTableX + fixedTableWidth; // 更新 X 坐标
            }
          });

          tableBounds.push(selectGroup.node().getBBox());
          tableBounds.push(processingGroup.node().getBBox());
          tableBounds.push(explainGroup.node().getBBox());
        }

        if (fromNodes.length > 0) {
          const fromParent = fromNodes[0].parent;
          const fromTableX = fromParent.y + tableOffset;
          const fromTableY = fromParent.x - fromHeight / 2;
          const fromGroup = svg.append("g").attr("class", "table-group").attr("transform", `translate(${fromTableX},${fromTableY})`);
          drawTable(fromGroup, "Table Name", fromNodes, "#ffae78", fixedTableWidth, headerHeight, rowHeight, tablePadding, fromParent);

          // 添加 Table Name 的 NL Explain 表格
          const fromExplainTableX = fromTableX + fixedTableWidth + 5;
          const fromExplainTableY = fromTableY;
          const fromExplainGroup = svg.append("g").attr("class", "explain-group").attr("transform", `translate(${fromExplainTableX},${fromExplainTableY})`);
          drawNLExplainTable(fromExplainGroup, fromNodes, "#90EE90", fixedTableWidth, headerHeight, rowHeight, tablePadding);

          // 绘制 From 后面的虚拟表结构并添加连接线
          let lastTableX = fromExplainTableX + fixedTableWidth + 50; // 从 NL Explain 右侧开始

          fromNodes.forEach((node) => {
            if (node.data.isVirtual && node.children && node.children.length > 0) {
              const virtualTableX = lastTableX;
              const virtualTableY = fromTableY; // 与 From 对齐
              const virtualGroup = svg.append("g").attr("class", "virtual-table-group").attr("transform", `translate(${virtualTableX},${virtualTableY})`);
              drawVirtualTable(virtualGroup, node, "#ffae78", fixedTableWidth, headerHeight, rowHeight, tablePadding);

              // 绘制从 Table Name 到虚拟表的连接线
              const sourceX = fromTableX + fixedTableWidth / 2; // Table Name 的右侧中心
              const sourceY = node.x; // 使用 node 的 x 坐标（Table Name 中的位置）
              const targetX = virtualTableX - 125; // 虚拟表的左侧
              const targetY = virtualTableY + headerHeight / 2; // 虚拟表表头的中心
              // 计算控制点
              const control1X = sourceX + (targetX - sourceX) / 2; // 第一个控制点 X：起点向终点方向偏移 1/4
              const control1Y = sourceY; // 第一个控制点 Y：与起点 Y 相同，水平延伸
              const control2X = targetX - (targetX - sourceX) / 2; // 第二个控制点 X：终点向起点方向偏移 1/4
              const control2Y = targetY; // 第二个控制点 Y：与终点 Y 相同，水平延伸

              svg.append("path")
                .datum({ parent: node.parent, child: node }) // 绑定父子节点
                .attr("class", "table-link")
                .attr("fill", "none")
                .attr("stroke", "#B0ACAC")
                .attr("stroke-width", 4)
                .attr("stroke-opacity", 0.8)
                .attr("d", `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`);

              tableBounds.push(virtualGroup.node().getBBox());
              lastTableX = virtualTableX + fixedTableWidth + 50; // 更新下一个表格的 X 坐标
            }
          });

          tableBounds.push(fromGroup.node().getBBox());
          tableBounds.push(fromExplainGroup.node().getBBox());
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
            drawTable(tableGroup, parentNode.data.name, childNodes, "#ffae78", fixedTableWidth, headerHeight, rowHeight, tablePadding, parentNode);

            // 添加 NL Explain 表格（在虚拟表之前）
            let lastTableX = tableX; // 从主表格右侧开始
            const explainTableX = lastTableX + fixedTableWidth + 5; // 在主表格右侧偏移
            const explainTableY = tableY; // 与主表格对齐
            const explainGroup = svg.append("g")
              .attr("class", "explain-group")
              .attr("transform", `translate(${explainTableX},${explainTableY})`);
            drawNLExplainTable(explainGroup, childNodes, "#90EE90", fixedTableWidth, headerHeight, rowHeight, tablePadding);

            // 更新 lastTableX
            lastTableX = explainTableX + fixedTableWidth;

            // 检查并绘制虚拟表
            childNodes.forEach((node) => {
              if (node.data.isVirtual && node.children && node.children.length > 0) {
                const virtualTableX = lastTableX + 50; // 在 NL Explain 后偏移
                const virtualTableY = tableY; // 与主表格对齐
                const virtualGroup = svg.append("g")
                  .attr("class", "virtual-table-group")
                  .attr("transform", `translate(${virtualTableX},${virtualTableY})`);
                drawVirtualTable(virtualGroup, node, "#ffae78", fixedTableWidth, headerHeight, rowHeight, tablePadding);

                // 绘制从表格行到虚拟表的连接线
                const sourceX = tableX + fixedTableWidth / 2; // 主表格右侧中心
                const sourceY = node.x; // node 在主表格中的 Y 坐标
                const targetX = virtualTableX - 125; // 虚拟表左侧
                const targetY = virtualTableY + headerHeight / 2; // 虚拟表表头中心
                // 计算控制点
                const control1X = sourceX + (targetX - sourceX) / 2; // 第一个控制点 X：起点向终点方向偏移 1/4
                const control1Y = sourceY; // 第一个控制点 Y：与起点 Y 相同，水平延伸
                const control2X = targetX - (targetX - sourceX) / 2; // 第二个控制点 X：终点向起点方向偏移 1/4
                const control2Y = targetY; // 第二个控制点 Y：与终点 Y 相同，水平延伸

                svg.append("path")
                  .datum({ parent: node.parent, child: node })// 绑定父子节点
                  .attr("class", "table-link")
                  .attr("fill", "none")
                  .attr("stroke", "#B0ACAC")
                  .attr("stroke-width", 4)
                  .attr("stroke-opacity", 0.8)
                  .attr("d", `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`);

                tableBounds.push(virtualGroup.node().getBBox());
                lastTableX = virtualTableX + fixedTableWidth; // 更新 X 坐标
              }
            });
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
          const rowGroup = group.append("g").attr("class", "row");
          const textContent = d.data.name || d.data.column_name || d.data.table_name || d.data.condition || "";
          const textElement = rowGroup.append("text").attr("x", 0).attr("y", currentYOffset + rowHeight / 2).attr("dy", "0.35em").attr("text-anchor", "middle").attr("fill", "#333").style("font-size", "14px").text(textContent);

          const textWidth = textElement.node().getBBox().width;
          let adjustedHeight = rowHeight;
          if (textWidth > fixedTableWidth - 20) {
            textElement.text("").selectAll("tspan").data(wrapText(textContent, fixedTableWidth - 20)).enter().append("tspan").attr("x", 0).attr("dy", (t, j) => (j === 0 ? "0.35em" : "1.2em")).text((t) => t);
            const lineCount = wrapText(textContent, fixedTableWidth - 20).length;
            adjustedHeight = rowHeight * lineCount; // 与初始绘制一致
          }

          rowGroup.insert("rect", "text").attr("x", -fixedTableWidth / 2).attr("y", currentYOffset).attr("width", fixedTableWidth).attr("height", adjustedHeight).attr("fill", "#FFFFFF").attr("stroke", "#333");

          d.y = group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/)[1];
          d.x = parseFloat(group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/)[2]) + currentYOffset + adjustedHeight / 2;

          svg.append("path")
            .datum({ parent: parentNode, child: d }) // 绑定父子节点
            .attr("class", "table-link")
            .attr("fill", "none")
            .attr("stroke", "#B0ACAC")
            .attr("stroke-width", 4)
            .attr("stroke-opacity", "0.8")
            .attr("d", () => {
              const sourceX = parentNode.y + 50; // 起点 X
              const sourceY = parentNode.x;      // 起点 Y
              const targetX = d.y - 125;          // 终点 X
              const targetY = d.x;               // 终点 Y

              // 计算控制点
              const control1X = sourceX + (targetX - sourceX) / 2;
              const control1Y = sourceY;
              const control2X = targetX - (targetX - sourceX) / 2;
              const control2Y = targetY;

              return `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`;
            });

          currentYOffset += adjustedHeight;
        });
      }

      function drawProcessingTable(group, nodes, headerFill, fixedTableWidth, headerHeight, rowHeight, tablePadding, processingTableX) {
        group.append("rect")
          .attr("x", -fixedTableWidth / 2)
          .attr("y", 0)
          .attr("width", fixedTableWidth)
          .attr("height", headerHeight)
          .attr("fill", headerFill)
          .attr("stroke", "#333");
        group.append("text")
          .attr("x", 0)
          .attr("y", headerHeight / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "middle")
          .attr("fill", "black")
          .style("font-size", "16px")
          .style("font-weight", "bold")
          .text("Column Processing");

        let currentYOffset = headerHeight;
        nodes.forEach((d, i) => {
          const rowGroup = group.append("g").attr("class", "row");
          const processingText = d.data.children && d.data.children.length > 0 ? d.data.children[0].name : "";
          const textElement = rowGroup.append("text")
            .attr("x", 0)
            .attr("y", currentYOffset + rowHeight / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .attr("fill", "#333")
            .style("font-size", "14px")
            .text(processingText);

          const textWidth = textElement.node().getBBox().width;
          let adjustedHeight = rowHeight;
          if (textWidth > fixedTableWidth - 25) {
            textElement.text("")
              .selectAll("tspan")
              .data(wrapText(processingText, fixedTableWidth - 20))
              .enter()
              .append("tspan")
              .attr("x", 0)
              .attr("dy", (t, j) => (j === 0 ? "0.35em" : "1.2em"))
              .text((t) => t);
            const lineCount = wrapText(processingText, fixedTableWidth - 25).length;
            adjustedHeight = rowHeight * lineCount / 1.5;
          }

          rowGroup.insert("rect", "text")
            .attr("x", -fixedTableWidth / 2)
            .attr("y", currentYOffset)
            .attr("width", fixedTableWidth)
            .attr("height", adjustedHeight)
            .attr("fill", "#FFFFFF")
            .attr("stroke", "#333");

          // 更新子节点坐标
          if (d.data.children && d.data.children.length > 0) {
            const groupTransform = group.attr("transform").match(/translate\(([^,]+),([^)]+)\)/);
            d.data.children[0].y = parseFloat(groupTransform[1]);
            d.data.children[0].x = parseFloat(groupTransform[2]) + currentYOffset + adjustedHeight / 2;
          }

          // 绘制从 Column Name (parent) 到 Column Processing 子节点 (node) 的连接线
          if (d.data.children && d.data.children.length > 0) {
            const parentY = parseFloat(d.y); // Column Name 的 y 坐标
            const parentX = parseFloat(d.x); // Column Name 的 x 坐标
            const childY = parseFloat(d.data.children[0].y); // 子节点的 y 坐标
            const childX = parseFloat(d.data.children[0].x); // 子节点的 x 坐标
            if (!isNaN(parentY) && !isNaN(parentX) && !isNaN(childY) && !isNaN(childX)) {
              svg.append("path")
                .datum({ parent: d, child: d.data.children[0] }) // 绑定父子节点
                .attr("class", "table-link")
                .attr("fill", "none")
                .attr("stroke", "#B0ACAC")
                .attr("stroke-width", 4)
                .attr("stroke-opacity", "0.8")
                .attr("d", () => {
                  const sourceX = parentY + fixedTableWidth / 2; // 起点 X
                  const sourceY = parentX;                       // 起点 Y
                  const targetX = childY - 125;                   // 终点 X
                  const targetY = childX;                        // 终点 Y

                  // 计算控制点
                  const control1X = sourceX + (targetX - sourceX) / 2;
                  const control1Y = sourceY;
                  const control2X = targetX - (targetX - sourceX) / 2;
                  const control2Y = targetY;
                  return `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`;
                });
            } else {
              console.warn(`Cannot draw connection from ${d.data.name} to ${d.data.children[0].name}:`, {
                parent_y: d.y,
                parent_x: d.x,
                child_y: d.data.children[0].y,
                child_x: d.data.children[0].x
              });
            }
          }
          currentYOffset += adjustedHeight;
        });
      }

      function drawNLExplainTable(group, nodes, headerFill, fixedTableWidth, headerHeight, rowHeight, tablePadding) {
        // 表头
        group.append("rect")
          .attr("x", -fixedTableWidth / 2)
          .attr("y", 0)
          .attr("width", fixedTableWidth)
          .attr("height", headerHeight)
          .attr("fill", headerFill)
          .attr("stroke", "none")
          .attr("rx", 10)
          .attr("ry", 10);

        group.append("text")
          .attr("x", 0)
          .attr("y", headerHeight / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "middle")
          .attr("fill", "#333")
          .style("font-size", "16px")
          .style("font-weight", "bold")
          .text("NL Explain");

        // 内容区域
        let currentYOffset = headerHeight;
        nodes.forEach((d, i) => {
          const rowGroup = group.append("g")
            .attr("class", "row")
            .datum(d); // 绑定数据到 rowGroup

          const explainText = d.data.nlExplain && d.data.nlExplain.trim() !== ''
            ? `${d.data.nlExplain}`
            : `Explaination for ${d.data.name}`;
          let currentText = explainText;

          // 计算文本的宽度和行数
          const tempTextElement = rowGroup.append("text")
            .attr("x", 0)
            .attr("y", currentYOffset + rowHeight / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .attr("fill", "#333")
            .style("font-size", "14px")
            .text(explainText);

          const textWidth = tempTextElement.node().getBBox().width;
          let adjustedHeight = rowHeight;
          let lines = [explainText];

          if (textWidth > fixedTableWidth - 25) {
            lines = wrapText(explainText, fixedTableWidth - 25);
            const lineCount = lines.length;
            adjustedHeight = rowHeight * lineCount;
          }
          tempTextElement.remove();

          // 添加背景矩形
          const rectElement = rowGroup.insert("rect", "text")
            .attr("x", -fixedTableWidth / 2)
            .attr("y", currentYOffset)
            .attr("width", fixedTableWidth)
            .attr("height", adjustedHeight)
            .attr("fill", "#FFFFFF")
            .attr("stroke", "#bdbaba")
            .attr("rx", 5)
            .attr("ry", 5);

          // 默认展示不可编辑文本
          const textElement = rowGroup.append("text")
            .attr("x", 0)
            .attr("y", currentYOffset + adjustedHeight / 2)
            .attr("text-anchor", "middle")
            .attr("fill", "#333")
            .style("font-size", "14px");

          if (lines.length > 1) {
            textElement.selectAll("tspan")
              .data(lines)
              .enter()
              .append("tspan")
              .attr("x", 0)
              .attr("dy", (t, j) => (j === 0 ? `${-0.6 * (lines.length - 1)}em` : "1.2em"))
              .text((t) => t);
          } else {
            textElement.text(explainText)
              .attr("dy", "0.35em");
          }
          
          // 点击编辑逻辑保持不变
          textElement.on("click", (event) => {
            d3.select("#edit-modal").remove();

            const modalWidth = window.innerWidth * 0.13;
            const modalHeight = window.innerHeight * 0.13;
            const modal = d3.select("body")
              .append("div")
              .attr("id", "edit-modal")
              .style("position", "fixed")
              .style("top", `${event.clientY}px`)
              .style("left", `${event.clientX}px`)
              .style("width", `${modalWidth}px`)
              .style("height", `${modalHeight}px`)
              .style("background", "#fff")
              .style("box-shadow", "0 0 10px rgba(0,0,0,0.5)")
              .style("z-index", 1000);

            const svgContainer = modal.append("svg")
              .attr("width", modalWidth)
              .attr("height", modalHeight);

            const svg = svgContainer.append("g")
              .attr("transform", "translate(20, 20)");

            svg.append("rect")
              .attr("x", 0)
              .attr("y", 0)
              .attr("width", modalWidth - 20)
              .attr("height", modalHeight - 20)
              .attr("fill", "#FFFFFF")
              .attr("stroke", "none")
              .attr("rx", 5)
              .attr("ry", 5);

            const foreignObject = svg.append("foreignObject")
              .attr("x", 10)
              .attr("y", 10)
              .attr("width", modalWidth - 60)
              .attr("height", modalHeight - 90);

            const textarea = foreignObject.append("xhtml:textarea")
              .style("width", "100%")
              .style("height", "100%")
              .style("font-size", "14px")
              .style("color", "#333")
              .style("border", "1px solid #ccc")
              .style("background", "#fff")
              .style("resize", "none")
              .style("padding", "5px")
              .text(currentText);

            const cancelButton = svg.append("g")
              .attr("transform", `translate(10, ${modalHeight - 70})`);
            cancelButton.append("rect")
              .attr("x", 0)
              .attr("y", 0)
              .attr("width", 80)
              .attr("height", 30)
              .attr("fill", "#f44336")
              .attr("rx", 3)
              .attr("ry", 3);
            cancelButton.append("text")
              .attr("x", 40)
              .attr("y", 15)
              .attr("dy", "0.35em")
              .attr("text-anchor", "middle")
              .attr("fill", "#FFFFFF")
              .style("font-size", "14px")
              .text("Cancel");

            const submitButton = svg.append("g")
              .attr("transform", `translate(100, ${modalHeight - 70})`);
            submitButton.append("rect")
              .attr("x", 0)
              .attr("y", 0)
              .attr("width", 80)
              .attr("height", 30)
              .attr("fill", "#4CAF50")
              .attr("rx", 3)
              .attr("ry", 3);
            submitButton.append("text")
              .attr("x", 40)
              .attr("y", 15)
              .attr("dy", "0.35em")
              .attr("text-anchor", "middle")
              .attr("fill", "#FFFFFF")
              .style("font-size", "14px")
              .text("Submit");

            cancelButton.on("click", () => {
              modal.remove();
            });

            submitButton.on("click", () => {
              const newText = textarea.property("value");
              currentText = newText;

              // 更新显示文本
              textElement.selectAll("tspan").remove();
              const newLines = wrapText(newText, fixedTableWidth - 25);
              if (newLines.length > 1) {
                textElement.selectAll("tspan")
                  .data(newLines)
                  .enter()
                  .append("tspan")
                  .attr("x", 0)
                  .attr("dy", (t, j) => (j === 0 ? `${-0.6 * (newLines.length - 1)}em` : "1.2em"))
                  .text((t) => t);
              } else {
                textElement.text(newText)
                  .attr("dy", "0.35em");
              }

              const newHeight = rowHeight * newLines.length;
              if (newHeight !== adjustedHeight) {
                adjustedHeight = newHeight;
                rectElement.attr("height", adjustedHeight);
                textElement.attr("y", currentYOffset + adjustedHeight / 2);
              }

              modal.remove();

              // 更新节点的 nlExplain
              d.data.nlExplain = newText;

              // 构造请求数据
              const requestData = {
                sql_query: self.sqlcode, // 完整的 SQL
                nl_sql: (d.data.children && d.data.children.length > 0) ? d.data.children[0].name : d.data.name, // 当前 nl_explain 的上一级内容
                nl_ex: newText // 修改后的 nl_explain
              };

              console.log("-----------Update NL Explain-----------:");
              console.log(requestData)

              // 发送 POST 请求到后端
              fetch('/api/modify', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
              })
                .then(response => {
                  if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                  }
                  return response.json();
                })
                .then(result => {
                  console.log("Received from backend:", result);
                  self.res = result
                  self.data = self.transformToTree(res);
                  self.draw(self.data); // 使用新的 res 数据绘制
                })
                .catch(error => {
                  console.error("Error sending data to backend:", error);
                });
            });
          });

          currentYOffset += adjustedHeight;
        });
      }

      function drawVirtualTable(group, virtualNode, headerFill, fixedTableWidth, headerHeight, rowHeight, tablePadding) {
        // 绘制虚拟表表头
        const headerRect = group.append("rect")
          .attr("x", -fixedTableWidth / 2)
          .attr("y", 0)
          .attr("width", fixedTableWidth)
          .attr("height", headerHeight)
          .attr("fill", headerFill)
          .attr("stroke", "#333")
          .style("cursor", "pointer"); // 表头半透明

        const headerText = group.append("text")
          .attr("x", 0)
          .attr("y", headerHeight / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "middle")
          .attr("fill", "#333")
          .style("font-size", "16px")
          .style("font-weight", "bold")
          .text(virtualNode.data.name);

        let currentYOffset = headerHeight;
        let isTreeView = false; // 初始为 SQL 视图

        // 生成层级化的 SQL 字符串
        function generateSQLString(node) {
          let sqlLines = [];
          if (node.data.isVirtual && node.children && node.children.length > 0) {
            node.children.forEach((section) => {
              const sectionKeyword = section.data.name;
              sqlLines.push(sectionKeyword);

              if (section.children && section.children.length > 0) {
                section.children.forEach((child) => {
                  let childText = `  ${child.data.name}`; // 缩进表示层级
                  if (child.children && child.children.length > 0) {
                    child.children.forEach((subChild) => {

                      childText += ` AS ${subChild.data.name}`; // 处理 column_processing
                    });
                  }
                  sqlLines.push(childText);
                });
              }
            });
          }
          return sqlLines.join("\n");
        }

        // 绘制 SQL 视图
        function drawSQLView() {
          group.selectAll(".tree-content").remove(); // 移除树状内容
          group.selectAll(".sql-content").remove(); // 移除旧的 SQL 内容
          group.selectAll(".sql-content-bg").remove(); // 移除旧的背景矩形

          const padding = 10; // 内容周围的内边距
          // const sqlText = generateSQLString(virtualNode);

          const placeholderText = "Click to view details";

          // 添加占位符文本
          const placeholderElement = group.append("text")
            .attr("class", "sql-content")
            .attr("x", 0)
            .attr("y", currentYOffset + rowHeight / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .attr("fill", "#333") // 改为深色，与普通文本一致
            .style("font-size", "14px")
            .text(placeholderText);

          // 计算边界并绘制背景矩形
          const textBBox = placeholderElement.node().getBBox();
          const contentHeight = textBBox.height + 2 * padding;

          group.insert("rect", ".sql-content")
            .attr("class", "sql-content-bg")
            .attr("x", -fixedTableWidth / 2)
            .attr("y", currentYOffset)
            .attr("width", fixedTableWidth)
            .attr("height", contentHeight)
            .attr("fill", "#FFFFFF")
            .attr("stroke", "#333")
            .attr("fill-opacity", 0.5);
          // if (sqlText) {
          //   const sqlElement = group.append("text")
          //     .attr("class", "sql-content")
          //     .attr("x", -fixedTableWidth / 2 + padding) // 左边留 padding
          //     .attr("y", currentYOffset + rowHeight / 2)
          //     .attr("dy", "0.35em")
          //     .attr("text-anchor", "start")
          //     .attr("fill", "#333")
          //     .style("font-size", "14px")
          //     .style("font-family", "monospace"); // 使用等宽字体

          //   // 先尝试绘制完整文本，检查宽度
          // sqlElement.text(sqlText);
          // const textBBox = sqlElement.node().getBBox();
          // let lines = [sqlText];
          // let contentHeight = textBBox.height + padding;

          // // 如果文本超出宽度，则换行
          // if (textBBox.width > fixedTableWidth - 2 * padding) {
          //   lines = wrapText(sqlText, fixedTableWidth - 2 * padding - 10);
          //   sqlElement.text(""); // 清空单行文本
          //   sqlElement.selectAll("tspan")
          //     .data(lines)
          //     .enter()
          //     .append("tspan")
          //     .attr("x", -fixedTableWidth / 2 + padding)
          //     .attr("dy", (d, i) => (i === 0 ? "0.35em" : "1.2em"))
          //     .text((d) => d);

          //   // 重新计算高度
          //   const newTextBBox = sqlElement.node().getBBox();
          //   contentHeight = newTextBBox.height + padding;
          // }

          //   // 绘制背景矩形，匹配内容尺寸
          //   group.insert("rect", ".sql-content")
          //     .attr("class", "sql-content-bg")
          //     .attr("x", -fixedTableWidth / 2)
          //     .attr("y", currentYOffset)
          //     .attr("width", fixedTableWidth)
          //     .attr("height", contentHeight)
          //     .attr("fill", "#FFFFFF")
          //     .attr("stroke", "#333")
          //     .attr("fill-opacity", 0.5);
          // } else {
          //   const placeholderText = "Virtual table definition not found";
          //   const placeholderElement = group.append("text")
          //     .attr("class", "sql-content")
          //     .attr("x", -fixedTableWidth / 2 + padding)
          //     .attr("y", currentYOffset + rowHeight / 2)
          //     .attr("dy", "0.35em")
          //     .attr("text-anchor", "start")
          //     .attr("fill", "#999")
          //     .style("font-size", "14px")
          //     .text(placeholderText);

          //   // 计算占位符的实际边界
          //   const textBBox = placeholderElement.node().getBBox();
          //   const contentWidth = textBBox.width + 2 * padding;
          //   const contentHeight = textBBox.height + padding;

          //   group.insert("rect", ".sql-content")
          //     .attr("class", "sql-content-bg")
          //     .attr("x", -fixedTableWidth / 2)
          //     .attr("y", currentYOffset)
          //     .attr("width", fixedTableWidth)
          //     .attr("height", contentHeight)
          //     .attr("fill", "#FFFFFF")
          //     .attr("stroke", "#333")
          //     .attr("fill-opacity", 0.5);
          // }
        }

        // 绘制树状视图
        function drawTreeView() {
          // 清理旧内容
          group.selectAll(".sql-content").remove();
          group.selectAll(".sql-content-bg").remove();
          group.selectAll(".tree-content").remove();
          group.selectAll(".tree-content-bg").remove();

          // 移除旧弹窗
          d3.select("#virtual-table-modal").remove();

          // 创建弹窗容器
          const modalWidth = window.innerWidth * 0.8;
          const modalHeight = window.innerHeight * 0.8;
          const modal = d3.select("body")
            .append("div")
            .attr("id", "virtual-table-modal")
            .style("position", "fixed")
            .style("top", "10%")
            .style("left", "10%")
            .style("width", `${modalWidth}px`)
            .style("height", `${modalHeight}px`)
            .style("background", "#fff")
            .style("border", "1px solid #333")
            .style("box-shadow", "0 0 10px rgba(0,0,0,0.5)")
            .style("z-index", 1000);

          // 创建 SVG 画布
          const svgContainer = modal.append("svg")
            .attr("width", modalWidth)
            .attr("height", modalHeight);

          const virtual_svg = svgContainer.append("g")
            .attr("transform", "translate(50,50)");
          
          // 添加缩放功能
          const zoom = d3.zoom()
            .scaleExtent([0.5, 2])
            .on("zoom", (event) => {
              virtual_svg.attr("transform", event.transform);
            });
          svgContainer.call(zoom);

          // 树布局
          const treeHeight = modalHeight - 100;
          const treeWidth = modalWidth - 200;
          const treeLayout = d3.tree().size([treeHeight, treeWidth]);
          const root = d3.hierarchy(virtualNode.data);
          treeLayout(root);

          // 常量定义
          const rectHeight = 40; // 矩形高度（第一层）
          const padding = 20;    // 矩形两侧额外间距
          const tableWidth = 250; // 表格宽度
          const rowHeight = 40;   // 表格行高
          const headerHeight = 50;// 表格表头高度
          const tableOffset = 300;// 表格相对于父节点的水平偏移量

          // **绘制第一层节点（depth === 0）**
          const level0Nodes = virtual_svg.selectAll("g.level0node")
            .data(root.descendants().filter(d => d.depth === 0))
            .enter()
            .append("g")
            .attr("class", "level0node")
            .attr("transform", (d) => `translate(${d.y},${d.x})`);

          const level0Texts = level0Nodes.append("text")
            .attr("dy", 5)
            .attr("text-anchor", "middle")
            .attr("fill", "black")
            .style("font-size", "14px")
            .text((d) => d.data.name);

          level0Texts.each(function (d) {
            const textWidth = this.getBBox().width + padding * 2;
            d.rectWidth = textWidth;
          });

          level0Nodes.insert("rect", "text")
            .attr("x", (d) => -d.rectWidth / 2)
            .attr("y", -rectHeight / 2)
            .attr("width", (d) => d.rectWidth)
            .attr("height", rectHeight)
            .attr("rx", 8)
            .attr("ry", 8)
            .attr("fill", "#D3D3D3") // 第一层灰色
            .attr("stroke", "#333")
            .attr("fill-opacity", 0.5);

          // **绘制连接线（第一层到第二层）**
          virtual_svg.selectAll("path.table-link")
            .data(root.links().filter(d => d.target.depth === 1))
            .enter()
            .append("path")
            .attr("class", "table-link")
            .attr("fill", "none")
            .attr("stroke", "#aaa")
            .attr("stroke-width", 4)
            .attr("d", (d) => {
              const sourceX = d.source.y + (d.source.rectWidth || 0) / 2; // 起点 X
              const sourceY = d.source.x;                                 // 起点 Y
              const targetX = d.target.y - 50;                            // 终点 X
              const targetY = d.target.x;                                 // 终点 Y

              // 计算控制点
              const control1X = sourceX + (targetX - sourceX) / 2;
              const control1Y = sourceY;
              const control2X = targetX - (targetX - sourceX) / 2;
              const control2Y = targetY;

              return `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`;
            })
            .datum(d => ({ parent: d.source, child: d.target }));

          // **绘制第二层节点（depth === 1）**
          const level1Data = root.descendants().filter(d => d.depth === 1);
          const level1Nodes = virtual_svg.selectAll("g.level1Node")
            .data(root.descendants().filter(d => d.depth === 1))
            .enter()
            .append("g")
            .attr("class", "level1Node")
            .attr("transform", (d) => `translate(${d.y},${d.x})`);

          const level1Texts = level1Nodes.append("text")
            .attr("dy", 5)
            .attr("text-anchor", "middle")
            .attr("fill", "black")
            .style("font-size", "14px")
            .text((d) => {
              return d.data.name;
            });

          level1Texts.each(function (d) {
            const textWidth = this.getBBox().width + padding * 2;
            d.rectWidth = textWidth;
          });

          level1Nodes.insert("rect", "text")
            .attr("x", (d) => -d.rectWidth / 2)
            .attr("y", -rectHeight / 2)
            .attr("width", (d) => d.rectWidth)
            .attr("height", rectHeight)
            .attr("rx", 8)
            .attr("ry", 8)
            .attr("fill", "#FFFFFF") // 第二层白色
            .attr("stroke", "#333")
            .attr("fill-opacity", 0.5);

          // **处理表格样式节点（depth >= 1）**
          const level1Nodes_parent = root.descendants().filter(d => d.depth === 1);

          level1Nodes_parent.forEach((parentNode) => {
            const childNodes = root.descendants().filter(d => d.depth === 2 && d.parent === parentNode);
            if (childNodes.length === 0) return;

            // 计算表格高度
            const tableHeight = headerHeight + childNodes.length * rowHeight + padding * 2;
            const tableX = parentNode.y + tableOffset;
            const tableY = parentNode.x - tableHeight / 2;

            const tableGroup = virtual_svg.append("g")
              .attr("class", "table-group")
              .attr("transform", `translate(${tableX},${tableY})`);

            // 绘制表头
            tableGroup.append("rect")
              .attr("x", -tableWidth / 2)
              .attr("y", 0)
              .attr("width", tableWidth)
              .attr("height", headerHeight)
              .attr("fill", "#ffae78")
              .attr("stroke", "#333");

            tableGroup.append("text")
              .attr("x", 0)
              .attr("y", headerHeight / 2)
              .attr("dy", "0.35em")
              .attr("text-anchor", "middle")
              .attr("fill", "black")
              .style("font-size", "16px")
              .style("font-weight", "bold")
              .text(parentNode.data.name === "Select" ? "Column Name" : parentNode.data.name);

            // 绘制表格行，模仿 drawProcessingTable
            let currentYOffset = headerHeight;
            childNodes.forEach((d, i) => {
              const rowGroup = tableGroup.append("g").attr("class", "row");
              const textContent = d.data.name || "";
              const textElement = rowGroup.append("text")
                .attr("x", 0)
                .attr("y", currentYOffset + rowHeight / 2)
                .attr("dy", "0.35em")
                .attr("text-anchor", "middle")
                .attr("fill", "#333")
                .style("font-size", "14px")
                .text(textContent);

              const textWidth = textElement.node().getBBox().width;
              let adjustedHeight = rowHeight;
              if (textWidth > tableWidth - 20) {
                textElement.text("")
                  .selectAll("tspan")
                  .data(wrapText(textContent, tableWidth - 20))
                  .enter()
                  .append("tspan")
                  .attr("x", 0)
                  .attr("dy", (t, j) => j === 0 ? "0.35em" : "1.2em")
                  .text(t => t);
                const lineCount = wrapText(textContent, tableWidth - 20).length;
                adjustedHeight = rowHeight * lineCount; // 可根据需要调整比例
              }

              rowGroup.insert("rect", "text")
                .attr("x", -tableWidth / 2)
                .attr("y", currentYOffset)
                .attr("width", tableWidth)
                .attr("height", adjustedHeight)
                .attr("fill", "#FFFFFF")
                .attr("stroke", "#333");

              d.y = tableX;
              d.x = tableY + currentYOffset + adjustedHeight / 2;
              currentYOffset += adjustedHeight;
            });

            // 绘制从父节点到表格的连接线
            childNodes.forEach((d) => {
              virtual_svg.append("path")
                .datum({ parent: parentNode, child: d })
                .attr("fill", "none")
                .attr("class", "table-link")
                .attr("stroke", "#aaa")
                .attr("stroke-width", 4)
                .attr("stroke-opacity", 0.8)
                .attr("d", () => {
                  const sourceX = parentNode.y + (parentNode.rectWidth || 0) / 2; // 起点 X
                  const sourceY = parentNode.x;                                   // 起点 Y
                  const targetX = d.y - 125;                                       // 终点 X
                  const targetY = d.x;                                            // 终点 Y

                  // 计算控制点
                  const control1X = sourceX + (targetX - sourceX) / 4; // 第一个控制点 X：起点向终点偏移 1/4
                  const control1Y = sourceY;                          // 第一个控制点 Y：与起点 Y 相同
                  const control2X = targetX - (targetX - sourceX) / 4; // 第二个控制点 X：终点向起点偏移 1/4
                  const control2Y = targetY;                          // 第二个控制点 Y：与终点 Y 相同

                  return `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`;
                });
            });

            let lastTableX = tableX; // 记录最后一个表格的 X 坐标
            let lastTableY = tableY; // 记录最后一个表格的 Y 坐标

            // 处理 Column Processing 表格（仅针对 Select）
            if (parentNode.data.name === "Select" && childNodes.some(d => d.children && d.children.length > 0)) {
              const processingTableX = tableX + tableWidth + 100;
              const processingTableY = tableY;
              console.log(processingTableY)
              const processingGroup = virtual_svg.append("g")
                .attr("class", "table-group")
                .attr("transform", `translate(${processingTableX},${processingTableY})`);

              processingGroup.append("rect")
                .attr("x", -tableWidth / 2)
                .attr("y", 0)
                .attr("width", tableWidth)
                .attr("height", headerHeight)
                .attr("fill", "#87CEEB")
                .attr("stroke", "#333");

              processingGroup.append("text")
                .attr("x", 0)
                .attr("y", headerHeight / 2)
                .attr("dy", "0.35em")
                .attr("text-anchor", "middle")
                .attr("fill", "black")
                .style("font-size", "16px")
                .style("font-weight", "bold")
                .text("Column Processing");

              currentYOffset = headerHeight;
              childNodes.forEach((d, i) => {
                const processingText = d.data.children && d.data.children.length > 0 ? d.data.children[0].name : "";
                const textElement = processingGroup.append("text")
                  .attr("x", 0)
                  .attr("y", currentYOffset + rowHeight / 2)
                  .attr("dy", "0.35em")
                  .attr("text-anchor", "middle")
                  .attr("fill", "#333")
                  .style("font-size", "14px")
                  .text(processingText);

                const textWidth = textElement.node().getBBox().width;
                let adjustedHeight = rowHeight;
                if (textWidth > tableWidth - 20) {
                  textElement.text("")
                    .selectAll("tspan")
                    .data(wrapText(processingText, tableWidth - 20))
                    .enter()
                    .append("tspan")
                    .attr("x", 0)
                    .attr("dy", (t, j) => j === 0 ? "0.35em" : "1.2em")
                    .text(t => t);
                  const lineCount = wrapText(processingText, tableWidth - 20).length;
                  adjustedHeight = rowHeight * lineCount;
                }

                processingGroup.insert("rect", "text")
                  .attr("x", -tableWidth / 2)
                  .attr("y", currentYOffset)
                  .attr("width", tableWidth)
                  .attr("height", adjustedHeight)
                  .attr("fill", "#FFFFFF")
                  .attr("stroke", "#333");

                if (d.data.children && d.data.children.length > 0) {
                  d.data.children[0].y = processingTableX;
                  d.data.children[0].x = processingTableY + currentYOffset + adjustedHeight / 2;
                }

                virtual_svg.append("path")
                  .datum({ parent: d, child: d.data.children[0] })
                  .attr("fill", "none")
                  .attr("class", "table-link")
                  .attr("stroke", "#666")
                  .attr("stroke-width", 4)
                  .attr("stroke-opacity", 0.8)
                  .attr("d", () => {
                    const sourceX = d.y + tableWidth / 2;      // 起点 X
                    const sourceY = d.x;                       // 起点 Y
                    const targetX = processingTableX - 125;    // 终点 X
                    const targetY = d.x;                       // 终点 Y

                    // 计算控制点
                    const control1X = sourceX + (targetX - sourceX) / 2; // 第一个控制点 X：起点向终点偏移 1/4
                    const control1Y = sourceY;                          // 第一个控制点 Y：与起点 Y 相同
                    const control2X = targetX - (targetX - sourceX) / 2; // 第二个控制点 X：终点向起点偏移 1/4
                    const control2Y = targetY;                          // 第二个控制点 Y：与终点 Y 相同

                    return `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`;
                  });

                currentYOffset += adjustedHeight;
              });
              // 更新最后一个表格的坐标
              lastTableX = processingTableX;
              lastTableY = processingTableY;
            }

            // 添加 NL Explain 表格（为每个 parentNode 绘制）
            const nlExplainX = lastTableX + 260;
            const nlExplainY = lastTableY;
            const nlExplainGroup = virtual_svg.append("g")
              .attr("class", "explain-group")
              .attr("transform", `translate(${nlExplainX},${nlExplainY})`);

            drawNLExplainTable(
              nlExplainGroup,
              childNodes, // 当前 parentNode 的子节点（depth === 2）
              "#90EE90", // 浅绿色表头
              tableWidth,
              headerHeight,
              rowHeight,
              padding
            );

            // childNodes.forEach((d, i) => {
            //   const nlExplainRowY = nlExplainY + headerHeight + (i + 0.5) * rowHeight; // 假设每行高度固定为 rowHeight
            //   virtual_svg.append("path")
            //     .attr("fill", "none")
            //     .attr("class", "nl-explain-link")
            //     .attr("stroke", "#aaa")
            //     .attr("stroke-width", 4)
            //     .attr("stroke-opacity", 0.8)
            //     .attr("d", () => {
            //       const sourceX = d.y + tableWidth / 2;
            //       const sourceY = d.x;
            //       const targetX = nlExplainX - 125;
            //       const targetY = nlExplainRowY;

            //       const control1X = sourceX + (targetX - sourceX) / 2;
            //       const control1Y = sourceY;
            //       const control2X = targetX - (targetX - sourceX) / 2;
            //       const control2Y = targetY;

            //       return `M${sourceX},${sourceY} C${control1X},${control1Y} ${control2X},${control2Y} ${targetX},${targetY}`;
            //     });
            // });
            // 将 SVG 添加到全局存储
            virtual_svgs.push(virtual_svg);
          });

          // 添加关闭按钮
          modal.append("div")
            .style("position", "absolute")
            .style("top", "10px")
            .style("right", "10px")
            .style("cursor", "pointer")
            .append("img")
            .attr("src", "src/assets/image/close.png")
            .attr("width", "30")
            .attr("height", "30")
            .attr("alt", "Close")
            .on("click", () => {
              modal.remove();
              drawSQLView();
            });
        }
        // 初始绘制 SQL 视图
        drawSQLView();

        // 点击切换视图
        group.on("click", function () {
          isTreeView = !isTreeView;
          if (isTreeView) {
            drawTreeView();
            if (self.currentTree && self.currentTree !== null) {
              console.log("------enter highlight in virtual table-------");
              virtual_svgs.forEach(current_svg => {
                highlightSubtree(current_svg, d3.hierarchy(virtualNode.data), self.currentTree);
              });
            }
          } else {
            drawSQLView();
          }
        });
      }

      // 辅助函数：将长文本拆分为多行
      function wrapText(text, maxWidth) {
        const words = text.trim().split(" "); // 移除首尾空格并按空格分割
        const lines = [];
        let currentLine = "";

        // 创建临时文本元素用于测量
        const tempText = svg.append("text")
          .attr("visibility", "hidden")
          .style("font-size", "14px");

        // 如果文本为空，直接返回空数组
        if (!text || words.length === 0) {
          tempText.remove();
          return [];
        }

        for (let i = 0; i < words.length; i++) {
          const word = words[i];
          const testLine = currentLine ? currentLine + " " + word : word; // 处理首词无空格的情况

          tempText.text(testLine);
          const textWidth = tempText.node().getBBox().width;

          if (textWidth <= maxWidth) {
            currentLine = testLine; // 如果宽度合适，追加到当前行
          } else {
            if (currentLine) {
              lines.push(currentLine); // 推送当前行（非空）
            }
            currentLine = word; // 新词作为新行开始
          }
        }

        // 推送最后一行（如果有内容）
        if (currentLine) {
          lines.push(currentLine);
        }

        tempText.remove();
        return lines;
      }
      // **将文本移回中心**
      texts.attr("text-anchor", "middle");

      function highlightSubtree(svg, originalRoot, currentTree) {
  // 收集 currentTree 中的节点名称和连接对
  const currentNames = [];
  const currentPairs = [];

  function collectValues(node, parentName = '') {
    if (!node) return;
    const prefix = parentName ? `${parentName}-` : '';
    if (node.name) {
      currentNames.push(`${prefix}${node.name}`);
    }
    if (node.nlExplain) {
      currentNames.push(`${prefix}${node.nlExplain}`);
    }
    if (node.children) {
      node.children.forEach(child => {
        if (node.name && child.name) {
          currentPairs.push(`${prefix}${node.name}-${child.name}`);
        }
        if (node.name && child.nlExplain) {
          currentPairs.push(`${prefix}${node.name}-${child.nlExplain}`);
        }
        collectValues(child, node.name || parentName);
      });
    }
  }

  collectValues(currentTree);
  console.log("Current Names:", currentNames);
  console.log("Current Pairs:", currentPairs);

  const allNodes = originalRoot.descendants();
  console.log("All Nodes:", allNodes.map(n => ({
    name: n.data.name,
    nlExplain: n.data.nlExplain,
    depth: n.depth
  })));

  allNodes.forEach(node => {
    const nodeName = node.data ? node.data.name : node.name;
    const nodeNLExplain = node.data ? (node.data.nlExplain || '') : (node.nlExplain || '');
    const parentName = node.parent ? node.parent.data.name : '';
    const prefix = parentName ? `${parentName}-` : '';
    const nameKey = `${prefix}${nodeName}`;
    const nlExplainKey = `${prefix}${nodeNLExplain}`;

    // 检查是否需要高亮（直接比较列表）
    const shouldHighlight = currentNames.includes(nameKey) || currentNames.includes(nlExplainKey);
    // console.log(nodeName, '||', nodeNLExplain)
    // console.log(nameKey, '||', nlExplainKey)

    // 第一层节点一定会被高亮 (depth === 0)
    svg.selectAll("g.level0node rect")
        .attr("stroke", "#FFDA20")
        .attr("stroke-width", 5);
    
    if (shouldHighlight) {
      console.log(nodeName, '||', nodeNLExplain)
      console.log(nameKey, '||', nlExplainKey)
      // console.log(node)
      // 高亮第二层节点 (depth === 1)
      svg.selectAll("g.level1Node rect")
        .filter(function(d) {
          // 检查 name 是否匹配
          if (!d || !node) return false;
          const matchesName = d.data.name === node.data.name;
          // 可选：检查父节点名称
          const matchesParent = d.parent && node.parent && d.parent.data.name === node.parent.data.name;
          return matchesName && matchesParent; // 根据需要调整条件
        })
        .attr("stroke", "#FFDA20")
        .attr("stroke-width", 5);

      // 高亮所有矩形（通用选择器）
      svg.selectAll("rect")
        .filter(d => d === node)
        .attr("stroke", "#FFDA20")
        .attr("stroke-width", 5);

      // 高亮表格节点
      svg.selectAll(".table-group rect")
        .filter(function() {
          const text = d3.select(this.parentNode).select("text").text() || '';
          return text.replace(/\s+/g, '') === nodeName.replace(/\s+/g, '');
        })
        .attr("stroke", "#FFDA20")
        .attr("stroke-width", 5);

      svg.selectAll(".explain-group rect")
        .filter(function() {
          const text = d3.select(this.parentNode).select("text").text() || '';
          return text.replace(/\s+/g, '') === nodeNLExplain.replace(/\s+/g, '');
        })
        .attr("stroke", "#FFDA20")
        .attr("stroke-width", 5);
    }
  });

  // 高亮连接线
  svg.selectAll("path.table-link")
    .filter(function(d) {
      if (!d || !d.parent || !d.child) return false;

      const parentPrefix = d.parent.parent ? `${d.parent.parent.data.name}-` : '';
      const parentName = d.parent.data.name;
      const childHasData = d.child.data !== undefined;
      const childName = childHasData
        ? (d.child.data.name || d.child.data.nlExplain)
        : (d.child.name || d.child.nlExplain);
      const pairKey = `${parentPrefix}${parentName}-${childName}`;

      // 检查是否需要高亮连接线
      const shouldHighlightLink = currentPairs.includes(pairKey);
      if (shouldHighlightLink) {
        // console.log("Matched PairKey:", pairKey);
      }
      return shouldHighlightLink;
    })
    .attr("stroke", "#FFDA20")
    .attr("stroke-width", 4);
}
      // 如果有 currentTree，则高亮
      if (this.currentTree && this.currentTree !== null) {
        console.log("------enter highlight-------")
        highlightSubtree(svg, root, this.currentTree);
      }
    }
  }
}

</script>

<style scoped>
svg {
  border: 1px solid #ccc;
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* 或 center，根据需求调整水平对齐 */
  margin-bottom: 0;
  font-size: 22px;
  font-weight: 550; /* 比 bold（700）稍轻，现代感更强 */
  color: #4e4e4e; /* 深灰色文字，确保对比度 */
  background: #dbf1d5;
  /* border-radius: 100px;  */
  height: 40px; /* 固定高度 */
  padding: 0 15px; /* 左右padding增加，上下靠height控制 */
  box-sizing: border-box; /* 确保padding不增加总高度 */
  line-height: 1; /* 确保文字垂直居中更精确 */
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
  min-width: 180px;
  /* 避免过窄 */
  max-width: 250px;
  /* 限制最大宽度 */
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

/* .NLExplain {
  padding: 20px;
} */

.combined-card {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
}

.data-item {
  margin-bottom: 20px;
}

.description {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
}

.code-block {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap; /* 保留空白并自动换行 */
}

.code-block code {
  font-family: 'Courier New', Courier, monospace;
  color: #333; /* 默认文字颜色 */
}

.highlight {
  color: #d63200; /* 高亮颜色 */
}
</style>