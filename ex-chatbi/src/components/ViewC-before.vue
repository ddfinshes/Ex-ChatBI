<template>
  <div class="common-layout">
    <h1>VIEW C</h1>
    <div class="select-container">
      <div class="card-container">
        <div v-for="(table_data, index) in sqljson" :key="index">
            <div v-if="table_data.created_virtual_table == 'False'"></div>
            <div v-for="(sql_content, j) in table_data.sql_content" :key="j">
                <div v-if="sql_content.keywords == 'Select'"> 
                    <!-- 處理select -->
                    <SelectCard :select_data="sql_content.scratched_content" class="select-card"/>
                    
                </div>

            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";
import SelectCard from './ViewC_Components/selectCard.vue';
export default {
  components: {
    SelectCard
  },
  props: {
    select_data: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      sqljson: [],
      select_data: []
      
    };
  },
  methods: {
    select(select_scratched_content){

    },
    async main_sqljson() {
      try {
        // const res = await axios.post(
        //     "/api/sql2json",
        //     {
        //     headers: {
        //     "Content-Type": "application/json",
        //     Accept: "application/json",
        //     },
        // }
        // )
        const res = {
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
        };
        this.sqljson = res.content;
        // 处理select数据并生成cards
        

        // 1. 是否是虚拟表。如果不是虚拟表，则是主表。否则是次表
        const table_num = this.sqljson.length;
        for (let i = 0; i < table_num; i++) {
          let table_data = this.sqljson[i];
          let sql_content = table_data["sql_content"];
          if (table_data.created_virtual_table == "False") {
            // to-do
          }
          // 处理sql_content
          let sql_content_num = sql_content.length;
          for (let j = 0; j < sql_content_num; j++) {
            const sql_code = sql_content[j];
            let keywords = sql_code["keywords"];
            if (keywords == "Select") {
              let select_scratched_content = sql_code["scratched_content"];

              this.select(select_scratched_content);
            }
          }
        }
      } catch (error) {
        console.error("Error fetching response:", error);
      }
    },
  },
  mounted() {
    this.main_sqljson();
  },
};
</script>

<style>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.text.item {
  margin: 8px 0;
}

.sub-content {
  margin-left: 20px;
  color: #666;
}
</style>
