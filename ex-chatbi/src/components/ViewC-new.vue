<template>
  <div ref="container" class="sql-vis-container"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as d3 from 'd3';

const props = {data:{
          content: [
            {
              created_virtual_table: "False",
              sql_content: [
                {
                  keywords: "Select",
                  scratched_content: [
                    {
                      column_name: "Sep2024NewMembers",
                      column_processing:
                        "(SELECT COUNT(DISTINCT member_code) FROM Sep2024FirstTimeCustomers) AS Sep2024NewMembers",
                      sub_select: "True",
                      sub_scratched_content: [
                        {
                          keywords: "Select",
                          scratched_content: [
                            {
                              column_name: "COUNT(DISTINCT member_code)",
                              column_processing: "COUNT(DISTINCT member_code)",
                            },
                          ],
                        },
                        {
                          keywords: "From",
                          scratched_content: [
                            {
                              table_name: "Sep2024FirstTimeCustomers",
                              is_virtual_table: "True",
                            },
                          ],
                        },
                      ],
                    },
                  ],
                },
                { keywords: "From", scratched_content: [] },
              ],
            },
            {
              created_virtual_table: "True",
              virtual_table_name: "Sep2024Transactions",
              sql_content: [
                {
                  keywords: "Select",
                  scratched_content: [
                    { column_name: "*", column_processing: "" },
                  ],
                },
                {
                  keywords: "From",
                  scratched_content: [
                    {
                      table_name: "dm_member_sales_chatbi",
                      is_virtual_table: "False",
                    },
                  ],
                },
                {
                  keywords: "Where",
                  scratched_content: [
                    {
                      content:
                        "transaction_date BETWEEN '2024-09-01' AND '2024-09-30'",
                    },
                  ],
                },
              ],
            },
            {
              created_virtual_table: "True",
              virtual_table_name: "Sep2024FirstTimeCustomers",
              sql_content: [
                {
                  keywords: "Select",
                  scratched_content: [
                    {
                      column_name: "member_code",
                      column_processing: "DISTINCT member_code",
                    },
                  ],
                },
                {
                  keywords: "From",
                  scratched_content: [
                    {
                      table_name: "Sep2024Transactions",
                      is_virtual_table: "True",
                    },
                  ],
                },
                {
                  keywords: "Where",
                  scratched_content: [
                    {
                      content:
                        "member_code NOT IN (SELECT member_code FROM dm_member_sales_chatbi)",
                      sub_select: "True",
                      sub_scratched_content: [
                        {
                          keywords: "Select",
                          scratched_content: [
                            {
                              column_name: "member_code",
                              column_processing: "",
                            },
                          ],
                        },
                        {
                          keywords: "From",
                          scratched_content: [
                            {
                              table_name: "dm_member_sales_chatbi",
                              is_virtual_table: "False",
                            },
                          ],
                        },
                      ],
                    },
                  ],
                },
              ],
            },
          ],
        }};
const container = ref(null);

onMounted(() => {
  const width = 1200;
  const height = 800;
  
  const svg = d3.select(container.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // 数据处理
  const processData = (content) => {
    return content.map(table => ({
      id: table.virtual_table_name || 'Main Query',
      type: table.created_virtual_table === 'True' ? 'Virtual Table' : 'Main Query',
      children: table.sql_content.flatMap(clause => 
        clause.scratched_content.map(item => ({
          id: `${clause.keywords}-${item.column_name || item.table_name}`,
          type: clause.keywords,
          content: item,
          children: item.sub_scratched_content?.map(sub => ({
            id: `${sub.keywords}-sub`,
            type: `Sub ${sub.keywords}`,
            content: sub.scratched_content[0]
          })) || []
        }))
      )
    }));
  };

  // 创建树布局
  const root = d3.hierarchy({ 
    children: processData(props.data.content) 
  }, d => d.children);

  const treeLayout = d3.tree()
    .size([height - 100, width - 200])
    .separation(() => 1.2);

  treeLayout(root);

  // 节点绘制
  const nodes = svg.append('g')
    .attr('transform', 'translate(100,50)')
    .selectAll('.node')
    .data(root.descendants())
    .join('g')
    .attr('class', 'node')
    .attr('transform', d => `translate(${d.y},${d.x})`);

  nodes.append('rect')
    .attr('width', 220)
    .attr('height', d => d.data.type === 'Virtual Table' ? 120 : 80)
    .attr('rx', 8)
    .style('fill', d => {
      switch(d.data.type) {
        case 'Virtual Table': return '#e3f2fd';
        case 'SELECT': return '#e8f5e9';
        case 'FROM': return '#fff3e0';
        case 'WHERE': return '#ffebee';
        default: return '#f5f5f5';
      }
    })
    .style('stroke', '#666');

  // 节点内容
  nodes.append('foreignObject')
    .attr('width', 200)
    .attr('height', d => d.data.type === 'Virtual Table' ? 100 : 60)
    .attr('x', 10)
    .attr('y', 10)
    .append('xhtml:div')
    .style('font-family', 'Arial')
    .style('font-size', '12px')
    .html(d => {
      const data = d.data;
      if (data.type === 'Virtual Table') {
        return `
          <div class="node-header">📁 ${data.id}</div>
          <div class="node-type">(Virtual Table)</div>
        `;
      }
      
      return `
        <div class="keyword">${data.type}</div>
        ${data.content.column_name ? `<div>Column: ${data.content.column_name}</div>` : ''}
        ${data.content.table_name ? `<div>Table: ${data.content.table_name}</div>` : ''}
        ${data.content.content ? `<div>Condition: ${data.content.content}</div>` : ''}
        ${data.content.column_processing ? `<div class="processing">Processing: ${data.content.column_processing}</div>` : ''}
        ${data.children.length ? `<div class="sub-query">Contains sub-query</div>` : ''}
      `;
    });

  // 连接线
  svg.append('g')
    .attr('transform', 'translate(100,50)')
    .selectAll('.link')
    .data(root.links())
    .join('path')
    .attr('class', 'link')
    .attr('d', d3.linkHorizontal()
      .x(d => d.y + 110)
      .y(d => d.x))
    .style('fill', 'none')
    .style('stroke', '#999')
    .style('stroke-width', 1.5);
});
</script>

<style>
.sql-vis-container {
  padding: 20px;
  background: white;
  border-radius: 8px;
}

.node-header {
  font-weight: bold;
  margin-bottom: 8px;
  color: #2c3e50;
}

.keyword {
  color: #1e88e5;
  font-weight: bold;
  margin-bottom: 6px;
}

.processing {
  font-size: 0.9em;
  color: #666;
  margin-top: 4px;
}

.sub-query {
  color: #e53935;
  font-style: italic;
  margin-top: 6px;
}

.node-type {
  color: #757575;
  font-size: 0.8em;
}
</style>